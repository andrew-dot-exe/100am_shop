"""
Авторизация пользователя, используя JWT-токены
"""
import bcrypt
from datetime import timedelta

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

