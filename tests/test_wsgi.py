from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_get_existing_product(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status = response.status
        self.assertIsInstance(product, dict)
        self.assertEqual(status, 200)

    def test_get_not_existing_product(self):
        response = self.client.get("/api/v1/products/0")
        product = response.json
        status = response.status
        self.assertIsInstance(product, None)
        self.assertEqual(status, 404)
