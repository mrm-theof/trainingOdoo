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

    # Relation vers la propriété
    property_id = fields.Many2one('estate.property', required=True)

    # Acheteur potentiel (ex. client)
    partner_id = fields.Many2one('res.partner', string="Customer")

    def action_accept_offer(self):
        """Accepter l'offre"""
        for offer in self:
            # Vérifie si la propriété est déjà vendue ou déjà dotée d'un acheteur
            if offer.property_id.buyer_id:
                raise UserError("Impossible d'accepter une seconde offre pour la même propriété !")
            if offer.status == 'refused':
                raise UserError("Impossible d'accepter une offre déjà refusée.")

            # Met à jour le statut de l'offre
            offer.status = 'accepted'
            # Met à jour la propriété associée
            offer.property_id.state = 'offer_received'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse_offer(self):
        """Refuser l'offre"""
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("Impossible de refuser une offre déjà acceptée.")
            offer.status = 'refused'
