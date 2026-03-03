from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.shipping_service import calculate_shipping
from app.schemas.shipping import ShippingChargeResponse
from app.schemas.shipping import (
    ShippingCalculateRequest,
    ShippingCalculateResponse,
)
from app.services.shipping_service import calculate_shipping_for_seller

router = APIRouter(prefix="/api/v1", tags=["Shipping"])

# Shipping API Endpoints:

# 1. GET /shipping-charge: Calculate shipping charge based on warehouse, customer, delivery
@router.get("/shipping-charge", response_model=ShippingChargeResponse)
def get_shipping_charge(
    warehouseId: int,
    customerId: int,
    deliverySpeed: str,
    db: Session = Depends(get_db),
):
    weight = 5.0

    charge = calculate_shipping(
        db,
        warehouseId,
        customerId,
        deliverySpeed,
        weight,
    )

    return {"shippingCharge": charge}

@router.post(
    "/shipping-charge/calculate",
    response_model=ShippingCalculateResponse,
)

# 2. POST /shipping-charge/calculate: Calculate shipping charge based on seller, customer, and delivery speed, and also return nearest warehouse information.
def calculate_combined_shipping(
    request: ShippingCalculateRequest,
    db: Session = Depends(get_db),
):
    warehouse, charge = calculate_shipping_for_seller(
        db=db,
        seller_id=request.sellerId,
        customer_id=request.customerId,
        delivery_speed=request.deliverySpeed,
    )

    return {
        "shippingCharge": charge,
        "nearestWarehouse": {
            "warehouseId": warehouse.id,
            "warehouseLocation": {
                "lat": warehouse.latitude,
                "long": warehouse.longitude,
            },
        },
    }