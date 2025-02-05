# from ..models import User, Base

# from sqlalchemy import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# from sqlalchemy.future import select

# DBASE_CONN_STRING = ""

# #database setup
# dbase_engine = create_async_engine(DBASE_CONN_STRING)
# dbase_async_session = sessionmaker(
#     dbase_engine, class_=AsyncSession
# )

# async def get_session(): #will be move to dbase layer
#     async with dbase_async_session() as session:
#         yield session

# async def create_tables(): #will be moved to dbase layer
#     async with dbase_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# #crud for Users, will replace user.UserManagement
# class as_UserManagement:
#     async def __init__(self):
#         # will be replaced with get_session(), so there's no need for constructor
#         pass

#     @staticmethod
#     async def get_hashed_psw_from_db(login: str):
#         async with get_session() as session:
#             result = await session.execute(select(User).where(User.login == login))
#             user = result.scalars().first()
#             if not user:
#                 return None
#             return user.password_hash

#     @staticmethod
#     async def add_user(login, hashed_password : bytes, phone_number: str, is_admin: bool = False):
#         async with get_session() as session:
#             usr = User(login=login,
#                     password_hash=hashed_password,
#                     phone_number=phone_number,
#                     is_admin=is_admin)
#             await session.add(usr)

#     @staticmethod
#     async def delete_user(login: str):
#         async with get_session() as session:
#             user = await session.query(User).filter(User.login == login).first()
#             if not user:
#                 return None
#             session.delete(user)


# # Вызов функции для создания таблиц
# import asyncio
# asyncio.run(create_tables())
