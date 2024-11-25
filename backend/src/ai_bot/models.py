from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from src.database import Base

class AIMessage(Base):
    __tablename__ = "ai_message"

    id = Column(Integer, primary_key=True, index=True)  # Индекс для первичного ключа
    sender_id = Column(Integer, ForeignKey("user.id"), index=True)  # Индекс для sender_id
    role = Column(String, index=True)  # Индекс для role
    content = Column(String, nullable=True)
    ai_answer = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), index=True)  # Индекс для created_at
