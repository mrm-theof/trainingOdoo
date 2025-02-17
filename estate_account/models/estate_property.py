import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one(
        'account.move',
        string="Facture",
        readonly=True
    )

    def action_sell_property(self):
        """ Étendre la méthode pour ajouter la logique de facturation avec 6% + 100$ """
        for record in self:
            if not record.buyer_id:
                raise models.ValidationError("La propriété doit avoir un acheteur avant d'être vendue.")

            # Calcul des frais
            frais_agence = record.selling_price * 0.06  # 6% du prix de vente
            frais_admin = 100.00  # 100$ fixe

            # Création de la facture client
            invoice_vals = {
                'partner_id': record.buyer_id.id,  # Client (acheteur)
                'move_type': 'out_invoice',  # Facture de vente
                'invoice_line_ids': [
                    # 1ère ligne : 6% du prix de vente
                    (0, 0, {
                        'name': f"Commission agence - 6% sur {record.selling_price}",
                        'quantity': 1,
                        'price_unit': frais_agence,
                    }),
                    # 2ème ligne : Frais administratifs
                    (0, 0, {
                        'name': "Frais administratifs",
                        'quantity': 1,
                        'price_unit': frais_admin,
                    }),
                ],
            }
            invoice = self.env['account.move'].create(invoice_vals)

            # 🔗 Associer la facture à la propriété
            record.invoice_id = invoice.id

            _logger.info(f"🧾 Facture créée avec succès : {invoice.id} pour la propriété {record.name}")
            print(f"✅ Facture créée avec succès : {invoice.id} pour la propriété {record.name}")

        return super().action_sell_property()
