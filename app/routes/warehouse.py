from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.warehouse_service import get_nearest_warehouse
from app.schemas.shipping import NearestWarehouseResponse

router = APIRouter(prefix="/api/v1/warehouse", tags=["Warehouse"])


@router.get("/nearest", response_model=NearestWarehouseResponse)
def nearest_warehouse(sellerId: int, db: Session = Depends(get_db)):
    warehouse = get_nearest_warehouse(db, sellerId)

    return {
        "warehouseId": warehouse.id,
        "warehouseLocation": {
            "lat": warehouse.latitude,
            "long": warehouse.longitude,
        },
    }