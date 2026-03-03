from sqlalchemy.orm import Session
from app.models.seller import Seller
from app.models.warehouse import Warehouse
from app.utils.distance import calculate_distance
from fastapi import HTTPException
from app.core.cache import cache

# Business Logic:
# 1. For seller-based shipping calculation, we first find the nearest warehouse to the seller.
# 2. We then calculate the shipping charge based on the product's weight and delivery speed.
def get_nearest_warehouse(db: Session, seller_id: int):

    # Caching key based on seller_id
    cache_key = f"nearest_warehouse:{seller_id}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    warehouses = db.query(Warehouse).filter(
        Warehouse.operational_status == "active"
    ).all()
    if not warehouses:
        raise HTTPException(status_code=404, detail="No warehouses available")

    # Finding the nearest warehouse to the seller
    nearest = None
    min_distance = float("inf") # Initialize with infinity to find the minimum

    for warehouse in warehouses:
        distance = calculate_distance(
            seller.latitude,
            seller.longitude,
            warehouse.latitude,
            warehouse.longitude,
        )

        if distance < min_distance:
            min_distance = distance
            nearest = warehouse

    cache.set(cache_key, nearest, ttl=60)  # cache for 60 seconds
    return nearest