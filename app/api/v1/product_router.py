# faltaria hacer todo el tema de los roles ya que no tengo users creado hasta el momento,faltaria el get_current_user y todo eso para poder sacar el role del user y hacer las validaciones correspondientes, por ahora lo deje como un parametro que se le pasa a cada funcion pero obviamente no es lo ideal
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product_service as product_srv

router = APIRouter(prefix="/categories", tags=["Categories"])


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
    return product_srv.delete_product_service(db, product_id)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> Product:
    return product_srv.get_product_by_id_service(db, product_id)


@router.get("", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)) -> list[Product]:
    return product_srv.get_products_service(db)


@router.get("/category/{category_id}", response_model=list[ProductRead])
def get_products_by_category(
    category_id: int, db: Session = Depends(get_db)
) -> list[Product]:
    return product_srv.get_products_by_category_service(db, category_id)


@router.get("/name/{name}", response_model=ProductRead)
def get_product_by_name(name: str, db: Session = Depends(get_db)) -> Product:
    return product_srv.get_product_by_name_service(db, name)
