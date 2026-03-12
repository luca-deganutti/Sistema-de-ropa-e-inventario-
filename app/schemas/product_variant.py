from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantBase(BaseModel):
    product_id: int = Field(..., gt=0)
    color: str = Field(..., min_length=2, max_length=100)
    size: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    additional_price: float = Field(..., ge=0)
    is_active: bool = True
    stock: int = Field(..., ge=0)


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    product_id: int | None = Field(default=None, gt=0)
    color: str | None = Field(default=None, min_length=2, max_length=100)
    size: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    additional_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None
    stock: int | None = Field(default=None, ge=0)


class ProductVariantRead(ProductVariantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
