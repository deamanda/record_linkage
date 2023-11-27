from sqlalchemy import String, Float, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from models.base import Base
from datetime import date


class Dealer(Base):
    name: Mapped[str] = mapped_column(String())
    dealerprice: Mapped[list["DealerPrice"]] = relationship(
        back_populates="dealer"
    )

    def __repr__(self) -> str:
        return f"Dealer(id={self.id!r}, name={self.name!r})"

    def __str__(self) -> str:
        return self.name


class DealerPrice(Base):
    product_key: Mapped[str | None] = mapped_column(String())
    price: Mapped[float | None] = mapped_column(Float())
    product_url: Mapped[str | None] = mapped_column(String())
    product_name: Mapped[str | None] = mapped_column(String())
    date: Mapped[date | None] = mapped_column(Date())
    mapped: Mapped[bool | None] = mapped_column(Boolean(), default=None)
    dealer_id: Mapped[int | None] = mapped_column(ForeignKey("dealers.id"))
    dealer: Mapped["Dealer"] = relationship(back_populates="dealerprice")

    def __repr__(self) -> str:
        return f"Dealer(id={self.id!r}, name={self.product_name!r})"

    def __str__(self) -> str:
        return self.product_name
