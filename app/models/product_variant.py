from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.product import Product


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    additional_price: Mapped[Numeric] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    product: Mapped[Product] = relationship("Product", back_populates="variants")
