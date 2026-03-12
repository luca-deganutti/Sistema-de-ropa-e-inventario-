from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(name=data.name, price=data.price, category_id=data.category_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, data: ProductUpdate) -> Product:
    if data.name is not None:
        product.name = data.name
    if data.base_price is not None:
        product.base_price = data.base_price
    if data.category_id is not None:
        product.category_id = data.category_id
    if data.is_active is not None:
        product.is_active = data.is_active
    if data.description is not None:
        product.description = data.description

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def get_products_by_category(
    db: Session, category_id: int, skip: int = 0, limit: int = 100
) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.category_id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product_by_name(db: Session, name: str) -> Product | None:
    return db.query(Product).filter(Product.name == name).first()
