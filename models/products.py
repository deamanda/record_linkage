from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    article: Mapped[str] = mapped_column(String(100))
    ean_13: Mapped[int] = mapped_column(Integer())
    cost: Mapped[int] = mapped_column(Integer())
    min_recommended_price: Mapped[int] = mapped_column(Integer())
    recommended_price: Mapped[int] = mapped_column(Integer())
    category_id: Mapped[int] = mapped_column(
        Integer()
    )  # категории мб зависимость one to many
    ozon_name: Mapped[str] = mapped_column(String(100))
    name_1c: Mapped[str] = mapped_column(String(100))
    wb_name: Mapped[str] = mapped_column(String(100))
    ozon_article: Mapped[str] = mapped_column(String(100))
    wb_article: Mapped[str] = mapped_column(String(100))
    ym_article: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return self.name
