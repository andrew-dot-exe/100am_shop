"""
Управление данными пользователей (регистрация, редактирование информации и т.д.)
"""


class UserManagement:
    def __init__(self):
        pass
    
    def create_user(self, login : str, password: bytes, phone_number: str, is_admin : bool = False):
        pass
    
    def delete_user(self, login: str):
        """
        Удаляет пользователя из базы данных
        """
        pass
    
    def update_password(self, login: str, new_password: bytes):
        """
        Изменяет пароль на новый для пользователя по логину
        """
        pass
    
    def update_phone_number(self, login: str, new_phone_number: str):
        """
        Изменяет номер телефона для пользователя по логину
        """
        pass
    
    def update_admin(self, login: str, new_permission: bool):
        """
        Изменяет статус права администрирования для пользователя по логину
        """
        pass