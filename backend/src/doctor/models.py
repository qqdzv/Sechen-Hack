from datetime import datetime, timezone
from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, Float
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Модель пользователя SQLAlchemy
class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String, index=True, nullable=False) #имя
    last_name = Column(String, index=True, nullable=False) # фамилия
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    gender = Column(String, index=True, nullable=True)
    age = Column(String,nullable=True)
    experience_age = Column(String,nullable=True)
    university = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    
    registered_at = Column(TIMESTAMP, default = lambda : datetime.now(timezone.utc).replace(tzinfo=None))
    
    # Метод для установки хэша пароля
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    # Метод для проверки пароля
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
    
    

class DoctorScan(Base):
    __tablename__ = "doctor_scan"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("doctor.id"), index=True)  # Индекс на sender_id
    gender = Column(String, index=True)  # Индекс на gender
    age = Column(String, index=True)  # Индекс на age
    body_part = Column(String, index=True)  # Индекс на body_part
    skin_type = Column(String)
    image_base64 = Column(String)
    contains_skin = Column(Boolean)
    response = Column(String, index=True)
    recommendations = Column(String, index=True)
    type = Column(String)
    percent = Column(Float)
    result = Column(String)
    ai_result = Column(String, nullable=False, default="")
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), index=True)  # Индекс на created_at