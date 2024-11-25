from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP
from src.database import Base

class PrivateAPI(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, nullable=False)  # Исправлено на api_key
    call_counts = Column(Integer, default=0)  # Изменено на Integer для подсчета вызовов
    created_at = Column(TIMESTAMP, default = lambda : datetime.now(timezone.utc).replace(tzinfo=None))
    