from sqlalchemy import (
    Integer,
    ForeignKey,
    Column,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped

from models import Base


class ProductDealer(Base):
    __tablename__ = "productdealerkey"

    key: Mapped[int] = Column(Integer, ForeignKey("dealerprices.id"))
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"))
    dealer_id: Mapped[int] = Column(Integer, ForeignKey("dealers.id"))

    # Добавляем UniqueConstraint для уникальной комбинации ключей
    __table_args__ = (UniqueConstraint("key", "product_id", "dealer_id"),)
