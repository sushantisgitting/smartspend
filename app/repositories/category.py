from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict
from datetime import datetime

from app.models.category import Category, CategoryType
from app.models.operation import Operation
from app.schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, categoty_id: int, user_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(
            Category.id == categoty_id,
            Category.user_id == user_id,
        ).first()
        
    def get_all(self, user_id: int, category_type: Optional[CategoryType] = None) -> List[Category]:
        query = self.db.query(Category).filter(Category.user_id == user_id)
        if category_type:
            query = query.filter(Category.type == category_type)
        return query.all()
    
    def get_with_balances(self, user_id: int, category_type: Optional[CategoryType] = None) -> List[Dict]:
        query = self.db.query(
            Category,
            func.coalesce(func.sum(Operation.amount), 0).label('total_amount')).outerjoin(Operation).filter(Category.user_id == user_id
        )
            
        if category_type:
            query = query.filter(Category.type == category_type)
        
        query = query.group_by(Category.id)
        return query.all()
    
    def create(self, user_id: int, category: CategoryCreate) -> Category:
        db_category = Category(
            user_id = user_id,
            name = category.name,
            type = category.type,
            icon = category.icon,
            color = category.color,
        )
        
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def update(self, category_id: int, user_id: int, category_update: CategoryUpdate) -> Optional[Category]:
        db_category = self.get_by_id(category_id, user_id)
        if not db_category:
            return None
        
        if category_update.name is not None:
            db_category.name = category_update.name
        if category_update.type is not None:
            db_category.type == category_update.type
        if category_update.icon is not None:
            db_category.icon == category_update.icon
        if category_update.color is not None:
            db_category.color = category_update.color
            
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def delete(self, category_id: int, user_id: int) -> bool:
        db_category = self.get_by_id(category_id, user_id)
        if not db_category:
            return False
        self.db.delete(db_category)
        self.db.commit()
        return True