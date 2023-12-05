from sqlalchemy import String, Integer, Float, BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from typing import TYPE_CHECKING

from models.base import Base
from models.match import ProductsMapped

if TYPE_CHECKING:
    from models.product_dealer import ProductDealer


class Product(Base):
    """Customer product model"""

    article: Mapped[str | None] = mapped_column(String(), unique=True)
    ean_13: Mapped[int | None] = mapped_column(BigInteger())
    name: Mapped[str | None] = mapped_column(String())
    cost: Mapped[float | None] = mapped_column(Float())
    recommended_price: Mapped[float | None] = mapped_column(Float())
    category_id: Mapped[int | None] = mapped_column(Integer())
    ozon_name: Mapped[str | None] = mapped_column(String())
    name_1c: Mapped[str | None] = mapped_column(String())
    wb_name: Mapped[str | None] = mapped_column(String())
    ozon_article: Mapped[str | None] = mapped_column(String())
    wb_article: Mapped[str | None] = mapped_column(String())
    ym_article: Mapped[str | None] = mapped_column(String())
    wb_article_td: Mapped[str | None] = mapped_column(String())
    productdealer: Mapped[list["ProductDealer"]] = relationship(
        back_populates="product"
    )
    productsmapped: Mapped["ProductsMapped"] = relationship(
        back_populates="product"
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return self.name
