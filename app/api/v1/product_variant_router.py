from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product_variant import ProductVariant
from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantRead,
    ProductVariantUpdate,
)
from app.services import product_variant_service as variant_service

router = APIRouter(prefix="/product-variants", tags=["product-variants"])


def get_current_user_role(role: str = Query(default="user")) -> str:
    # Temporary role source until JWT auth is implemented.
    return role


@router.post("", response_model=ProductVariantRead, status_code=status.HTTP_201_CREATED)
def create_product_variant(
    data: ProductVariantCreate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariant:
    return variant_service.create_product_variant_service(db, data, role)


@router.put("/{product_variant_id}", response_model=ProductVariantRead)
def update_product_variant(
    product_variant_id: int,
    data: ProductVariantUpdate,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariant:
    return variant_service.update_product_variant_service(
        db, product_variant_id, data, role
    )


@router.delete("/{product_variant_id}", status_code=status.HTTP_204_NO_CONTENT)
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
) -> ProductVariant:
    return variant_service.get_product_variant_by_id_service(
        db, product_variant_id, role
    )


@router.get("", response_model=list[ProductVariantRead])
def get_product_variants(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[ProductVariant]:
    return variant_service.get_product_variants_service(db, role, skip, limit)


@router.get("/product/{product_id}", response_model=list[ProductVariantRead])
def get_product_variants_by_product_id(
    product_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[ProductVariant]:
    return variant_service.get_product_variants_by_product_id_service(
        db, product_id, role, skip, limit
    )


@router.get("/search", response_model=ProductVariantRead)
def get_product_variant_by_color_and_size(
    product_id: int,
    color: str,
    size: str,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> ProductVariant:
    return variant_service.get_product_variant_by_color_and_size_service(
        db, product_id, color, size, role
    )


@router.get("/color-size", response_model=list[ProductVariantRead])
def get_product_variants_by_color_and_size(
    product_id: int,
    color: str,
    size: str,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> list[ProductVariant]:
    return variant_service.get_product_variants_by_color_and_size_service(
        db, product_id, color, size, role
    )
