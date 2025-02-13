from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=False)  # Correction: pas de readonly

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
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
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
