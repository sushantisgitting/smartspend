from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, date

from app.models.operation import Operation
from app.models.account import Account
from app.models.category import Category, CategoryType
from app.schemas.operation import OperationCreate, OperationUpdate


class OperationRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, operation_id: int, user_id: int) -> Optional[Operation]:
        return self.db.query(Operation).filter(
            Operation.id == operation_id,
            Operation.user_id == user_id,
        ).first()
        
    def get_all(
        self,
        user_id: int,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Operation]:
        query = self.db.query(Operation).filter(Operation.user_id == user_id)
        
        if account_id:
            query = query.filter(Operation.account_id == account_id)
        if category_id:
            query = query.filter(Operation.category_id == category_id)
        if start_date:
            query = query.filter(Operation.operation_date >= start_date)
        if end_date:
            query = query.filter(Operation.operation_date <= end_date)
            
        return query.order_by(Operation.operation_date.desc()).all()
    
    def get_with_details(
        self,
        user_id: int,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[tuple]:
        query = self.db.query(
            Operation,
            Account.name.label('account_name'),
            Category.name.label('category_name'),
            Category.type.label('category_type')
        ).join(Account).join(Category).filter(Operation.user_id == user_id)
        
        if account_id:
            query = query.filter(Operation.account_id == account_id)
        if category_id:
            query = query.filter(Operation.category_id == category_id)
        if start_date:
            query = query.filter(Operation.operation_date >= start_date)
        if end_date:
            query = query.filter(Operation.operation_date <= end_date)
        
        return query.order_by(Operation.operation_date.desc()).all()
    
    def create(self, user_id: int, operation: OperationCreate) -> Operation:
        db_operation = Operation(
            user_id = user_id,
            account_id = operation.account_id,
            category_id = operation.category_id,
            amount = operation.amount,
            description = operation.description,
            operation_date = operation.operation_date or datetime.utcnow()
        )
        
        self.db.add(db_operation)
        self.db.commit()
        self.db.refresh(db_operation)
        return db_operation
    
    def update(self, operation_id: int, user_id: int, operation_update: OperationUpdate) -> Optional[Operation]:
        db_operation = self.get_by_id(operation_id, user_id)
        if not db_operation:
            return None

        if operation_update.account_id is not None:
            db_operation.account_id = operation_update.account_id
        if operation_update.category_id is not None:
            db_operation.category_id = operation_update.category_id
        if operation_update.amount is not None:
            db_operation.amount = operation_update.amount
        if operation_update.description is not None:
            db_operation.description = operation_update.description
        if operation_update.operation_date is not None:
            db_operation.operation_date = operation_update.operation_date

        self.db.commit()
        self.db.refresh(db_operation)
        return db_operation

    def delete(self, operation_id: int, user_id: int) -> Optional[Operation]:
        db_operation = self.get_by_id(operation_id, user_id)
        if not db_operation:
            return False
        self.db.delete(db_operation)
        self.db.commit()
        return db_operation