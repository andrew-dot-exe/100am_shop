"""
Описание схемы данных с использованием SQLAlchemy
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean, Numeric, Text
from sqlalchemy.orm import relationship, Session, declarative_base

Base = declarative_base()
DATABASE_URL = "postgresql+psycopg://andrew:databasepsw@localhost:5432/1amshop"
engine = create_engine(DATABASE_URL, echo=True)


class User(Base):
    """ Class representing a user in database """
    __tablename__ = 'users'  # Имя таблицы в базе данных

    login = Column(String(50), unique=True, nullable=False, primary_key=True)  # Имя пользователя
    password_hash = Column(String(255), nullable=False)  # Хэш пароля
    is_admin = Column(Boolean, nullable=False)
    phone_number = Column(String(10), unique=True, nullable=False)
    
    basket_user_rel = relationship("basket", back_populates="users")

class ShopItem(Base):
    __tablename__ = "shop_items"
    
    article = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(Numeric(16, 2), nullable=False)
    description = Column(Text, nullable=True)
    path_to_photo = Column(String, nullable=True) # представляет относительный путь до фотографий
    
    basket_shopitem_rel = relationship("basket", back_populates="shop_items")
    
class Basket(Base):
    __tablename__ = "basket"

    shop_item_id = Column(Integer, ForeignKey("shop_items.article"), nullable=False, primary_key=True)
    user_login = Column(String, ForeignKey("users.login"), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False, default=1)

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.commit()
        session.close()
