from models import Base, User, ShopItem, Basket
from sqlalchemy import create_engine, Session, insert, delete

MEMORY_DATABASE_URL = "sqlite:///:memory:"


class FakeSQLAlchemyDBase:
    def __init__(self):
        self.engine = create_engine(MEMORY_DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            session.commit()
            session.close()
        

    def get_engine(self):
        return self.engine
    
    def insert_fake_values(self):
        insetrions = (
            User(login='andrew', password_hash="hashed_pwd", is_admin=True, phone_number="88000"),
            User(login='user1', password_hash="hashed_pwd", is_admin=True, phone_number="88000"),
            User(login='user2', password_hash="hashed_pwd", is_admin=True, phone_number="88000"),
        )
        pass