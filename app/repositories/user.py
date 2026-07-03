from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email = user.email,
            username = user.username,
            hashed_password = hashed_password,
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user_update: UserUpdate, hashed_password: Optional[str] = None) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.username is not None:
            db_user.username = user_update.username
        if hashed_password is not None:
            db_user.hashed_password = hashed_password
            
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        
        return True