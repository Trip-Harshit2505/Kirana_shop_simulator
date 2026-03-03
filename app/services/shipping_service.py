from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customer import Customer
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.utils.distance import calculate_distance
from app.services.transport_strategy import get_transport_strategy
from app.services.warehouse_service import get_nearest_warehouse
from app.core.cache import cache


def calculate_shipping(
    db: Session,
    warehouse_id: int,
    customer_id: int,
    delivery_speed: str,
    weight: float,
):
    cache_key = f"shipping:{warehouse_id}:{customer_id}:{delivery_speed}:{weight}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    distance = calculate_distance(
        warehouse.latitude,
        warehouse.longitude,
        customer.latitude,
        customer.longitude,
    )

    strategy = get_transport_strategy(distance)
    base_charge = strategy.calculate(distance, weight)

    if delivery_speed == "express":
        final_charge = base_charge + 10 + (weight * 1.2)
    else:
        final_charge = base_charge + 10

    final_charge = round(final_charge, 2)

    cache.set(cache_key, final_charge, ttl=60)

    return final_charge

def calculate_shipping_for_seller(
    db: Session,
    seller_id: int,
    customer_id: int,
    delivery_speed: str,
):
    product = (
        db.query(Product)
        .filter(Product.seller_id == seller_id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="No product found for seller")
    
    if product.is_perishable and delivery_speed != "express":
        raise HTTPException(
            status_code=400,
            detail="Perishable products require express delivery"
        )

    warehouse = get_nearest_warehouse(db, seller_id)

    shipping_charge = calculate_shipping(
        db=db,
        warehouse_id=warehouse.id,
        customer_id=customer_id,
        delivery_speed=delivery_speed,
        weight=product.weight,
    )
    if product.is_fragile:
        shipping_charge += 5

    return warehouse, shipping_charge