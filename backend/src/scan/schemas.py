from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class BodyPart(str, Enum):
    anterior_torso = "anterior torso"  # Передняя часть торса
    lower_extremity = "lower extremity"  # Нижняя конечность
    head_or_neck = "head/neck"  # Голова/шея
    upper_extremity = "upper extremity"  # Верхняя конечность
    posterior_torso = "posterior torso"  # Задняя часть торса
    palms_or_soles = "palms/soles"  # Ладони/подошвы
    oral_or_genital = "oral/genital"  # Ротовая/генитальная область
    lateral_torso = "lateral torso"  # Боковая часть торса

class ScanAddNew(BaseModel):
    folder_name: str
    body_part: Optional[BodyPart] = 'head/neck'
    size: str
    how_many_days: str
    have_pain: Optional[bool] = True
    have_medicines: Optional[bool] = True
    mixing: str
    image_base64: str

    class Config:
        from_attributes = True

        
class ScanResponse(BaseModel):
    id: int
    response : str
    percent : float
    type : str
    result : str
    recommendations : str
    image_base64 : str
    
    class Config:
        from_attributes = True
        
class ScanInfo(BaseModel):
    id : int
    folder_id: int
    response : str
    percent : Optional[float]
    type : Optional[str]
    result : Optional[str]
    recommendations :Optional[str]
    image_base64 : Optional[str]
    created_at: datetime 

    class Config:
        from_attributes = True


class Folder(BaseModel):
    id: int
    folder_name: str
    body_part: Optional[BodyPart]
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
