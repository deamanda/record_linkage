from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base


class ProductDealer(Base):
    key: Mapped[int] = mapped_column(Integer())
    product_id: Mapped[int] = mapped_column(Integer())
    dealer_id: Mapped[int] = mapped_column(Integer())
