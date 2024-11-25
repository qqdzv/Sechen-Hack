from datetime import datetime,timezone
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean,ForeignKey, Float
from src.database import Base

class Scan(Base):
    __tablename__ = "scan"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    folder_id = Column(Integer, ForeignKey("scan_folder.id"))
    contains_skin = Column(Boolean,index=True)
    
    response = Column(String, index=True)
    recommendations = Column(String, index=True)
    type = Column(String)
    percent = Column(Float)
    result = Column(String)
    image_base64 = Column(String)
    segmentation_base64 = Column(String)
    ai_result = Column(String, nullable=False, default="")
    created_at = Column(TIMESTAMP, default = lambda : datetime.now(timezone.utc).replace(tzinfo=None))
    
class ScanFolder(Base):
    __tablename__ = "scan_folder"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    body_part = Column(String)
    size = Column(String)
    how_many_days = Column(String)
    have_pain = Column(Boolean)
    have_medicines = Column(Boolean)
    mixing = Column(String)
    folder_name = Column(String)
    created_at = Column(TIMESTAMP, default = lambda : datetime.now(timezone.utc).replace(tzinfo=None))