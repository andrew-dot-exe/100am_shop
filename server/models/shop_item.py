from sqlalchemy import Column, Integer, String, Numeric, Text
from sqlalchemy.orm import relationship
from .base import Base

class ShopItem(Base):
    __tablename__ = "shop_items"

    article = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(Numeric(16, 2), nullable=False)
    description = Column(Text, nullable=True)
    path_to_photo = Column(String, nullable=True)

    