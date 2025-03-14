from pydantic import BaseModel
from datetime import date
    
class TransactionBase(BaseModel):
    description: str
    tickets: int
    
class TransactionCreate(TransactionBase):
    pass

class TransactionSchema(TransactionBase):
    id: int
    active: bool
    user_id: int
    user_email: str
    tickets: int
    date: date
    
    class Config:
        from_attributes = True