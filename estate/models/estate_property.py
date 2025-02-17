from odoo.exceptions import UserError
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=False)  # Correction: pas de readonly

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags",
    )
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    # ✅ Ajout du champ `state`
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string="State", default="new", required=True)

    bedrooms = fields.Integer(string="Bedrooms", default=1)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")

    # ✅ Correction du champ total_area
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")

    # Champ pour relier une propriété à un vendeur (utilisateur Odoo)
    salesman_id = fields.Many2one(
        "res.users",  # Modèle cible
        string="Vendeur",
        default=lambda self: self.env.user,  # Définit l'utilisateur actuel comme vendeur par défaut
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area  # Correction: `record.total_area`

    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        ondelete='cascade',
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )

    # ✅ Correction: Ajout du champ `best_price` correctement défini
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)

    @api.depends('selling_price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = record.selling_price if record.selling_price else 0.0

    # ✅ Boutons "Annuler" et "Vendu" corrigés
    def action_sell_property(self):
        """Marquer la propriété comme vendue"""
        for record in self:
            if record.state == 'canceled':
                raise UserError("Une propriété annulée ne peut pas être vendue.")
            record.state = 'sold'

    def action_cancel_property(self):
        """Annuler la propriété"""
        for record in self:
            if record.state == 'sold':
                raise UserError("Une propriété vendue ne peut pas être annulée.")
            record.state = 'canceled'

    # ✅ Ajout de la contrainte Python
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """Vérifie que le prix de vente ne soit pas inférieur à 90% du prix attendu."""
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                # Si le prix de vente est nul (avant validation d'une offre), on ne bloque pas
                continue
            min_price = record.expected_price * 0.9  # 90% du prix attendu
            if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                raise ValidationError(_("Le prix de vente ne peut pas être inférieur à 90% du prix attendu !"))

    @api.model
    def create(self, vals):
        """Forcer l'état à 'offer_received' lors de la création d'une propriété"""
        vals['state'] = 'offer_received'  # On impose l'état "offer_received"
        return super(EstateProperty, self).create(vals)

    # ✅ Empêcher la suppression si l'état n'est pas "new" ou "canceled"
    @api.ondelete(at_uninstall=False)
    def _check_delete_property(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(_("Vous ne pouvez supprimer une propriété que si son état est 'Nouveau' ou 'Annulé'."))


    _sql_constraints = [
        ('unique_property_name', 'UNIQUE(name)', 'The property name must be unique!'),
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'The selling price cannot be negative.')
    ]
