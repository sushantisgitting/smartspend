from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithBalance
from app.models.category import CategoryType


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create_category(self, user_id: int, category: CategoryCreate) -> CategoryResponse:
        db_category = self.repo.create(user_id, category)
        return CategoryResponse.model_validate(db_category)

    def get_category(self, category_id: int, user_id: int) -> CategoryResponse:
        category = self.repo.get_by_id(category_id, user_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse.model_validate(category)

    def get_all_categories(
        self, 
        user_id: int, 
        category_type: Optional[CategoryType] = None
    ) -> List[CategoryResponse]:
        categories = self.repo.get_all(user_id, category_type)
        return [CategoryResponse.model_validate(cat) for cat in categories]

    def get_categories_with_balances(
        self,
        user_id: int,
        category_type: Optional[CategoryType] = None
    ) -> List[CategoryWithBalance]:
        results = self.repo.get_with_balances(user_id, category_type)
        return [
            CategoryWithBalance(
                **CategoryResponse.model_validate(cat).model_dump(),
                total_amount=float(total)
            )
            for cat, total in results
        ]

    def update_category(
        self, 
        category_id: int, 
        user_id: int, 
        category_update: CategoryUpdate
    ) -> CategoryResponse:
        category = self.repo.update(category_id, user_id, category_update)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse.model_validate(category)

    def delete_category(self, category_id: int, user_id: int) -> bool:
        if not self.repo.delete(category_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return True