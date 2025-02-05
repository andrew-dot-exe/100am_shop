from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Basket(Base):
    __tablename__ = "basket"

    shop_item_id = Column(Integer, ForeignKey("shop_items.article"), nullable=False, primary_key=True)
    user_login = Column(String, ForeignKey("users.login"), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False, default=1)
    
    basket_user = relationship("User", backref="users")
    basketr_shop_item = relationship("ShopItem", backref="shop_item")