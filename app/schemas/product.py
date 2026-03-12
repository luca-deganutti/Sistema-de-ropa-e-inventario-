from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    category_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    base_price: Decimal = Field(..., gt=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    base_price: Decimal | None = Field(default=None, gt=0)
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
