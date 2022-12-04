from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class Category(BaseModel):
    id: int
    name: str
    image: str


class Rating(BaseModel):
    rate: float
    count: int


class Business(BaseModel):
    id = int
    name = str
    country = str
    image = str

class Product(BaseModel):
    id: int
    title: str
    price: int
    description: str
    category: Category
    images: List[str]
    rating: Rating
    business: Business

class ProductRegisterSchema(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: List[str]
    business: str

