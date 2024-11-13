from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.registration'
    _description = 'Material Registration'

    material_code = fields.Char('Material Code', required=True)
    material_name = fields.Char('Material Name', required=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], string='Material Type', required=True)
    material_buy_price = fields.Float('Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', True)], required=True)

    @api.constrains('material_buy_price')
    def check_material_price(self):
        if self.material_buy_price < 100:
            raise ValidationError('Material Buy Price must be at least 100!')
