from odoo import fields, models

class PropertyType(models.Model):
        _name = 'estate.property.type'
        _description = 'Estate Property Type'
        _order = 'name asc'  # Tri par nom croissant (ordre alphabétique)

        name = fields.Char(string="Title", required=True)
        property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties", readonly=True)




