from pydantic import BaseModel
from typing import Optional

class BookInfo(BaseModel):
    title: str
    author: Optional[str]
    price: Optional[float]
    url: Optional[str]
    image_url: Optional[str]

class ProductInfo(BaseModel):
    title: str
    description: str
    price: float
    image_url: Optional[str]
    url: Optional[str]
    author: Optional[str] 