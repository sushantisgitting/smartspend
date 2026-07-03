from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from app.repositories.operation import OperationRepository
from app.repositories.account import AccountRepository
from app.repositories.category import CategoryRepository
from app.schemas.operation import OperationCreate, OperationUpdate, OperationResponse, OperationWithDetails
from app.models.category import CategoryType


class OperationService:
    def __init__(self, db: Session):
        self.repo = OperationRepository(db)
        self.account_repo = AccountRepository(db)
        self.category_repo = CategoryRepository(db)

    def create_operation(self, user_id: int, operation: OperationCreate) -> OperationResponse:
        account = self.account_repo.get_by_id(operation.account_id, user_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )

        category = self.category_repo.get_by_id(operation.category_id, user_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        db_operation = self.repo.create(user_id, operation)

        if category.type == CategoryType.EXPENSE:
            self.account_repo.update_balance(operation.account_id, -operation.amount)
        else:  
            self.account_repo.update_balance(operation.account_id, operation.amount)

        return OperationResponse.model_validate(db_operation)

    def get_operation(self, operation_id: int, user_id: int) -> OperationResponse:
        operation = self.repo.get_by_id(operation_id, user_id)
        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operation not found"
            )
        return OperationResponse.model_validate(operation)

    def get_all_operations(
        self,
        user_id: int,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[OperationResponse]:
        operations = self.repo.get_all(user_id, account_id, category_id, start_date, end_date)
        return [OperationResponse.model_validate(op) for op in operations]

    def get_operations_with_details(
        self,
        user_id: int,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[OperationWithDetails]:
        results = self.repo.get_with_details(user_id, account_id, category_id, start_date, end_date)
        return [
            OperationWithDetails(
                **OperationResponse.model_validate(op).model_dump(),
                account_name=acc_name,
                category_name=cat_name,
                category_type=cat_type.value
            )
            for op, acc_name, cat_name, cat_type in results
        ]

    def update_operation(
        self,
        operation_id: int,
        user_id: int,
        operation_update: OperationUpdate
    ) -> OperationResponse:
        old_operation = self.repo.get_by_id(operation_id, user_id)
        if not old_operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operation not found"
            )

        old_category = self.category_repo.get_by_id(old_operation.category_id, user_id)

        if old_category.type == CategoryType.EXPENSE:
            self.account_repo.update_balance(old_operation.account_id, old_operation.amount)
        else:
            self.account_repo.update_balance(old_operation.account_id, -old_operation.amount)

        updated_operation = self.repo.update(operation_id, user_id, operation_update)

        new_account_id = operation_update.account_id or old_operation.account_id
        new_category_id = operation_update.category_id or old_operation.category_id
        new_amount = operation_update.amount or old_operation.amount

        new_category = self.category_repo.get_by_id(new_category_id, user_id)
        if new_category.type == CategoryType.EXPENSE:
            self.account_repo.update_balance(new_account_id, -new_amount)
        else:
            self.account_repo.update_balance(new_account_id, new_amount)

        return OperationResponse.model_validate(updated_operation)

    def delete_operation(self, operation_id: int, user_id: int) -> bool:
        operation = self.repo.get_by_id(operation_id, user_id)
        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Operation not found"
            )

        category = self.category_repo.get_by_id(operation.category_id, user_id)
        
        if category.type == CategoryType.EXPENSE:
            self.account_repo.update_balance(operation.account_id, operation.amount)
        else:
            self.account_repo.update_balance(operation.account_id, -operation.amount)

        self.repo.delete(operation_id, user_id)
        return True