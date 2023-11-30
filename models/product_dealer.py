from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    Integer,
    ForeignKey,
    Column,
    UniqueConstraint,
    select,
    event,
    DateTime,
    func,
    Boolean,
)
from sqlalchemy.orm import Mapped, relationship

from models import Base


if TYPE_CHECKING:
    from models.dealers import Dealer, DealerPrice
    from models.products import Product


class ProductDealer(Base):
    key: Mapped[int] = Column(
        Integer, ForeignKey("dealerprices.id"), unique=True
    )
    product_id: Mapped[int | None] = Column(Integer, ForeignKey("products.id"))
    dealer_id: Mapped[int] = Column(Integer, ForeignKey("dealers.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=func.now())
    status: Mapped[bool | None] = Column(Boolean())
    dealerprice: Mapped["DealerPrice"] = relationship(
        back_populates="productdealer"
    )
    dealer: Mapped["Dealer"] = relationship(back_populates="productdealer")
    product: Mapped["Product"] = relationship(back_populates="productdealer")
    __table_args__ = (UniqueConstraint("key", "product_id", "dealer_id"),)


def set_dealer_id_before_insert(mapper, connection, target):
    from .dealers import DealerPrice

    if target.dealer_id is None and target.key:
        dealer_price = connection.execute(
            select(DealerPrice.dealer_id).where(DealerPrice.id == target.key)
        ).scalar()
        target.dealer_id = dealer_price


event.listen(ProductDealer, "before_insert", set_dealer_id_before_insert)
