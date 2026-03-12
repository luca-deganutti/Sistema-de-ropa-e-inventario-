from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product_service as product_srv

router = APIRouter(prefix="/products", tags=["products"])


def get_current_user_role(role: str = Query(default="user")) -> str:
    # Temporary role source until JWT auth is implemented.
    return role


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)) -> Product:
    return product_srv.create_product_service(db, data)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int, data: ProductUpdate, db: Session = Depends(get_db)
) -> Product:
    return product_srv.update_product_service(db, product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    product_srv.delete_product_service(db, product_id)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> Product:
    return product_srv.get_product_by_id_service(db, product_id, role)


@router.get("", response_model=list[ProductRead])
def get_products(
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[Product]:
    return product_srv.get_products_service(db, role, skip, limit)


@router.get("/category/{category_id}", response_model=list[ProductRead])
def get_products_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[Product]:
    return product_srv.get_products_by_category_service(
        db, category_id, role, skip, limit
    )


@router.get("/name/{name}", response_model=ProductRead)
def get_product_by_name(
    name: str,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role),
) -> Product:
    return product_srv.get_product_by_name_service(db, name, role)
