import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schema.user_schema import User, UserCreate
import os
from dotenv import load_dotenv

client = TestClient(app)

load_dotenv()

headers_admin = {"Authorization": os.getenv("ADMIN_TOKEN")}

def test_create_user(): #Creo un usuario para que sea el creador de un paquete (firebase_uid)
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "firebase_uid": "firebase123",
        "phone_number": "123456789"
    }
    response = client.post("/user/createLoadUser", json=new_user, headers=headers_admin)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == new_user["email"]
    assert user["firebase_uid"] == new_user["firebase_uid"]
    assert isinstance(user["user_id"], int)
    assert isinstance(user["tickets"], int)
    
def test_createPackage():
    new_package = {
        "price": 10,
        "ticket_quantity": 10,
        "title": "PruebaPaquete",
        "description": "PruebaPaquete description",
        "firebase_uid": "firebase123"
    }
    response = client.post("/package/createPackage", json=new_package, headers=headers_admin)
    assert response.status_code == 200
    package = response.json()
    assert package["title"] == new_package["title"]
    assert package["firebase_uid"] == new_package["firebase_uid"]
    assert isinstance(package["package_id"], int)
    assert isinstance(package["ticket_quantity"], int)

def test_get_packages():
    response = client.get("/package/getPackages", headers=headers_admin)
    assert response.status_code == 200
    packages = response.json()
    assert isinstance(packages, list)

def test_updatePackageByID():
    new_package = {
        "price": 10,
        "ticket_quantity": 30,
        "title": "PruebaPaqueteCambio",
        "description": "PruebaPaqueteCambio description",
        "firebase_uid": "firebase123"
    }
    package_id = 1
    response = client.put(f"/package/updatePackageByID/{package_id}", json=new_package, headers=headers_admin)
    assert response.status_code == 200
    package = response.json()
    
def test_deletePackageByID():
    package_id = 1
    response = client.post(f"/package/deletePackageByID/{package_id}", headers=headers_admin)
    assert response.status_code == 200
    package = response.json()