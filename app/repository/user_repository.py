from sqlalchemy.orm import Session
from app.model.user import User
from app.schema.user_schema import UserCreate
from app.database.database import db_instance
from sqlalchemy import or_

class UserRepository:
    def __init__(self):
        self.db: Session = db_instance.get_session()

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_firebase_uid(self, firebase_uid: str):
        return self.db.query(User).filter(
    or_(
        User.firebase_uid == firebase_uid,  
        (User.firebase_uid == None if firebase_uid is None else False))).first()
    
    def save(self, user: UserCreate):
        try:
            user_data = user.model_dump()  
            user_instance = User(**user_data)  
            
            self.db.add(user_instance)
            self.db.commit()
            self.db.refresh(user_instance)
            return user_instance
        except Exception as e:
            self.db.rollback()
            raise e  
    
    def update(self, user: User):
        try:
            self.db.merge(user)  
            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
