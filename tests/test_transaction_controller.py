from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

config = dotenv_values()

client = TestClient(app)
header_admin = {"Authorization": os.getenv("ADMIN_TOKEN") or config.get("ADMIN_TOKEN")}

def test_create_user(): #Creo un usuario para que sea el creador de un paquete (firebase_uid)
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "firebase_uid": "firebase123",
        "phone_number": "123456789"
    }
    response = client.post("/user/createLoadUser", json=new_user, headers=header_admin)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == new_user["email"]
    assert user["firebase_uid"] == new_user["firebase_uid"]
    assert isinstance(user["user_id"], int)
    assert isinstance(user["tickets"], int)

def test_create_transaction():
    transaction_create = { "date" : "2025-02-28", "description":"test_create", "tickets":5 }
    user_id = 1
    response = client.post(f"/transaction/createTransaction/{user_id}", json=transaction_create, headers=header_admin)
    assert response.status_code == 200
    transaction = response.json()
    assert "id" in transaction

def test_get_transactions():
    response = client.get("/transaction/getTransactions", headers=header_admin)
    assert response.status_code == 200
    transactions = response.json()
    assert isinstance(transactions, list)

def test_get_transaction_by_id():
    transaction_id = 1
    response = client.get(f"/transaction/getTransactionById/{transaction_id}", headers=header_admin)
    assert response.status_code == 200
    transaction = response.json()
    assert "id" in transaction

def test_get_transactions_by_user():
    user_id = 1
    response = client.get(f"/transaction/getTransactionsByUserId/{user_id}", headers=header_admin)
    assert response.status_code == 200
    transactions_by_user = response.json()
    assert isinstance(transactions_by_user, list)

def test_delete_transaction():
    transaction_id = 1
    response = client.post(f"/transaction/deleteTransactionById/{transaction_id}", headers=header_admin)
    assert response.status_code == 200