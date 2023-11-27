from sqlalchemy import String, Integer, Float, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


class Product(Base):
    article: Mapped[str | None] = mapped_column(String())
    ean_13: Mapped[int | None] = mapped_column(BigInteger())
    name: Mapped[str | None] = mapped_column(String())
    cost: Mapped[float | None] = mapped_column(Float())
    recommended_price: Mapped[float | None] = mapped_column(Float())
    category_id: Mapped[int | None] = mapped_column(
        Integer()
    )  # категории мб зависимость one to many
    ozon_name: Mapped[str | None] = mapped_column(String())
    name_1c: Mapped[str | None] = mapped_column(String())
    wb_name: Mapped[str | None] = mapped_column(String())
    ozon_article: Mapped[str | None] = mapped_column(String())
    wb_article: Mapped[str | None] = mapped_column(String())
    ym_article: Mapped[str | None] = mapped_column(String())
    wb_article_td: Mapped[str | None] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return self.name
