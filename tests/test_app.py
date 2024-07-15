import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from app import app, orders

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_orders(client):
    response = client.get('/api/orders/')
    assert response.status_code == 200
    assert response.json == []

def test_create_order(client):
    new_order = {"item": "Laptop", "quantity": 1}
    response = client.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
    assert response.status_code == 201
    assert response.json['item'] == "Laptop"
    assert response.json['quantity'] == 1

def test_get_order(client):
    new_order = {"item": "Laptop", "quantity": 1}
    client.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
    response = client.get('/api/orders/1')
    assert response.status_code == 200
    assert response.json['item'] == "Laptop"
    assert response.json['quantity'] == 1

def test_update_order(client):
    new_order = {"item": "Laptop", "quantity": 1}
    client.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
    updated_order = {"item": "Laptop", "quantity": 2}
    response = client.put('/api/orders/1', data=json.dumps(updated_order), content_type='application/json')
    assert response.status_code == 200
    assert response.json['quantity'] == 2

def test_delete_order(client):
    new_order = {"item": "Laptop", "quantity": 1}
    client.post('/api/orders/', data=json.dumps(new_order), content_type='application/json')
    response = client.delete('/api/orders/1')
    assert response.status_code == 200
    assert response.json['message'] == "Order deleted"
    response = client.get('/api/orders/1')
    assert response.status_code == 404
