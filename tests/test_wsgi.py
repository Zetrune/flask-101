from flask_testing import TestCase
from wsgi import app, init_product_list

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        init_product_list()

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        print(products)
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_get_existing_product(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict)
        self.assertEqual(status_code, 200)

    def test_get_not_existing_product_0(self):
        response = self.client.get("/api/v1/products/0")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)

    def test_get_not_existing_product_max_index(self):
        response = self.client.get("/api/v1/products")
        product_list = response.json
        index = len(product_list) + 1
        response = self.client.get(f"/api/v1/products/{index}")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)

    def test_delete_existing_product(self):
        response = self.client.delete("/api/v1/products/1")
        print(f"Response = [{response.json}]")
        status_code = response.status_code
        self.assertEqual(status_code, 204)
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)

    def test_delete_not_existing_product_0(self):
        response = self.client.delete("/api/v1/products/0")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)

    def test_delete_not_existing_product_max_index(self):
        response = self.client.get("/api/v1/products")
        product_list = response.json
        index = len(product_list) + 1
        response = self.client.get(f"/api/v1/products/{index}")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)
