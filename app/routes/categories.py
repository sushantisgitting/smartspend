from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithBalance
from app.services.category import CategoryService
from app.services.auth import get_current_user_id
from app.models.category import CategoryType

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.create_category(current_user_id, category)


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    category_type: Optional[CategoryType] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_all_categories(current_user_id, category_type)


@router.get("/with-balances", response_model=List[CategoryWithBalance])
def get_categories_with_balances(
    category_type: Optional[CategoryType] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_categories_with_balances(current_user_id, category_type)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.get_category(category_id, current_user_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    return service.update_category(category_id, current_user_id, category_update)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CategoryService(db)
    service.delete_category(category_id, current_user_id)