"""
REST-ful Shop server implementation
"""
import os
import logging
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI, Security, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import sessionmaker

from services.shop_item import ShopController
from services.user import UserController
from dto.user import UserLoginCredentials, UserInDB


from models import Base

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

#load variables from .env
try:
    load_dotenv()
except FileNotFoundError:
    raise FileNotFoundError('.env file not found.')

SECRET_KEY = os.getenv('SECRET_KEY') or "null"
ALGORITHM = os.getenv('ALGORITHM') or "HS256"
DBASE_CONN_STRING = os.getenv('DATABASE_CONN_STRING') or "sqlite://memory"

#database setup
dbase_engine = create_async_engine(DBASE_CONN_STRING)
dbase_async_session = sessionmaker(
    dbase_engine, class_=AsyncSession #type:ignore
) #type: ignore

async def get_session():
    async with dbase_async_session() as session: #type: ignore
        logger.debug(type(session))
        yield session


async def get_user_controller(
    session: AsyncSession = Depends(get_session),
):
    # Создаем экземпляр UserController с сессией
    controller = UserController(session, SECRET_KEY, ALGORITHM)
    yield controller

async def get_shop_controller(session: AsyncSession = Depends(get_session)):
    controller = ShopController(session)
    yield controller

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0",
        routes=app.routes,
    )

    # Добавляем секцию безопасности
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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

@app.get('/whoami')
async def whoami_route():
    return "null"

@app.get('/items')
async def get_shop_items_route(count: int,
    shop_controller: ShopController = Depends(get_shop_controller)):
    return {"null"}

@app.get('/item/{article}')
async def get_shop_item_info_route():
    pass


if __name__ == '__main__':
    uvicorn.run(app=app, reload=True)
