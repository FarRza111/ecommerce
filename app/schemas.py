from typing import List
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    category: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True



class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True  # ORM models can be converted to Pydantic models


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] # items of  OrderItemCreate - look below json example 
    address: str
    total_price: float  # Optional: If passed by the frontend

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models

    # {
    #   "items": [
    #     {
    #       "product_id": 10,
    #       "quantity": 12322
    #     }
    #   ],
    #   "address": "AZAASA",
    #   "total_price": 112.334
    # }
