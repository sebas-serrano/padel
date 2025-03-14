from sqlalchemy.orm import Session
from app.model.transaction import Transaction
from app.schema.transaction import TransactionCreate
from app.repository.user_repository import UserRepository
from app.database.database import db_instance

class TransactionRepository:
    def __init__(self):
        self.db: Session = db_instance.get_session()
        self.user_repository = UserRepository()

    def get_all_transactions(self):
        return self.db.query(Transaction).filter(Transaction.active == True).all()

    def get_all_transactions_by_user_id(self, user_id: int):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

    def get_transaction_by_id(self, id: int):
        return self.db.query(Transaction).filter(Transaction.id == id).one_or_none()

    def create_transaction(self, transaction_create: TransactionCreate, user_id: int):
        
        created_user = self.user_repository.get_user_by_id(user_id)
        if not created_user:
            return None

        new_transaction = Transaction(
            user_id=user_id,
            user_email=created_user.email,
            description=transaction_create.description,
            date=transaction_create.date,
            tickets=transaction_create.tickets,
            active=True
        )
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction
        

    def delete_transaction(self, transaction_id: int):
    
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            transaction.active = False  # Borrado lógico de la transacción
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
        return None
        