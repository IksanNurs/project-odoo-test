from odoo import http
from odoo.http import request

class MaterialController(http.Controller):

    @http.route('/api/material', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **post):
        material = request.env['material.registration'].create({
            'material_code': post.get('material_code'),
            'material_name': post.get('material_name'),
            'material_type': post.get('material_type'),
            'material_buy_price': post.get('material_buy_price'),
            'supplier_id': post.get('supplier_id'),
        })
        return {'status': 'success', 'data': material.id}

    @http.route('/api/materials', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, material_type=None):
        domain = []
        if material_type:
            domain.append(('material_type', '=', material_type))
        materials = request.env['material.registration'].search(domain)
        result = [{'material_code': m.material_code, 'material_name': m.material_name} for m in materials]
        return {'status': 'success', 'data': result}
    
    @http.route('/api/material/<int:material_id>', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **post):
        material = request.env['material.registration'].browse(material_id)
        if material:
            material.write({
                'material_code': post.get('material_code', material.material_code),
                'material_name': post.get('material_name', material.material_name),
                'material_type': post.get('material_type', material.material_type),
                'material_buy_price': post.get('material_buy_price', material.material_buy_price),
                'supplier_id': post.get('supplier_id', material.supplier_id.id),
            })
            return {'status': 'success', 'data': material.id}
        return {'status': 'error', 'message': 'Material not found'}

    @http.route('/api/material/<int:material_id>', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        material = request.env['material.registration'].browse(material_id)
        if material:
            material.unlink()
            return {'status': 'success', 'message': 'Material deleted'}
        return {'status': 'error', 'message': 'Material not found'}
