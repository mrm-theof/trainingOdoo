from odoo import fields, models

class PropertyType(models.Model):
        _name = 'estate.property.type'
        _description = 'Estate Property Type'

        name = fields.Char(string="Title", required=True)
        property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties", readonly=True)




