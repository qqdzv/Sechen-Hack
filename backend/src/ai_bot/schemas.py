
from pydantic import BaseModel
from datetime import datetime

    
class AIMessageAdd(BaseModel):
    content: str 

    class Config:
        from_attributes = True
        
        
class AIMessageRead(BaseModel):
    id : int
    sender_id: int 
    content: str 
    ai_answer: str|None
    role: str
    created_at: datetime 

    class Config:
        from_attributes = True