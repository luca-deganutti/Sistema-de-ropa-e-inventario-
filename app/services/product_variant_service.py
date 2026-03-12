from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_variant import ProductVariant
from app.repositories import product_variant_repository as variant_repo
from app.schemas.product_variant import ProductVariantCreate, ProductVariantUpdate


def create_product_variant_service(
    db: Session, data: ProductVariantCreate, role: str
) -> ProductVariant:
    if role.strip().lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return variant_repo.create_product_variant(db, data)


def update_product_variant_service(
    db: Session, product_variant_id: int, data: ProductVariantUpdate, role: str
) -> ProductVariant:
    product_variant = variant_repo.get_product_variant_by_id(db, product_variant_id)
    if product_variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    if role.strip().lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return variant_repo.update_product_variant(db, product_variant, data)


def delete_product_variant_service(
    db: Session, product_variant_id: int, role: str
) -> None:
    product_variant = variant_repo.get_product_variant_by_id(db, product_variant_id)
    if product_variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    if role.strip().lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    variant_repo.delete_product_variant(db, product_variant)


def get_product_variant_by_id_service(
    db: Session, product_variant_id: int, role: str
) -> ProductVariant:
    product_variant = variant_repo.get_product_variant_by_id(db, product_variant_id)
    if product_variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    if role.strip().lower() != "admin" and not product_variant.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    return product_variant


def get_product_variants_service(
    db: Session, role: str, skip: int = 0, limit: int = 100
) -> list[ProductVariant]:
    variants = variant_repo.get_product_variants(db, skip, limit)
    if role.strip().lower() == "admin":
        return variants
    return [variant for variant in variants if variant.is_active]


def get_product_variants_by_product_id_service(
    db: Session, product_id: int, role: str, skip: int = 0, limit: int = 100
) -> list[ProductVariant]:
    variants = variant_repo.get_product_variants_by_product_id(
        db, product_id, skip, limit
    )
    if role.strip().lower() == "admin":
        return variants
    return [variant for variant in variants if variant.is_active]


def get_product_variant_by_color_and_size_service(
    db: Session, product_id: int, color: str, size: str, role: str
) -> ProductVariant:
    product_variant = variant_repo.get_product_variant_by_color_and_size(
        db, product_id, color, size
    )
    if product_variant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    if role.strip().lower() != "admin" and not product_variant.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product variant not found",
        )
    return product_variant


def get_product_variants_by_color_and_size_service(
    db: Session, product_id: int, color: str, size: str, role: str
) -> list[ProductVariant]:
    variants = variant_repo.get_product_variants_by_color_and_size(
        db, product_id, color, size
    )
    if role.strip().lower() == "admin":
        return variants
    return [variant for variant in variants if variant.is_active]
