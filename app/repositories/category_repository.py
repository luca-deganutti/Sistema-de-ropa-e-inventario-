from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(name=data.name, is_active=data.is_active)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool | None = None,
) -> list[Category]:
    stmt = select(Category).order_by(Category.id.asc()).offset(skip).limit(limit)

    if only_active is True:
        stmt = stmt.where(Category.is_active.is_(True))
    elif only_active is False:
        stmt = stmt.where(Category.is_active.is_(False))

    return list(db.scalars(stmt).all())


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    return cast(Category | None, db.get(Category, category_id))


def get_category_by_name(db: Session, name: str) -> Category | None:
    stmt = select(Category).where(Category.name == name)
    return cast(Category | None, db.scalars(stmt).first())


def update_category(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
