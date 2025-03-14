from fastapi import APIRouter, Depends
from typing import List
from app.schema.transaction import TransactionSchema, TransactionCreate
from app.service.transaction_service import TransactionService
from app.repository.transaction_repository import TransactionRepository
from app.auth.auth import verify_admin, verify_user

router = APIRouter()
transaction_repository = TransactionRepository()
transaction_service = TransactionService(transaction_repository)  # Inyección de dependencias

@router.get("/getTransactions", dependencies=[Depends(verify_admin)], response_model=List[TransactionSchema])
def get_transactions():
    return transaction_service.get_all_transactions()

@router.get("/getTransactionById/{transaction_id}", dependencies=[Depends(verify_admin)], response_model=TransactionSchema)
def get_transaction_by_id(transaction_id: int):
    return transaction_service.get_transaction_by_id(transaction_id)

@router.get("/getTransactionsByUserId/{user_id}", dependencies=[Depends(verify_user)], response_model=List[TransactionSchema])
def get_transactions_by_user_id(user_id: int):
    return transaction_service.get_all_transactions_by_user_id(user_id)

@router.post("/createTransaction/{user_id}", dependencies=[Depends(verify_admin)], response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate, user_id: int):
    return transaction_service.create_transaction(transaction, user_id)

@router.post("/deleteTransactionById/{transaction_id}", dependencies=[Depends(verify_admin)], response_model=TransactionSchema)
def delete_transaction(transaction_id: int):
    return transaction_service.delete_transaction(transaction_id)
