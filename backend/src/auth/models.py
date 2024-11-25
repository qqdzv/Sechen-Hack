from datetime import datetime, timezone
from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)  # Индекс на первичный ключ

    first_name = Column(String, index=True, nullable=False)  # Индекс для поиска по имени
    last_name = Column(String, index=True, nullable=False)    # Индекс для поиска по фамилии
    email = Column(String, unique=True, index=True, nullable=False)  # Уникальный индекс на email
    hashed_password = Column(String, nullable=True)
    gender = Column(String, index=True, nullable=True)  # Индекс для поиска по полу
    age = Column(String, nullable=True)
    skin_type = Column(String, nullable=True)
    
    tg_id = Column(BigInteger, nullable=True, default=None)
    registered_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), index=True)  # Индекс на время регистрации
    
    # Метод для установки хэша пароля
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    # Метод для проверки пароля
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)