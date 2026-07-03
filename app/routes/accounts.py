from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.services.account import AccountService
from app.services.auth import get_current_user_id

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.create_account(current_user_id, account)


@router.get("/", response_model=List[AccountResponse])
def get_accounts(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.get_all_accounts(current_user_id)


@router.get("/balance")
def get_total_balance(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.get_total_balance(current_user_id)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.get_account(account_id, current_user_id)


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    return service.update_account(account_id, current_user_id, account_update)


@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    service.delete_account(account_id, current_user_id)