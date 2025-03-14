from pydantic import BaseModel

class PackageBase(BaseModel):
    price : float
    ticket_quantity: int
    title : str
    description : str
    firebase_uid : str
    
class PackageCreate(PackageBase):
    pass 

class PackageResponse(PackageBase):
    package_id: int
    active : bool
    
    class Config:
        from_attributes = True