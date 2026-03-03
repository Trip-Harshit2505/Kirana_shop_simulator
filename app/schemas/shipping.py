from pydantic import BaseModel
from typing import Literal

# Schemas for Shipping API

# These schemas define the request and response models for the shipping-related endpoints.
class ShippingChargeResponse(BaseModel):
    shippingCharge: float

# This schema is used for the /shipping-charge endpoint to return the calculated shipping charge based on the provided parameters.
class NearestWarehouseResponse(BaseModel):
    warehouseId: int
    warehouseLocation: dict

# This schema is used for the /shipping-charge/calculate endpoint to return both the calculated shipping charge and the nearest warehouse information.
class ShippingCalculateRequest(BaseModel):
    sellerId: int
    customerId: int
    deliverySpeed: Literal["standard", "express"]

# This schema is used for the /shipping-charge/calculate endpoint to return both the calculated shipping charge and the nearest warehouse information.
class ShippingCalculateResponse(BaseModel):
    shippingCharge: float
    nearestWarehouse: NearestWarehouseResponse