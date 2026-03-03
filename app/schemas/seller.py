from pydantic import BaseModel


class SellerBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class SellerCreate(SellerBase):
    pass


class SellerResponse(SellerBase):
    id: int

    class Config:
        from_attributes = True