
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr
from enum import Enum

class SkinType(str, Enum):
    TYPE_I = "1"  # Очень светлая кожа, всегда обгорает, никогда не загорает
    TYPE_II = "2"  # Светлая кожа, часто обгорает, иногда загорает
    TYPE_III = "3"  # Средняя кожа, иногда обгорает, загорает постепенно
    TYPE_IV = "4"  # Смуглая кожа, редко обгорает, хорошо загорает
    TYPE_V = "5"  # Темная кожа, почти никогда не обгорает, легко загорает
    TYPE_VI = "6"  # Очень темная кожа, никогда не обгорает, хорошо загорает

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class DoctorProfileUpdate(BaseModel):
    first_name: Optional[str]  = None
    last_name: Optional[str]  = None
    email: Optional[EmailStr]  = None
    gender: Optional[Gender]  = None
    age : Optional[str] = None
    experience_age : Optional[str] = None
    university : Optional[str] = None
    speciality : Optional[str] = None
    
    
class DoctorRead(BaseModel):
    id : int
    first_name: str
    last_name: str
    email: EmailStr
    gender : Gender
    age : str
    experience_age: str
    university : Optional[str] = None
    speciality : Optional[str] = None
    role : str = 'doctor'
    
    class Config:
        from_attributes = True

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    gender : Gender
    age : str
    experience_age: str
    university : str
    speciality : str

class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class BodyPart(str, Enum):
    anterior_torso = "anterior torso"  # Передняя часть торса
    lower_extremity = "lower extremity"  # Нижняя конечность
    head_or_neck = "head/neck"  # Голова/шея
    upper_extremity = "upper extremity"  # Верхняя конечность
    posterior_torso = "posterior torso"  # Задняя часть торса
    palms_or_soles = "palms/soles"  # Ладони/подошвы
    oral_or_genital = "oral/genital"  # Ротовая/генитальная область
    lateral_torso = "lateral torso"  # Боковая часть торса

class DoctorScanAddNew(BaseModel):
    gender: Gender
    age: str
    body_part: BodyPart
    image_base64: str

    class Config:
        from_attributes = True

        
class DoctorScanResponse(BaseModel):
    id: int
    response : str
    percent : float
    type : str
    result : str
    recommendations : str
    image_base64 : str
    
    class Config:
        from_attributes = True
        