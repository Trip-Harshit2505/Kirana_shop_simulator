from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    phone: str
    latitude: float
    longitude: float


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True