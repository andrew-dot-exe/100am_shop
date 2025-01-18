"""
REST-ful Shop server implementation
"""
import os
import logging
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, Security, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .services.user import UserController
from .dto.user import UserLoginCredentials, UserInDB

from .models import Base

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

#load variables from .env
try:
    load_dotenv()
except FileNotFoundError:
    raise FileNotFoundError('.env file not found.')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
DBASE_CONN_STRING = os.getenv('DATABASE_CONN_STRING')

#database setup
dbase_engine = create_async_engine(DBASE_CONN_STRING)
dbase_async_session = sessionmaker(
    dbase_engine, class_=AsyncSession
)

async def get_session():
    async with dbase_async_session() as session:
        logger.debug(type(session))
        yield session
        

async def get_user_controller(
    session: AsyncSession = Depends(get_session),
):
    # Создаем экземпляр UserController с сессией
    controller = UserController(session, SECRET_KEY, ALGORITHM)
    yield controller

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with dbase_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def get_root():
    session = get_session()
    print(type(session))
    return {"response": "Welcome to my 1am shop!"}


@app.post('/login')
async def login_route(credentials: UserLoginCredentials,
                      user_controller: UserController = Depends(get_user_controller)):#
    token = await user_controller.login(credentials)
    return {"token": token}

@app.post('/register')
async def register_route(user_db: UserInDB,
                         user_controller: UserController = Depends(get_user_controller)):
    await user_controller.register_user(user_db)
    return {'result': user_db.login}



if __name__ == '__main__':
    uvicorn.run(app=app, reload=True)
