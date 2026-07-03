from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AccountBase(BaseModel):
    name: str
    currency: str = "KGS"
    icon: str
    
    
class AccountCreate(AccountBase):
    balance: float = 0.0
    
    
class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[str] = None
    currency: Optional[str] = None
    icon: Optional[str] = None
    
class AccountResponse(AccountBase):
    id: int
    user_id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
