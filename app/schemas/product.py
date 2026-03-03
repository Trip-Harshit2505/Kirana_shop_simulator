from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    weight: float
    length: float
    width: float
    height: float
    seller_id: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True