from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories import category_repository as category_repo
from app.schemas.category import CategoryCreate, CategoryUpdate


def _normalize_name(name: str) -> str:
    return " ".join(name.split()).strip()


def create_category_service(db: Session, data: CategoryCreate) -> Category:
    normalized_name = _normalize_name(data.name)

    existing = category_repo.get_category_by_name(db, normalized_name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )

    payload = data.model_copy(update={"name": normalized_name})
    return category_repo.create_category(db, payload)


def get_categories_by_role(
    db: Session, role: str, skip: int = 0, limit: int = 100
) -> list[Category]:
    role_normalized = role.strip().lower()
    if role_normalized == "admin":
        return category_repo.list_categories(db, skip=skip, limit=limit)
    return category_repo.list_categories(db, skip=skip, limit=limit, only_active=True)


def get_category_service(db: Session, category_id: int) -> Category:
    category = category_repo.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


def update_category_service(
    db: Session,
    category_id: int,
    data: CategoryUpdate,
) -> Category:
    category = get_category_service(db, category_id)
    update_data = data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        normalized_name = _normalize_name(update_data["name"])
        existing = category_repo.get_category_by_name(db, normalized_name)
        if existing is not None and existing.id != category.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category name already exists",
            )
        category.name = normalized_name

    if "is_active" in update_data:
        category.is_active = update_data["is_active"]

    return category_repo.update_category(db, category)


def delete_category_service(db: Session, category_id: int) -> None:
    category = get_category_service(db, category_id)
    if not category.is_active:
        return

    category.is_active = False
    category_repo.update_category(db, category)
