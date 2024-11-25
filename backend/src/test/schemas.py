from pydantic import BaseModel
from typing import Optional

class TestBase(BaseModel):
    task1: Optional[str] = None
    task2: Optional[str] = None
    task3: Optional[str] = None
    task4: Optional[str] = None
    task5: Optional[str] = None
    task6: Optional[str] = None
    task7: Optional[str] = None
    
    class Config:
        from_attributes = True
