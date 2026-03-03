from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    operational_status = Column(String, default="active")