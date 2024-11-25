
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.private_api.models import PrivateAPI
import secrets
import string
from fastapi.responses import JSONResponse
from fastapi import Header
from typing import Optional

router = APIRouter(
    prefix="/shared",
    tags=["Shared API"]
)


def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    return api_key


@router.get("/create_apikey")
async def create_apikey(session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    api = PrivateAPI(
        api_key=generate_api_key(),
        call_counts=10
    )
    session.add(api)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "detail": "Успешно создан ключ на 10,000 использований. По поводу расширенной версии писать в поддержку.",
            "api_key": f"Ваш ключ : '{api.api_key}'. Он должен находиться в заголовках запроса под названием API-KEY"
        }
    )


@router.post('/scan')
async def scan(
    api_key: Optional[str] = Header(None),  # Получаем токен из заголовка
    session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    token_exists = await session.execute(select(PrivateAPI).where(PrivateAPI.api_key==api_key))
    token_exists = (token_exists.scalar_one_or_none())
    if not token_exists:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Невалидный ключ"}
        )
    
    if token_exists.call_counts < 1:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Закончились все использования"}
        )
    token_exists.call_counts-=1
    await session.commit()
    
    '''
    обработка скана
    '''
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "вы здоровы"}
    )
