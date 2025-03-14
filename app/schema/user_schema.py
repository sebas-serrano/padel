from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    firebase_uid: Optional[str] = None
    phone_number: Optional[str] = None
    
class UserCreate(UserBase):
    pass
        
class User(UserBase):
    user_id: int
    tickets:int
class UserCreateAdmin(BaseModel):
    name: str
    email: str

    
class Config:
        from_attributes = True


