
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageAdd(BaseModel):
    receiver_id: int 
    content: str 
    image_base64: Optional[str] = ''

    class Config:
        from_attributes = True
        
        
class MessageRead(BaseModel):
    id: int
    sender_id: int
    sender_type: str
    receiver_id: int 
    receiver_type: str
    receiver_name: str
    content: str 
    abcd_score: Optional[str]
    doctor_result: Optional[str]
    image_base64: Optional[str]
    segmentation_base64: Optional[str]
    created_at: datetime 

    class Config:
        from_attributes = True
