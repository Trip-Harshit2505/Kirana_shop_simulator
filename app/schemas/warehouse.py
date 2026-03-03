from pydantic import BaseModel


class WarehouseBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True