from pydantic import BaseModel
from typing import List

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

class OrderBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    product: Product
    class Config:
        orm_mode = True
