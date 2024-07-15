import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        global orders
        orders = []

    def test_get_orders(self):
        response = self.app.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_order(self):
        new_order = {"item": "Laptop", "quantity": 1}
        response = self.app.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['item'], "Laptop")
        self.assertEqual(response.json['quantity'], 1)

    def test_get_order(self):
        new_order = {"item": "Laptop", "quantity": 1}
        self.app.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
        response = self.app.get('/api/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['item'], "Laptop")
        self.assertEqual(response.json['quantity'], 1)

    def test_update_order(self):
        new_order = {"item": "Laptop", "quantity": 1}
        self.app.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
        updated_order = {"item": "Laptop", "quantity": 2}
        response = self.app.put('/api/orders/1', data=json.dumps(updated_order), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['quantity'], 2)

    def test_delete_order(self):
        new_order = {"item": "Laptop", "quantity": 1}
        self.app.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
        response = self.app.delete('/api/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Order deleted")
        response = self.app.get('/api/orders/1')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
