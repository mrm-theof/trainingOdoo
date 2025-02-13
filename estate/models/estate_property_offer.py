from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False, default=False)

    # Relation vers la propriété, pour savoir à quel bien s’applique l’offre
    property_id = fields.Many2one('estate.property', required=True)

    # Exemple de relation vers un client (pour savoir qui fait l’offre)
    partner_id = fields.Many2one('res.partner', string="Customer")

    def action_accept_offer(self):
        """Accepter l'offre"""
        for offer in self:
            if offer.status == 'refused':
                raise UserError("Impossible d'accepter une offre déjà refusée.")
            offer.status = 'accepted'
            # On peut aussi modifier l'état ou le prix de la propriété, par exemple :
            offer.property_id.state = 'offer_received'
            offer.property_id.selling_price = offer.price



    def action_refuse_offer(self):
        """Refuser l'offre"""
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("Impossible de refuser une offre déjà acceptée.")
            offer.status = 'refused'
