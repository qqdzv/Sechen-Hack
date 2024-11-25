from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
from src.auth.models import User
from src.config import SECRET_JWT,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from src.myredis import redis_fastapi
# Настройка JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_JWT, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)) -> User:
    try:
        exists = await redis_fastapi.exists(token)
        if exists:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "You was logout"
                }
            )
            
        payload = jwt.decode(token, SECRET_JWT, algorithms=[JWT_ALGORITHM])
        uid: int = payload.get("uid")
        role: str = payload.get("role")
        
        if uid is None or role != 'user':
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "User not registred"
                }
            )
        
        result = await session.execute(select(User).where(User.id == uid))
        existing_user = result.scalar_one_or_none()
    
        if existing_user is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "User not found"
                }
            )
        return existing_user
    except jwt.exceptions.ExpiredSignatureError:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Token has expired"
                }
            )
    except jwt.InvalidTokenError:
        return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "error": "Invalid JWT"
                }
            )


async def get_jwt_user(token: str = Depends(oauth2_scheme)) -> str:
    return token