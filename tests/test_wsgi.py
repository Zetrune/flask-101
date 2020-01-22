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
        self.assertEqual(status, '200 OK')

    def test_get_not_existing_product_0(self):
        response = self.client.get("/api/v1/products/0")
        product = response.json
        status = response.status
        self.assertIsNone(product)
        self.assertEqual(status, '404 NOT FOUND')

    def test_get_not_existing_product_max_index(self):
        response = self.client.get("/api/v1/products")
        product_list = response.json
        index = str(len(product_list) + 1)
        response = self.client.get("/api/v1/products/index")
        product = response.json
        status = response.status
        self.assertIsNone(product)
        self.assertEqual(status, "404 NOT FOUND")
