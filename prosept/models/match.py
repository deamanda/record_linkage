from typing import TYPE_CHECKING

from sqlalchemy import Float, ARRAY, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


if TYPE_CHECKING:
    from models.dealers import DealerPrice
    from models.products import Product


class ModelVector(Base):
    """Vectors model (ML)"""

    value = Column(ARRAY(Float()))


class ProductsMapped(Base):
    """Auxiliary matching model"""

    position: Mapped[int] = mapped_column(Integer)
    dealerprice_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("dealerprices.id")
    )
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    dealerprice: Mapped["DealerPrice"] = relationship(
        back_populates="productsmapped"
    )
    product: Mapped["Product"] = relationship(back_populates="productsmapped")
