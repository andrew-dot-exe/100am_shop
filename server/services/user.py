import bcrypt
from datetime import timedelta
from sqlalchemy.orm import Session

from models.user import User

class UserAuth:
    
    def hash_password(self, password : bytes) -> bytes:
        """
        Функция хэширования пароля
        Принимает пароль в формате строки с кодировкой UTF-8 и 
        шифрует его при помощи bcrypt.
        Возвращет bytes с хешированным паролем.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(
            password,
            salt)

    def check_password(self, hash: bytes, base_hash: bytes) -> bool:
        """
        Проверка пароля используя проверку bcrypt.
        """
        return bcrypt.checkpw(hash, base_hash)
    
    def create_access_token(self, userData: dict, expire_delta: timedelta) -> str:
        return "token"
    
    def decode_token(self, token: str) -> None:
        raise NotImplementedError

class UserDBaseManagement:
    def __init__(self, session : Session):
        self.session = session
    
    def add_user(self, login : str, password: bytes, phone_number: str, is_admin : bool = False):
        """
        Создает пользователя в базе данных
        """
        usr = User(login=login,
                   password_hash=password,
                   phone_number=phone_number,
                   is_admin=is_admin)
        self.session.add(usr)
    
    def delete_user(self, login: str):
        """
        Удаляет пользователя из базы данных
        """
        user_to_delete = self.session.query(User).filter(User.login == login).first()
        if not user_to_delete:
            raise RuntimeError
        self.session.delete(user_to_delete)
    
    def update_password(self, login: str, new_password: bytes):
        """
        Изменяет пароль на новый для пользователя по логину
        """
        user = self.session.query(User).filter(User.login == login).first()
        if not user:
            raise RuntimeError
        user.password_hash = new_password
        
    
    def update_phone_number(self, login: str, new_phone_number: str):
        """
        Изменяет номер телефона для пользователя по логину
        """
        user = self.session.query(User).filter(User.login == login).first()
        if not user:
            raise RuntimeError
        user.phone_number = new_phone_number
    
    def update_admin(self, login: str, new_permission: bool):
        """
        Изменяет статус права администрирования для пользователя по логину
        """
        user = self.session.query(User).filter(User.login == login).first()
        if not user:
            raise RuntimeError
        user.is_admin = new_permission
    
    def save_changes(self):
        self.session.commit()
        
        
class UserService:
    
    def __init__(self, session: Session):
        self.session = session
        
    def login(self, userCredentials: dict):
        pass
    
    