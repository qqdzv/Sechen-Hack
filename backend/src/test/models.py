from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base

class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    
    task1 = Column(String)
    task2 = Column(String)
    task3 = Column(String)
    task4 = Column(String)
    task5 = Column(String)
    task6 = Column(String)
    task7 = Column(String)
    
    