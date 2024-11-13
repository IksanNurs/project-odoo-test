from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterialRegistration(TransactionCase):

    def setUp(self):
        # Setup awal, membuat data supplier untuk tes
        super(TestMaterialRegistration, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Supplier A',
            'supplier': True,
        })

    def test_create_material(self):
        # Test untuk membuat material baru
        material = self.env['material.registration'].create({
            'material_code': 'M001',
            'material_name': 'Cotton Fabric',
            'material_type': 'cotton',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })
        self.assertEqual(material.material_code, 'M001')
        self.assertEqual(material.material_name, 'Cotton Fabric')
        self.assertEqual(material.material_type, 'cotton')
        self.assertEqual(material.material_buy_price, 150)
        self.assertEqual(material.supplier_id, self.supplier)

    def test_material_price_constraint(self):
        # Test untuk memvalidasi harga material < 100
        with self.assertRaises(ValidationError):
            self.env['material.registration'].create({
                'material_code': 'M002',
                'material_name': 'Jeans Fabric',
                'material_type': 'jeans',
                'material_buy_price': 50,  # Harga kurang dari 100
                'supplier_id': self.supplier.id
            })

    def test_update_material(self):
        # Test untuk update material yang sudah ada
        material = self.env['material.registration'].create({
            'material_code': 'M003',
            'material_name': 'Jeans Fabric',
            'material_type': 'jeans',
            'material_buy_price': 200,
            'supplier_id': self.supplier.id
        })
        material.write({
            'material_name': 'Updated Jeans Fabric',
            'material_buy_price': 250
        })
        self.assertEqual(material.material_name, 'Updated Jeans Fabric')
        self.assertEqual(material.material_buy_price, 250)

    def test_delete_material(self):
        # Test untuk menghapus material
        material = self.env['material.registration'].create({
            'material_code': 'M004',
            'material_name': 'Fabric',
            'material_type': 'fabric',
            'material_buy_price': 120,
            'supplier_id': self.supplier.id
        })
        material_id = material.id
        material.unlink()
        with self.assertRaises(Exception):
            self.env['material.registration'].browse(material_id).exists()

    def test_filter_material_by_type(self):
        # Test untuk filter material berdasarkan tipe
        self.env['material.registration'].create({
            'material_code': 'M005',
            'material_name': 'Cotton Shirt',
            'material_type': 'cotton',
            'material_buy_price': 200,
            'supplier_id': self.supplier.id
        })
        cotton_materials = self.env['material.registration'].search([('material_type', '=', 'cotton')])
        self.assertEqual(len(cotton_materials), 1)
