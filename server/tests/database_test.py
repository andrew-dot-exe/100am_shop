
# from models import Base, User, ShopItem
# from sqlalchemy import create_engine, insert, delete, select
# from sqlalchemy.orm import Session

# MEMORY_DATABASE_URL = "sqlite:///:memory:"
# REAL_DBASE = "postgresql+psycopg://andrew:databasepsw@localhost:5432/1amshop"

# class FakeSQLAlchemyDBase:
#     def __init__(self):
#         self.engine = create_engine(MEMORY_DATABASE_URL, echo=True)
#         Base.metadata.create_all(self.engine)
#         self.insert_fake_values()
#         with Session(self.engine) as session:
#             session.commit()

#     def get_engine(self):
#         return self.engine

#     def get_session(self):
#         return Session(self.engine)

#     def insert_fake_values(self):
#         insetrions = (
#             User(login='andrew', password_hash=b"hashed_pwd", is_admin=True, phone_number="88000"),
#             User(login='user1', password_hash=b"hashed_pwd", is_admin=True, phone_number="88001"),
#             User(login='user2', password_hash=b"hashed_pwd", is_admin=True, phone_number="88002"),
#             ShopItem(article=1, name="Some item 1", price=100.0, description=None, path_to_photo=None),
#             ShopItem(article=2, name="Some item 2", price=100.0, description=None, path_to_photo=None),
#             ShopItem(article=3, name="Some item 3", price=100.0, description=None, path_to_photo=None),
#             ShopItem(article=4, name="Some item 4", price=100.0, description=None, path_to_photo=None),

#         )
#         with Session(self.engine) as session:
#             session.add_all(insetrions)
#             session.commit()
#         pass

#     def list_user(self):
#         with Session(self.get_engine()) as session:
#             for user in session.scalars(select(User)):
#                 print(user.login)

#     def save_changes(self):
#         self.engine.commit()

# class DBaseTest:
#     def __init__(self):
#         self.base = FakeSQLAlchemyDBase()


#     def test_list(self):
#         get_all = select(User)
#         with Session(self.base.get_engine()) as session:
#             for user in session.scalars(get_all):
#                 print(user)



# if __name__ == '__main__':
#     test = DBaseTest()
#     test.test_list()
