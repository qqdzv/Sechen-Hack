

from fastapi import APIRouter,Depends,status

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.auth.models import User

from src.ai_bot.utils import get_bot_for_user
from src.auth.base_config import get_current_user
from fastapi.responses import JSONResponse
from datetime import datetime
from src.ai_bot.models import AIMessage
from src.doctor.models import Doctor
from src.doctor.base_config import get_current_doctor
from src.ai_bot.schemas import AIMessageAdd,AIMessageRead
from typing import List


async def get_role(
    user: User = Depends(get_current_user),
    doctor: Doctor = Depends(get_current_doctor)
):
    if isinstance(doctor, JSONResponse):
        doctor = False
        pass
    if isinstance(user, JSONResponse):
        user = False
        pass
    
    if not doctor and not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Вы не авторизованы"}
        )

    elif doctor:
        return {"role" : "doctor", "uid" : doctor.id}
    else:
        return {"role" : "user", "uid" : user.id}
    
router = APIRouter(
    prefix="/ai_chat",
    tags=["AI Chat"]
)

@router.post("/send", response_model=AIMessageRead)
async def send_message(message: AIMessageAdd, info = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info
    
    # Создаем экземпляр модели Message
    new_message = AIMessage(
        sender_id=info['uid'],
        role=info['role'],
        content=message.content
    )
    session.add(new_message)
    await session.commit()  # Подтверждаем изменения в базе данных
    await session.refresh(new_message)  # Обновляем экземпляр, чтобы получить новые значения (например, ID)
    
    bot = await get_bot_for_user(role=info['role'],user_id=info['uid'])
    ai_content = (await bot.get_response(message=message.content))

    new_message.ai_answer = ai_content
    await session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": new_message.id,
            "sender_id": new_message.sender_id,
            "content": new_message.content,
            "ai_answer": new_message.ai_answer,
            "created_at": new_message.created_at.isoformat() if isinstance(new_message.created_at, datetime) else new_message.created_at
        }
    )

@router.get("/get_history", response_model=List[AIMessageRead])
async def get_chat_history(info = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(info,JSONResponse):
        return info
    
    all_messages = await session.execute(
        select(AIMessage).where(
            and_(
                AIMessage.sender_id == info['uid'],
                AIMessage.role == info['role']
            )
        )
    )
    
    history = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "content": message.content,
            "ai_answer": message.ai_answer,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        }
        
        for message in (all_messages.scalars().all())
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=history
    )
   
   