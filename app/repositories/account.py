from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, account_id: int, user_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(
            Account.id == account_id,
            Account.user_id == user_id,
        ).first()
        
    def get_all(self, user_id: int) -> List[Account]:
        return self.db.query(Account).filter(Account.user_id == user_id).all()
    
    def create(self, user_id: int, account: AccountCreate) -> Account:
        db_account = Account(
            user_id = user_id,
            name = account.name,
            balance = account.balance,
            currency = account.currency,
            icon = account.icon,
        )
        
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account
    
    def update(self, account_id: id, user_id: int, account_update: AccountUpdate) -> Optional[Account]:
        db_account = self.get_by_id(account_id, user_id)
        if not db_account:
            return None
        
        if account_update.name is not None:
            db_account.name = account_update.name
        if account_update.balance is not None:
            db_account.balance = account_update.balance
        if account_update.currency is not None:
            db_account.currency = account_update.currency
        if account_update.icon is not None:
            db_account.icon = account_update.icon
            
        self.db.commit()
        self.db.refresh(db_account)
        return db_account
    
    def delete(self, account_id: int, user_id: int) -> bool:
        db_account = self.get_by_id(account_id, user_id)
        if not db_account:
            return False
        
        self.db.delete(db_account)
        self.db.commit()
        
        return True
    
    def update_balance(self, account_id: int, amount: float) -> Optional[Account]:
        db_account = self.db.query(Account).filter(Account.id == account_id).first()
        if not db_account:
            return None
        
        db_account.balance += amount
        self.db.commit()
        self.db.refresh(db_account)
        return db_account