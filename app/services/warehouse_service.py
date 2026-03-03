from sqlalchemy.orm import Session
from app.models.seller import Seller
from app.models.warehouse import Warehouse
from app.utils.distance import calculate_distance
from fastapi import HTTPException
from app.core.cache import cache


def get_nearest_warehouse(db: Session, seller_id: int):
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

    nearest = None
    min_distance = float("inf")

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