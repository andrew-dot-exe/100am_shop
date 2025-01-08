from sqlalchemy import Column, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    """Class representing a user in the database."""
    __tablename__ = 'users'

    login = Column(String(50), unique=True, nullable=False, primary_key=True)
    password_hash = Column(LargeBinary(255), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    phone_number = Column(String(10), unique=True, nullable=False)

    basket_user_rel = relationship("Basket", back_populates="users")