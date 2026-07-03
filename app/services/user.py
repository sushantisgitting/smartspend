from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.auth import AuthService


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.auth_service = AuthService()
        
    def create_user(self, user: UserCreate) -> UserResponse:
        if self.repo.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if self.repo.get_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
            
        hashed_password = self.auth_service.get_password_hash(user.password)
        db_user = self.repo.create(user, hashed_password)
        return UserResponse.model_validate(db_user)
    
    def authenticate_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not self.auth_service.verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_user(self, user_id: int) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        if user_update.email:
            existing = self.repo.get_by_email(user_update.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        if user_update.username:
            existing = self.repo.get_by_username(user_update.username)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        hashed_password = None
        if user_update.password:
            hashed_password = self.auth_service.get_password_hash(user_update.password)

        user = self.repo.update(user_id, user_update, hashed_password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)
    
    def delete_user(self, user_id: int) -> bool:
        if not self.repo.delete(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return True