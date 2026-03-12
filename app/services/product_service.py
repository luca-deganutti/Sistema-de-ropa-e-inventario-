from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories import product_repository as product_repo
from app.schemas.product import ProductCreate, ProductUpdate


def create_product_service(db: Session, data: ProductCreate) -> Product:
    existing = product_repo.get_product_by_name(db, data.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product name already exists",
        )
    return product_repo.create_product(db, data)


def update_product_service(
    db: Session, product_id: int, data: ProductUpdate
) -> Product:
    product = product_repo.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product_repo.update_product(db, product, data)


def delete_product_service(db: Session, product_id: int) -> None:
    product = product_repo.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    product_repo.delete_product(db, product)


def get_product_by_id_service(db: Session, product_id: int, role: str) -> Product:
    product = product_repo.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if role.strip().lower() != "admin" and not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


def get_products_service(
    db: Session, role: str, skip: int = 0, limit: int = 100
) -> list[Product]:
    products = product_repo.get_products(db, skip, limit)
    if role.strip().lower() == "admin":
        return products
    return [product for product in products if product.is_active]


def get_products_by_category_service(
    db: Session, category_id: int, role: str, skip: int = 0, limit: int = 100
) -> list[Product]:
    products = product_repo.get_products_by_category(db, category_id, skip, limit)
    if role.strip().lower() == "admin":
        return products
    return [product for product in products if product.is_active]


def get_product_by_name_service(db: Session, name: str, role: str) -> Product:
    product = product_repo.get_product_by_name(db, name)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if role.strip().lower() != "admin" and not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product
