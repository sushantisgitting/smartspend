from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.schemas.operation import OperationCreate, OperationUpdate, OperationResponse, OperationWithDetails
from app.services.operation import OperationService
from app.services.auth import get_current_user_id

router = APIRouter(prefix="/operations", tags=["operations"])


@router.post("/", response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
def create_operation(
    operation: OperationCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    return service.create_operation(current_user_id, operation)


@router.get("/", response_model=List[OperationResponse])
def get_operations(
    account_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    return service.get_all_operations(
        current_user_id,
        account_id,
        category_id,
        start_date,
        end_date
    )


@router.get("/details", response_model=List[OperationWithDetails])
def get_operations_with_details(
    account_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    return service.get_operations_with_details(
        current_user_id,
        account_id,
        category_id,
        start_date,
        end_date
    )


@router.get("/{operation_id}", response_model=OperationResponse)
def get_operation(
    operation_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    return service.get_operation(operation_id, current_user_id)


@router.put("/{operation_id}", response_model=OperationResponse)
def update_operation(
    operation_id: int,
    operation_update: OperationUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    return service.update_operation(operation_id, current_user_id, operation_update)


@router.delete("/{operation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(
    operation_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = OperationService(db)
    service.delete_operation(operation_id, current_user_id)