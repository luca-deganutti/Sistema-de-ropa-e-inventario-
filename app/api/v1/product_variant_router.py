from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantRead,
    ProductVariantUpdate,
)
from app.services import product_variant_service as variant_service

router = APIRouter(prefix="/product-variants", tags=["Product Variants"])


router.post("", response_model=ProductVariantRead)


def create_product_variant(
    data: ProductVariantCreate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariantRead:
    variant = variant_service.create_product_variant_service(db, data, role)
    return ProductVariantRead.from_orm(variant)


@router.put("/{product_variant_id}", response_model=ProductVariantRead)
def update_product_variant(
    product_variant_id: int,
    data: ProductVariantUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariantRead:
    variant = variant_service.update_product_variant_service(
        db, product_variant_id, data, role
    )
    return ProductVariantRead.from_orm(variant)


@router.delete("/{product_variant_id}")
def delete_product_variant(
    product_variant_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> None:
    variant_service.delete_product_variant_service(db, product_variant_id, role)


@router.get("/{product_variant_id}", response_model=ProductVariantRead)
def get_product_variant_by_id(
    product_variant_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariantRead:
    variant = variant_service.get_product_variant_by_id_service(
        db, product_variant_id, role
    )
    return ProductVariantRead.from_orm(variant)


@router.get("", response_model=list[ProductVariantRead])
def get_product_variants(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = 0,
    limit: int = 100,
) -> list[ProductVariantRead]:
    variants = variant_service.get_product_variants_service(db, role, skip, limit)
    return [ProductVariantRead.from_orm(variant) for variant in variants]


@router.get("/product/{product_id}", response_model=list[ProductVariantRead])
def get_product_variants_by_product_id(
    product_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = 0,
    limit: int = 100,
) -> list[ProductVariantRead]:
    variants = variant_service.get_product_variants_by_product_id_service(
        db, product_id, role, skip, limit
    )
    return [ProductVariantRead.from_orm(variant) for variant in variants]


@router.get("/search", response_model=ProductVariantRead)
def get_product_variant_by_color_and_size(
    product_id: int,
    color: str,
    size: str,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariantRead:
    variant = variant_service.get_product_variant_by_color_and_size_service(
        db, product_id, color, size, role
    )
    return ProductVariantRead.from_orm(variant)


@router.get("/color-size", response_model=list[ProductVariantRead])
def get_product_variants_by_color_and_size(
    product_id: int,
    color: str,
    size: str,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = 0,
    limit: int = 100,
) -> list[ProductVariantRead]:
    variants = variant_service.get_product_variants_by_color_and_size_service(
        db, product_id, color, size, role, skip, limit
    )
    return [ProductVariantRead.from_orm(variant) for variant in variants]
