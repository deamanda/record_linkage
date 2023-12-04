from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint,
    select,
    event,
    DateTime,
    String,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base


if TYPE_CHECKING:
    from models.dealers import Dealer, DealerPrice
    from models.products import Product
    from models.users import User


class ProductDealer(Base):
    key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dealerprices.id"), unique=True
    )
    product_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("products.id")
    )
    dealer_id: Mapped[int] = mapped_column(Integer, ForeignKey("dealers.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    status: Mapped[str] = mapped_column(String, nullable=True)
    dealerprice: Mapped["DealerPrice"] = relationship(
        back_populates="productdealer"
    )
    dealer: Mapped["Dealer"] = relationship(back_populates="productdealer")
    product: Mapped["Product"] = relationship(back_populates="productdealer")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="productdealer")

    __table_args__ = (
        UniqueConstraint("key", "product_id", "dealer_id"),
        CheckConstraint(
            status.in_(["matched", "not matched", "deferred"]),
            name="check_status",
        ),
    )


def set_dealer_id_before_insert(mapper, connection, target):
    from .dealers import DealerPrice

    if target.dealer_id is None and target.key:
        dealer_price = connection.execute(
            select(DealerPrice.dealer_id).where(DealerPrice.id == target.key)
        ).scalar()
        target.dealer_id = dealer_price


event.listen(ProductDealer, "before_insert", set_dealer_id_before_insert)
