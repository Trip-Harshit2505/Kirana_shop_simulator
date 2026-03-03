from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    length = Column(Float, nullable=False, default=1.0)
    width = Column(Float, nullable=False, default=1.0)
    height = Column(Float, nullable=False, default=1.0)

    seller_id = Column(Integer, ForeignKey("sellers.id"))
    seller = relationship("Seller", back_populates="products")

    # NEW FIELDS (Business Thinking)
    is_fragile = Column(Boolean, default=False)
    is_perishable = Column(Boolean, default=False)
    min_order_quantity = Column(Integer, default=1)