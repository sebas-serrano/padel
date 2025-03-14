from fastapi import APIRouter, Depends, Body
from typing import List
from app.schema.user_schema import User as UserSchema, UserCreate, UserCreateAdmin
from app.service.user_service import UserService
from app.repository.user_repository import UserRepository
from app.repository.package_repository import PackageRepository
from app.repository.transaction_repository import TransactionRepository
from app.schema.transaction import TransactionCreate
from app.auth.auth import verify_admin, verify_user
from app.dynatrace_client import enviar_metrica

router = APIRouter()
user_repository = UserRepository() 
package_repository = PackageRepository() # Instancia de UserRepository
transaction_repository = TransactionRepository() # Instancia de UserRepository
user_service = UserService(user_repository, package_repository, transaction_repository)  # Inyección de dependencias


@router.get("/getUsers", dependencies=[Depends(verify_admin)], response_model=List[UserSchema])
def get_users():
    enviar_metrica("usuarios.consultados", 1, "count")
    return user_service.get_all_users()



@router.get("/getUsers2", response_model=List[UserSchema])
def get_users():
    enviar_metrica("usuarios.consultados", 1, "count")
    return user_service.get_all_users()

@router.get("/getUserByFirebaseId/{firebase_uid}", response_model=UserSchema)
def get_user_by_firebase_uid(firebase_uid: str):
    user = user_service.get_user_by_firebase_uid(firebase_uid)
    return user

@router.get("/getUserById/{id}", dependencies=[Depends(verify_admin)],  response_model=UserSchema)
def get_user_by_id(id: int):
    user = user_service.get_user_by_id(id)
    return user

@router.post("/logUser")
def log_user(user = Depends(verify_user)):
    return user_service.log_user(user)

@router.post("/createLoadUser", response_model=UserSchema)
def create_user(user: UserCreate):
    return user_service.create_load_user(user)

@router.get("/getUserByEmail/{email}", dependencies=[Depends(verify_user)], response_model=UserSchema)
def get_user_by_email(email: str):
    user = user_service.get_user_by_email(email)
    return user

# Metodo solo para admin
@router.post("/addTickets/{firebase_uid}",dependencies = [Depends(verify_user)], response_model=int)
def add_tickets(firebase_uid: str, transaction_create: TransactionCreate):
    return user_service.add_tickets(firebase_uid, transaction_create)

# Metodo solo para admin
@router.post("/removeTickets/{user_id}", response_model=int)
def remove_tickets(user_id: int, transaction_create: TransactionCreate,  admin = Depends(verify_admin)):
    return user_service.remove_tickets(user_id, transaction_create)

#Metodo solo para admin
@router.post("/registerUserByAdmin", response_model=UserSchema)
def register_user_by_admin(user: UserCreateAdmin, admin = Depends(verify_admin)):
    return user_service.register_user_by_admin(user)

@router.post("/addPhoneNumber/{user_id}", response_model=UserSchema)
def add_phone_number(user_id: int, phone_number: str = Body(..., embed=True)):
    return user_service.set_user_phone(user_id, phone_number)