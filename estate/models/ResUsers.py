from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",  # Modèle cible
        "salesman_id",      # Champ Many2one dans estate.property qui relie à res.users
        string="Propriétés en vente",
        domain=[('state', 'in', ['new', 'offer_received'])],  # Filtrer uniquement les propriétés disponibles
    )
