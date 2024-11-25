
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class SkinType(str, Enum):
    TYPE_I = "1"  # Очень светлая кожа, всегда обгорает, никогда не загорает
    TYPE_II = "2"  # Светлая кожа, часто обгорает, иногда загорает
    TYPE_III = "3"  # Средняя кожа, иногда обгорает, загорает постепенно
    TYPE_IV = "4"  # Смуглая кожа, редко обгорает, хорошо загорает
    TYPE_V = "5"  # Темная кожа, почти никогда не обгорает, легко загорает
    TYPE_VI = "6"  # Очень темная кожа, никогда не обгорает, хорошо загорает

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class UserProfileUpdate(BaseModel):
    first_name: Optional[str]  = None
    last_name: Optional[str]  = None
    email: Optional[EmailStr]  = None
    gender: Optional[Gender]  = None
    age : Optional[str] = None
    skin_type: Optional[SkinType]  = None

class UserRead(BaseModel):
    id : int
    first_name: str
    last_name: str
    email: EmailStr
    gender : Gender
    age : str
    skin_type: SkinType
    has_test: bool = False
    role : str = 'user'
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    gender : Gender
    age : str
    skin_type: SkinType

class UserLogin(BaseModel):
    email: EmailStr
    password: str

