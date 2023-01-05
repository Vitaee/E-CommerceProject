from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class Category(BaseModel):
    id: int
    name: str

class CategoryRegisterSchema(BaseModel):
    name: str


class Rating(BaseModel):
    rate: float
    count: int


class Business(BaseModel):
    id = int
    name = str
    country = str
    image = str

class BusinessRegisterSchema(BaseModel):
    name: str
    country: str
    image: str
    
class Product(BaseModel):
    id: int
    title: str
    price: int
    description: str
    #category: str
    images: List[str]
    rating: float
    #business: str

class ProductRegisterSchema(BaseModel):
    title: str
    price: float
    description: str
    category: str
    images: List[str]
    count: int = 0
    rating: float = 0.0

