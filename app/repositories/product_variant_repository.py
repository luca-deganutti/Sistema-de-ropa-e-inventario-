from app.db.session import Session
from app.models.product_variant import ProductVariant
from app.schemas.product_variant import (
    ProductVariantCreate,
    ProductVariantUpdate,
)


def create_product_variant(db: Session, data: ProductVariantCreate) -> ProductVariant:
    product_variant = ProductVariant(
        product_id=data.product_id,
        color=data.color,
        size=data.size,
        description=data.description,
        additional_price=data.additional_price,
        is_active=data.is_active,
        stock=data.stock,
    )
    db.add(product_variant)
    db.commit()
    db.refresh(product_variant)
    return product_variant


def update_product_variant(
    db: Session, product_variant: ProductVariant, data: ProductVariantUpdate
) -> ProductVariant:
    if data.product_id is not None:
        product_variant.product_id = data.product_id
    if data.color is not None:
        product_variant.color = data.color
    if data.size is not None:
        product_variant.size = data.size
    if data.description is not None:
        product_variant.description = data.description
    if data.additional_price is not None:
        product_variant.additional_price = data.additional_price
    if data.is_active is not None:
        product_variant.is_active = data.is_active
    if data.stock is not None:
        product_variant.stock = data.stock

    db.add(product_variant)
    db.commit()
    db.refresh(product_variant)
    return product_variant


def delete_product_variant(db: Session, product_variant: ProductVariant) -> None:
    db.delete(product_variant)
    db.commit()


def get_product_variant_by_id(
    db: Session, product_variant_id: int
) -> ProductVariant | None:
    return (
        db.query(ProductVariant).filter(ProductVariant.id == product_variant_id).first()
    )


def get_product_variants(
    db: Session, skip: int = 0, limit: int = 100
) -> list[ProductVariant]:
    return db.query(ProductVariant).offset(skip).limit(limit).all()


def get_product_variant_by_color_and_size(
    db: Session, product_id: int, color: str, size: str
) -> ProductVariant | None:
    return (
        db.query(ProductVariant)
        .filter(
            ProductVariant.product_id == product_id,
            ProductVariant.color == color,
            ProductVariant.size == size,
        )
        .first()
    )


def get_product_variants_by_product_id(
    db: Session, product_id: int, skip: int = 0, limit: int = 100
) -> list[ProductVariant]:
    return (
        db.query(ProductVariant)
        .filter(ProductVariant.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product_variants_by_color_and_size(
    db: Session, product_id: int, color: str, size: str
) -> list[ProductVariant]:
    return (
        db.query(ProductVariant)
        .filter(
            ProductVariant.product_id == product_id,
            ProductVariant.color == color,
            ProductVariant.size == size,
        )
        .all()
    )
