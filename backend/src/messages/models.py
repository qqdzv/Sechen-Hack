from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP
from src.database import Base

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False, index=True)  # Индекс на sender_id
    sender_type = Column(String, nullable=False, index=True)  # Индекс на sender_type
    receiver_id = Column(Integer, nullable=False, index=True)  # Индекс на receiver_id
    receiver_type = Column(String, nullable=False, index=True)  # Индекс на receiver_type
    content = Column(String, nullable=False)
    abcd_score = Column(String,default=None)
    doctor_result = Column(String, default=None)
    image_base64 = Column(String, default=None)
    segmentation_base64 = Column(String, default=None)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), index=True)  # Индекс на created_at
    