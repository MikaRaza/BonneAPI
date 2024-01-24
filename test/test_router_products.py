from fastapi.testclient import TestClient
from main import app
from routers.router_auth import secure_endpoint
client = TestClient(app)


def test_create_product():
    product_data = {"name": "Test Product", "price": 19.99}
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    assert "id" in response.json()
    
def test_get_product_by_id():
    existing_product_id = "12345"
    response = client.get(f"/products/{existing_product_id}")
    
def test_modify_product_name():
    existing_product_id = "12345"
    modified_product_data = {"name": "New Test Name", "price": 10.99}
    response = client.patch(f"/products/{existing_product_id}", json=modified_product_data)
    assert response.status_code == 404  
def test_delete_product():
    existing_product_id = "12345"
    response = client.delete(f"/products/{existing_product_id}")
    assert response.status_code == 404 
