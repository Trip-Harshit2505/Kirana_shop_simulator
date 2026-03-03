from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customer import Customer
from app.models.warehouse import Warehouse
from app.models.product import Product
from app.utils.distance import calculate_distance
from app.services.transport_strategy import get_transport_strategy
from app.services.warehouse_service import get_nearest_warehouse
from app.core.cache import cache

# Business Logic:
# 1. Shipping charge is calculated based on distance, weight, and delivery speed.
# 2. We use a strategy pattern to determine the transport method based on distance.
def calculate_shipping(
    db: Session,
    warehouse_id: int,
    customer_id: int,
    delivery_speed: str,
    weight: float,
):  
    # Caching key based on input parameters
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

    # Determine transport strategy based on distance
    strategy = get_transport_strategy(distance)
    base_charge = strategy.calculate(distance, weight)

    if delivery_speed == "express":
        final_charge = base_charge + 10 + (weight * 1.2)
    else:
        final_charge = base_charge + 10

    final_charge = round(final_charge, 2)

    cache.set(cache_key, final_charge, ttl=60)

    return final_charge

# Business Logic:
# 1. For seller-based shipping calculation, we first find the nearest warehouse to the seller.
# 2. We then calculate the shipping charge based on the product's weight and delivery speed.
# 3. If the product is fragile, we add an additional charge.
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
    
    # Business Rule: Perishable products must use express delivery
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
    # Business Rule: Fragile items incur an additional charge
    if product.is_fragile:
        shipping_charge += 5

    return warehouse, shipping_charge