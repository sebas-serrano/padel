import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schema.user_schema import User, UserCreate
import os
from dotenv import load_dotenv

client = TestClient(app)

load_dotenv()

headers_admin = {"Authorization": os.getenv("ADMIN_TOKEN")}

def test_create_user():
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "firebase_uid": "firebase123",
        "phone_number": "123456789"
    }
    response = client.post("/user/createLoadUser", json=new_user)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == new_user["email"]
    assert user["firebase_uid"] == new_user["firebase_uid"]
    assert isinstance(user["user_id"], int)
    assert isinstance(user["tickets"], int)
    
def test_create_user_no_phone():
    new_user = {
        "name": "Test User2",
        "email": "test2@example.com",
        "firebase_uid": "firebase1234",
    }
    response = client.post("/user/createLoadUser", json=new_user)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == new_user["email"]
    assert user["firebase_uid"] == new_user["firebase_uid"]
    assert isinstance(user["user_id"], int)
    assert isinstance(user["tickets"], int)

def test_get_users():
    response = client.get("/user/getUsers", headers=headers_admin)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    if users:  #Si hay usuarios valido la estructura
        assert "user_id" in users[0]
        assert "tickets" in users[0]
        assert "email" in users[0]

def test_get_user_by_firebase_uid(): #No anda deberia probar un uid real
    firebase_uid = "firebase123"
    response = client.get(f"/user/getUserByFirebaseId/{firebase_uid}")
    assert response.status_code == 200
    user = response.json()
    assert "user_id" in user

def test_get_user_by_id():
    user_id = 1
    response = client.get(f"/user/getUserById/{user_id}", headers=headers_admin)
    assert response.status_code == 200
    user = response.json()
    assert user["user_id"] == user_id
    assert "email" in user

def test_add_tickets():
    transaction_data = {
        "date": "2025-02-27",
        "description": "Prueba",
        "tickets": 10
    }
    firebase_uid = "firebase123"
    response = client.post(f"/user/addTickets/{firebase_uid}", json=transaction_data, headers=headers_admin)
    assert response.status_code == 200
    assert isinstance(response.json(), int)

def test_remove_tickets():
    transaction_data = {
        "date": "2025-02-27",
        "description": "Prueba2",
        "tickets": 5
    }
    user_id = 1
    response = client.post(f"/user/removeTickets/{user_id}", json=transaction_data, headers=headers_admin)
    assert response.status_code == 200
    assert isinstance(response.json(), int)

def test_register_user_by_admin():
    new_user = {
        "name": "Admin Test",
        "email": "admin_test@example.com"
    }
    firebase_uid = "firebase_admin"
    response = client.post(f"/user/registerUserByAdmin/{firebase_uid}", json=new_user, headers=headers_admin)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == new_user["email"]
    assert isinstance(user["user_id"], int)
    
def test_add_phone_number():
    user_id = 2
    phone_data = {"phone_number": "555555555"}
    response = client.post(f"/user/addPhoneNumber/{user_id}", json=phone_data)
    assert response.status_code == 200
    assert response.json()["phone_number"] == phone_data["phone_number"]