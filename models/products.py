from sqlalchemy import String, Integer, Float, BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base


class Product(Base):
    article: Mapped[str] = mapped_column(String(), nullable=True)
    ean_13: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)
    cost: Mapped[float] = mapped_column(Float(), nullable=True)
    recommended_price: Mapped[float] = mapped_column(Float(), nullable=True)
    category_id: Mapped[int] = mapped_column(
        Integer(), nullable=True
    )  # категории мб зависимость one to many
    ozon_name: Mapped[str] = mapped_column(String(), nullable=True)
    name_1c: Mapped[str] = mapped_column(String(), nullable=True)
    wb_name: Mapped[str] = mapped_column(String(), nullable=True)
    ozon_article: Mapped[str] = mapped_column(String(), nullable=True)
    wb_article: Mapped[str] = mapped_column(String(), nullable=True)
    ym_article: Mapped[str] = mapped_column(String(), nullable=True)
    wb_article_td: Mapped[str] = mapped_column(String(), nullable=True)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return self.name
