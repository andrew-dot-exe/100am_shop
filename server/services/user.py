import bcrypt
import datetime
import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from models.user import User
from dto.user import UserLoginCredentials, UserInDB, TokenPayload


class UserAuth:

    @staticmethod
    def hash_password(password : str) -> str:
        """
        Функция хэширования пароля
        Принимает пароль в формате строки с кодировкой UTF-8 и
        шифрует его при помощи bcrypt.
        Возвращет bytes с хешированным паролем.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            password.encode('utf-8'),
            salt).decode('utf-8')

    @staticmethod
    def check_password(hash: str, base_hash: str) -> bool:
        """
        Проверка пароля используя проверку bcrypt.
        Хэш с базы почему-то в виде str, хотя должен быть как bytes
        """
        return bcrypt.checkpw(hash.encode('utf-8'), base_hash.encode('utf-8'))

    @staticmethod
    def create_access_token(userData: TokenPayload, secret_key:str, algorithm: str) -> str:
        """
        Создает JWT-токен
        """
        encoded_user = userData.model_dump()
        token = jwt.encode(
            payload=encoded_user,
            key=secret_key,
            algorithm=algorithm)
        return token

    @staticmethod
    def decode_token(token: str, secret_key: str, algorithm: str) -> TokenPayload:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        decoded_payload = TokenPayload(login=payload['login'],
                                        is_admin=payload['is_admin'],
                                        expire_time=payload['expire_time'])
        return decoded_payload

    @staticmethod
    def async_create_access_token(userData: TokenPayload, secret_key:str, algorithm: str) -> str:
        """
        Создает JWT-токен
        """
        encoded_user = userData.model_dump()
        token = jwt.encode(encoded_user, secret_key, algorithm)
        return token

    @staticmethod
    def async_decode_token(token: str, secret_key: str, algorithm: str) -> TokenPayload:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        decoded_payload = TokenPayload(login=payload['login'],
                                        is_admin=payload['is_admin'],
                                        expire_time=payload['expire_time'])
        return decoded_payload

class UserDBaseManagement:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_hashed_psw_from_db(self, login: str) -> str:
        """
        Retrieves the hashed password for a user by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user = result.scalars().first()
        if not user:
            return None
        return user.password_hash

    async def user_is_admin(self, login: str) -> bool:
        """
        Checks if a user is an admin by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user = result.scalars().first()
        if not user:
            return None
        return user.is_admin

    async def add_user(self, login: str, password: str, phone_number: str, is_admin: bool = False):
        """
        Adds a new user to the database.
        """
        usr = User(login=login, password_hash=password, phone_number=phone_number, is_admin=is_admin)
        async with self.session.begin():
            self.session.add(usr)
            await self.session.commit()

    async def delete_user(self, login: str):
        """
        Deletes a user from the database by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user_to_delete = result.scalars().first()
        if not user_to_delete:
            raise RuntimeError("User not found")
        await self.session.delete(user_to_delete)
        await self.session.commit()

    async def update_password(self, login: str, new_password: str):
        """
        Updates the password for a user by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user = result.scalars().first()
        if not user:
            raise RuntimeError("User not found")
        user.password_hash = new_password
        await self.session.commit()

    async def update_phone_number(self, login: str, new_phone_number: str):
        """
        Updates the phone number for a user by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user = result.scalars().first()
        if not user:
            raise RuntimeError("User not found")
        user.phone_number = new_phone_number
        await self.session.commit()

    async def update_admin(self, login: str, new_permission: bool):
        """
        Updates the admin permission for a user by their login.
        """
        result = await self.session.execute(select(User).filter(User.login == login))
        user = result.scalars().first()
        if not user:
            raise RuntimeError("User not found")
        user.is_admin = new_permission
        await self.session.commit()

    async def save_changes(self):
        """
        Commits the changes to the database.
        """
        await self.session.commit()



class UserController:
    secret: str ="secret-from-dotenvs"
    algorithm = "HS256"

    def __init__(self, session: AsyncSession, secret : str, algorithm: str):
        self.session = session
        self.database_manager = UserDBaseManagement(session)
        self.secret = secret
        self.algorithm = algorithm
        if secret == None:
            raise TypeError("No secret provided!")

    async def login(self, userCredentials: UserLoginCredentials) -> str:

        hashed_psw =  await self.database_manager.get_hashed_psw_from_db(userCredentials.login)
        if hashed_psw == None:
            raise ValueError("User not found")
        check_login = UserAuth.check_password(userCredentials.password, hashed_psw)
        if check_login:
            expire = datetime.datetime.now() + datetime.timedelta(
                                        minutes=30)
            payload = TokenPayload(login=userCredentials.login,
                                    is_admin=False,
                                    expire_time= "mamu_ebal"
                                    )
            token = UserAuth.create_access_token(payload, self.secret, self.algorithm)
            return token

    async def register_user(self, userInfo:UserInDB):
        hashed_psw = UserAuth.hash_password(userInfo.password)
        await self.database_manager.add_user(
            userInfo.login,
            hashed_psw,
            userInfo.phone_number,
            userInfo.is_admin
        )
