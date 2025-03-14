from fastapi import HTTPException
from app.repository.transaction_repository import TransactionRepository
from app.schema.transaction import TransactionCreate

class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository
    
    def get_all_transactions(self):
        return self.transaction_repository.get_all_transactions()
    
    def get_all_transactions_by_user_id(self, user_id: int):
        transaction = self.transaction_repository.get_all_transactions_by_user_id(user_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        return transaction
    
    def get_transaction_by_id(self, transaction_id: int):
        transaction = self.transaction_repository.get_transaction_by_id(transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        return transaction
    
    def create_transaction(self, transaction: TransactionCreate, user_id: int):
        transaction = self.transaction_repository.create_transaction(transaction, user_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transacción no válida")
        return transaction

    def delete_transaction(self, transaction_id: int):
        transaction = self.transaction_repository.delete_transaction(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        return transaction
