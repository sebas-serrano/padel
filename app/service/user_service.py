from fastapi import HTTPException
from app.repository.user_repository import UserRepository
from app.repository.package_repository import PackageRepository
from app.repository.transaction_repository import TransactionRepository
from app.schema.transaction import TransactionCreate
from app.schema.user_schema import UserCreate, UserCreateAdmin
from datetime import date

class UserService:
    def __init__(self, user_repository: UserRepository, package_repository : PackageRepository, transaction_repository: TransactionRepository): 
        self.user_repository = user_repository
        self.package_repository = package_repository
        self.transaction_repository = transaction_repository
        
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    
    def get_user_by_firebase_uid(self, firebase_uid: str):
        user = self.user_repository.get_user_by_firebase_uid(firebase_uid)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    
    def log_user(self, user : dict):
        existing_user = self.user_repository.get_user_by_firebase_uid(user.get("uid"))

        if existing_user:
            return existing_user

        new_user = UserCreate(name=user.get("email").split("@")[0], email=user.get("email"), firebase_uid=user.get("uid"))
        return self.user_repository.save(new_user)

    def create_load_user(self, user: UserCreate):
        print (f"UserCreate: {user}")
        existing_user = self.user_repository.get_user_by_firebase_uid(user.firebase_uid)
        
        if existing_user:
            return existing_user
        
        user_email = self.user_repository.get_user_by_email(user.email)
        
        if user_email:
            if user_email.firebase_uid == None:
                user_email.firebase_uid = user.firebase_uid
                self.user_repository.update(user_email)
            return user_email 
        
        
        try:
            user = self.user_repository.save(user) 
            return user
        except Exception as e:
            self.db.rollback()  # Revertir cambios en caso de error
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    def get_user_by_email(self, email: str):
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    
    def add_tickets(self, firebase_uid: str, transaction_create: TransactionCreate):
        if transaction_create.tickets <= 0:
            raise HTTPException(
                status_code=400,
                detail="El número de tickets debe ser mayor que 0"
            )
        try:
            user = self.get_user_by_firebase_uid(firebase_uid)
                
            user.tickets += transaction_create.tickets
            updated_user = self.user_repository.update(user)
            transaction_create.date = datetime.now().date()

            new_transaction = self.transaction_repository.create_transaction(transaction_create, updated_user.user_id)
            
            if not new_transaction:
                raise HTTPException(
                    status_code=500,
                    detail="Error al crear transacción"
                )
            
            return user.tickets
                
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al agregar tickets: {str(e)}"
            )

    def remove_tickets(self, user_id: int, transaction_create: TransactionCreate):
        if transaction_create.tickets <= 0:
            raise HTTPException(
                status_code=400,
                detail="El número de tickets a restar debe ser mayor que 0"
            )

        user = self.get_user_by_id(user_id)
        if user.tickets < transaction_create.tickets:
            raise HTTPException(
                status_code=400,
                detail="No tienes suficientes tickets para consumir, debes comprar más tickets"
            )
        try:
            user.tickets -= transaction_create.tickets
            updated_user = self.user_repository.update(user)
            transaction_create.date = datetime.now().date()

            new_transaction = self.transaction_repository.create_transaction(transaction_create, updated_user.user_id)
            
            if not new_transaction:
                self.db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail="Error al crear transacción"
                )
            return user.tickets
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al quitar tickets: {str(e)}")
        
    def create_package(self, firebase_uid: str, ticket_quantity: int):
        user = self.get_user_by_firebase_uid(firebase_uid)
        self.package_repository.create_package(user.user_id, ticket_quantity)
        self.user_repository.update(user)
        return user
    
    def get_user_packages(self, firebase_uid: str):
        user = self.get_user_by_firebase_uid(firebase_uid)
        return self.package_repository.get_user_packages(user.user_id)
    
    def register_user_by_admin(self, user: UserCreateAdmin):
            existing_user = self.user_repository.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="El usuario ya existe")
            try:
                user = self.user_repository.save(user)
                return user
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    def set_user_phone(self, user_id: int, phone_number: str):
        user = self.user_repository.get_user_by_id(user_id)
        user.phone_number = phone_number
        self.user_repository.update(user)
        return user
    