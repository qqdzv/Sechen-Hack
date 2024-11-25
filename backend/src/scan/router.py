

from fastapi import APIRouter, Depends, status

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.auth.schemas import UserRead

from src.auth.models import User
from pydantic import BaseModel

from src.doctor.models import Doctor
from src.messages.models import Message

from starlette.concurrency import run_in_threadpool

from src.auth.base_config import get_current_user
from src.doctor.base_config import get_current_doctor
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from src.scan.models import Scan, ScanFolder
from src.scan.schemas import ScanResponse,ScanInfo, ScanAddNew,Folder
from pydantic import BaseModel
from src.logger import logger
from src.scan.body_checker import validate_body_scan
from src.scan.ml.classification_model import get_result
from src.scan.test_support import generate_user_report
from src.doctor.models import DoctorScan
from src.scan.ml.segmnetation import png_to_base64, get_segmentation

import os
from src.scan.doctor_support import generate_doctor_report
from src.scan.ml.abcd_generate import get_absd_score


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
    prefix="/scan",
    tags=["Scan"]
)

categories_risk = {
    "АК (Актинический кератоз)": "good",
    "БКК (Базальноклеточная карцинома)": "bad",
    "БКЛ (Доброкачественное кератотическое поражение)": "good",
    "ДФ (Дерматофиброма)": "good",
    "МЕЛ (Меланома)": "bad",
    "НВ (Невус)": "good",
    "ПСК (Плоскоклеточная карцинома)": "bad",
    "СОС (Сосудистые поражения)": "good"
}


class DetailResponse(BaseModel):
    detail: str
    
class ReceiverID(BaseModel):
    receiver_id : int

class ForwardScan(BaseModel):
    doctor_id: int
    scan_id: int

@router.post("/send_new", response_model=ScanResponse)
async def send_message(new_scan: ScanAddNew, user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user
    

    new_message = Scan(
        sender_id=user.id,
        image_base64=new_scan.image_base64,
    )
    
    session.add(new_message)
    await session.commit()  # Подтверждаем изменения в базе данных
    await session.refresh(new_message)  # Обновляем экземпляр, чтобы получить новые значения (например, ID)
    
    ai_aswer = await validate_body_scan(image_base64=new_scan.image_base64)
    
    new_message.contains_skin = ai_aswer['contains_skin']
    new_message.ai_result = ai_aswer["description"]
    
    if not ai_aswer['contains_skin']:
        await session.commit()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "id": new_message.id,
                "detail": new_message.ai_result,
            }
        )

    existing_folder = await session.execute(
        select(ScanFolder).filter(
            ScanFolder.sender_id == user.id,
            ScanFolder.folder_name == new_scan.folder_name
        )
    )
    existing_folder = existing_folder.scalar_one_or_none()
    
    if not existing_folder:
        if not new_scan.body_part:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Папка не может создаться без Части тела"}
            )
        # Создаем экземпляр модели Message
        existing_folder = ScanFolder(
            sender_id=user.id,
            body_part = new_scan.body_part,
            folder_name=new_scan.folder_name,
            size = new_scan.size,
            how_many_days = new_scan.how_many_days,
            have_pain = new_scan.have_pain,
            have_medicines =new_scan.have_medicines,
            mixing = new_scan.mixing
        )
        session.add(existing_folder)
        await session.commit()  # Подтверждаем изменения в базе данных
        await session.refresh(existing_folder)  # Обновляем экземпляр, чтобы получить новые значения (например, ID)
        logger.info(f"создаем папку {new_scan.folder_name}")
    
    new_message.folder_id = existing_folder.id
    
    session.add(new_message)
    await session.commit()  # Подтверждаем изменения в базе данных
    await session.refresh(new_message)  # Обновляем экземпляр, чтобы получить новые значения (например, ID)

    '''
    выше вся проверка валидности фотки, дальше обработка
    '''
    user_info = UserRead.model_validate(user)
    result = await run_in_threadpool(get_result,age=int(user_info.age),gender=user_info.gender,body_part=existing_folder.body_part,image_base64=new_message.image_base64)
    
    more_info = await generate_user_report(
        gender = user.gender,
        age = user.age,
        skin_type = user.skin_type,
        diagnosis=result[0],
        probability=result[1],
        disease_type=categories_risk[result[0]]
    ) 
    
    new_message.response = result[0]
    new_message.percent = result[1]
    new_message.type = categories_risk[result[0]]
    new_message.result = more_info['result']
    new_message.recommendations = more_info["recommendations"]
    
    await session.commit()
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": new_message.id,
            "response": result[0],
            "percent": result[1],
            "type" : categories_risk[result[0]],
            "result" : more_info['result'],
            "recommendations" : more_info["recommendations"],
            "image_base64" : new_scan.image_base64  
        }
    )


@router.get("/get_folders", response_model=List[Folder])
async def get_folders(user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user
    
    folders = await session.execute(
        select(ScanFolder).where(
            ScanFolder.sender_id == user.id
        )
    )

    user_folders = [
        {
            "id": folder.id,
            "folder_name": folder.folder_name,
            "body_part": folder.body_part,
            "created_at": folder.created_at.isoformat() if isinstance(folder.created_at, datetime) else folder.created_at
        }
        for folder in (folders.scalars().all())
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user_folders
    )

    
@router.get("/history/{folder_id}", response_model=List[ScanInfo])
async def get_history_by_folder_id(folder_id: str, user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user
    
    folder = await session.execute(
        select(ScanFolder).where(
            and_(
                ScanFolder.sender_id == user.id,
                ScanFolder.id == int(folder_id)
            )
        )
    )
    folder = folder.scalar_one_or_none()
    
    if not folder:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Папки с таким id не существует"}
        )
    
    scans = await session.execute(
        select(Scan).where(
            Scan.folder_id == folder.id 
        )
    )
    
    history = [
        {
            "id": message.id,
            "image_base64": message.image_base64,
            "folder_id": message.folder_id,
            "response" : message.response,
            "percent" : message.percent,
            "type" : message.type,
            "result" : message.result,
            "recommendations": message.recommendations,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        }
        for message in (scans.scalars().all())
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=history
    )

@router.post('/forward',response_model=DetailResponse)
async def forward_scan_to_doctor(form : ForwardScan, user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    result = await session.execute(select(Doctor).where(Doctor.id == form.doctor_id))
    doctor = result.scalar_one_or_none() 
    
    if not doctor:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Доктор с данным id не найден"}
        )
    
    result = await session.execute(select(Scan).where(
        and_(
            Scan.id == form.scan_id,
            Scan.sender_id == user.id
            )
        )
    )
    scan = result.scalar_one_or_none() 
    
    if not scan:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Скан с данным id не найден"}
        )
    
    pic_path = await run_in_threadpool(get_segmentation,image_base64=scan.image_base64)
    segmentation_base64 = await run_in_threadpool(png_to_base64,png_file_path=pic_path)
    
    folder = await session.execute(select(ScanFolder).where(ScanFolder.id == scan.folder_id))
    folder = folder.scalar_one_or_none()
    
    abcd_score = await run_in_threadpool(get_absd_score,image_base64=scan.image_base64,size_answer=folder.size)
    
    result = await run_in_threadpool(get_result,age=int(user.age),gender=user.gender,body_part=folder.body_part,image_base64=scan.image_base64)
    
    result = (await generate_doctor_report(
        gender = user.gender,
        age = user.age,
        skin_type = user.skin_type,
        diagnosis=result[0],
        probability=result[1],
        disease_type=categories_risk[result[0]],
        abcd=abcd_score
    ))
    
    if os.path.exists(pic_path):
        os.remove(pic_path)  # Удаляем файл
        logger.info(f"Файл {pic_path} был успешно удален.")
            
    message = Message(
        sender_id = user.id,
        sender_type = 'user',
        receiver_id = doctor.id,
        receiver_type = 'doctor',
        content = scan.ai_result,
        image_base64 = scan.image_base64, 
        segmentation_base64 = segmentation_base64,
        abcd_score=abcd_score,
        doctor_result=result
        
    )
    
    session.add(message)
    await session.commit()
    await session.refresh(message)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Успешно отправлено врачу"}
    )


@router.get("/get_all_scans", response_model=List[ScanInfo])
async def get_all_scans(user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user

    scans = await session.execute(
        select(Scan).where(
            and_(
                Scan.sender_id == user.id,
                Scan.contains_skin == True
            )
        )
    )
    
    history = [
        {
            "id": message.id,
            "image_base64": message.image_base64,
            "folder_id": message.folder_id,
            "response": message.response,
            "percent": message.percent,
            "type": message.type,
            "result": message.result,
            "recommendations": message.recommendations,
            "created_at": message.created_at.isoformat() if isinstance(message.created_at, datetime) else message.created_at
        }
        for message in (scans.scalars().all())  # Используйте await для асинхронного запроса
    ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=history
    )


@router.get("/scan_by_id/{scan_id}", response_model=ScanInfo)
async def get_scan_by_id(scan_id : int, info : str = Depends(get_role), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    
    if isinstance(info, JSONResponse):
        return info
    
    if info['role'] == 'user':
        result = await session.execute(select(Scan).where(
            and_(
                Scan.id == scan_id,
                Scan.sender_id == info['uid']
                )
            )
        )
        result = await session.execute(select(Scan).where(Scan.id == scan_id))
    else:
        result = await session.execute(select(DoctorScan).where(DoctorScan.id == scan_id))
                                       
    scan = result.scalar_one_or_none() 
    
    if not scan:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Скан с данным id не найден"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": scan.id,
            "image_base64": scan.image_base64,
            "response" : scan.response,
            "percent" : scan.percent,
            "type" : scan.type,
            "result" : scan.result,
            "recommendations": scan.recommendations,
            "created_at": scan.created_at.isoformat() if isinstance(scan.created_at, datetime) else scan.created_at
        }
    ) 
