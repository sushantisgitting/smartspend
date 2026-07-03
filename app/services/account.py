from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.repositories.account import AccountRepository
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse


class AccountService:
    def __init__(self, db: Session):
        self.repo = AccountRepository(db)

    def create_account(self, user_id: int, account: AccountCreate) -> AccountResponse:
        db_account = self.repo.create(user_id, account)
        return AccountResponse.model_validate(db_account)

    def get_account(self, account_id: int, user_id: int) -> AccountResponse:
        account = self.repo.get_by_id(account_id, user_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return AccountResponse.model_validate(account)

    def get_all_accounts(self, user_id: int) -> List[AccountResponse]:
        accounts = self.repo.get_all(user_id)
        return [AccountResponse.model_validate(acc) for acc in accounts]

    def update_account(self, account_id: int, user_id: int, account_update: AccountUpdate) -> AccountResponse:
        account = self.repo.update(account_id, user_id, account_update)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return AccountResponse.model_validate(account)

    def delete_account(self, account_id: int, user_id: int) -> bool:
        if not self.repo.delete(account_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        return True

    def get_total_balance(self, user_id: int) -> dict:
        accounts = self.repo.get_all(user_id)
        total_balance = sum(acc.balance for acc in accounts)
        return {
            "total_balance": total_balance,
            "currency": "KGS"  
        }