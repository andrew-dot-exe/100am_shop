from pydantic import BaseModel
from decimal import Decimal

class ShopItem(BaseModel):
   article: int = 0
   name: str
   price: Decimal
   description: str
   path_to_photo: str | None

class ShopItemShort(BaseModel):
    article: int
    name: str
    price: Decimal
