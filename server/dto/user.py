from pydantic import BaseModel, field_validator
from datetime import datetime

class UserLoginCredentials(BaseModel):
    login : str
    password : str

class UserInDB(BaseModel):
    login : str
    password : str
    phone_number: str
    is_admin: bool = False
class TokenPayload(BaseModel):
    login: str
    is_admin: bool
    expire_time: str # there is no expire info, but he's must present in token