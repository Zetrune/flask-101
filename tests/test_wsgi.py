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

    def test_create_not_existing_product(self):
        payload = {"name": "Workelo"}
        response = self.client.get("/api/v1/products")
        product_list = response.json
        nb_product_before_add = len(product_list)
        response = self.client.post("/api/v1/products", json=payload)
        target_id = response.json
        status_code = response.status_code
        self.assertEqual(status_code, 201)
        response = self.client.get(f"/api/v1/products/{target_id}")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict)
        self.assertEqual(status_code, 200)
        response = self.client.get("/api/v1/products")
        product_list = response.json
        nb_product_after_add = len(product_list)
        self.assertEqual(nb_product_after_add, nb_product_before_add + 1)

    def test_create_product_on_empty_id(self):
        response = self.client.delete("/api/v1/products/1")
        status_code = response.status_code
        self.assertEqual(status_code, 204)
        response = self.client.get("/api/v1/products/1")
        product = response.json
        status_code = response.status_code
        self.assertIsNone(product)
        self.assertEqual(status_code, 404)
        payload = {"name": "Workelo"}
        response = self.client.get("/api/v1/products")
        product_list = response.json
        nb_product_before_add = len(product_list)
        response = self.client.post("/api/v1/products", json=payload)
        target_id = response.json
        status_code = response.status_code
        self.assertEqual(status_code, 201)
        response = self.client.get(f"/api/v1/products/{target_id}")
        product = response.json
        status_code = response.status_code
        self.assertIsInstance(product, dict)
        self.assertEqual(status_code, 200)
        response = self.client.get("/api/v1/products")
        product_list = response.json
        nb_product_after_add = len(product_list)
        self.assertEqual(nb_product_after_add, nb_product_before_add + 1)
