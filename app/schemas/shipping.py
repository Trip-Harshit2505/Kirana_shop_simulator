from pydantic import BaseModel
from typing import Literal


class ShippingChargeResponse(BaseModel):
    shippingCharge: float


class NearestWarehouseResponse(BaseModel):
    warehouseId: int
    warehouseLocation: dict


class ShippingCalculateRequest(BaseModel):
    sellerId: int
    customerId: int
    deliverySpeed: Literal["standard", "express"]


class ShippingCalculateResponse(BaseModel):
    shippingCharge: float
    nearestWarehouse: NearestWarehouseResponse