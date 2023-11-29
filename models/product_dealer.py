from sqlalchemy import (
    Integer,
    ForeignKey,
    Column,
    UniqueConstraint,
    select,
    event,
)
from sqlalchemy.orm import Mapped

from models import Base, DealerPrice


class ProductDealer(Base):
    __tablename__ = "productdealerkey"

    key: Mapped[int] = Column(Integer, ForeignKey("dealerprices.id"))
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"))
    dealer_id: Mapped[int] = Column(Integer, ForeignKey("dealers.id"))

    __table_args__ = (UniqueConstraint("key", "product_id", "dealer_id"),)


def set_dealer_id_before_insert(mapper, connection, target):
    if target.dealer_id is None and target.key:
        dealer_price = connection.execute(
            select(DealerPrice.dealer_id).where(DealerPrice.id == target.key)
        ).scalar()
        target.dealer_id = dealer_price


event.listen(ProductDealer, "before_insert", set_dealer_id_before_insert)
