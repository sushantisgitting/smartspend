from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models.category import CategoryType


class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    icon: str
    color: Optional[str]
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    

class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        

class CategoryWithBalance(CategoryResponse):
    total_amount: float