from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OperationBase(BaseModel):
    account_id: int
    category_id: int
    amount: float
    description: Optional[str] = None
    operation_date: datetime
    

class OperationCreate(OperationBase):
    pass


class OperationUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    operation_date: Optional[datetime] = None
    
class OperationResponse(OperationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class OperationWithDetails(OperationResponse):
    account_name: str
    category_name: str
    category_type: str