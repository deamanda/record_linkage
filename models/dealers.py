from sqlalchemy import String, Integer, Float, ForeignKey, Date
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
    product_key: Mapped[int] = mapped_column(Integer(), nullable=True)
    price: Mapped[float] = mapped_column(Float(), nullable=True)
    product_url: Mapped[str] = mapped_column(String(), nullable=True)
    product_name: Mapped[str] = mapped_column(String(), nullable=True)
    date: Mapped[date] = mapped_column(Date(), nullable=True)
    dealer_id: Mapped[int] = mapped_column(
        ForeignKey("dealers.id"), nullable=True
    )
    dealer: Mapped["Dealer"] = relationship(back_populates="dealerprice")

    def __repr__(self) -> str:
        return f"Dealer(id={self.id!r}, name={self.product_name!r})"

    def __str__(self) -> str:
        return self.product_name
