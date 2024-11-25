
from fastapi import APIRouter,Depends,status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.doctor.schemas import DoctorRead, DoctorCreate
from src.doctor.models import Doctor, DoctorScan
from pydantic import BaseModel

from src.doctor.base_config import create_access_token
from src.doctor.base_config import get_current_doctor, get_jwt_doctor
from fastapi.responses import JSONResponse
from src.doctor.schemas import DoctorCreate, DoctorLogin, DoctorProfileUpdate, PasswordChange, DoctorScanAddNew, DoctorScanResponse
from src.myredis import redis_fastapi
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List
from src.scan.body_checker import validate_body_scan
from src.scan.ml.classification_model import get_result
from starlette.concurrency import run_in_threadpool
from src.scan.test_support import generate_user_report

router = APIRouter(
    prefix="/doctor",
    tags=["Doctor"]
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

class JWTResponse(BaseModel):
    access_token : str

class DetailResponse(BaseModel):
    detail: str

@router.post("/login",response_model=JWTResponse)
async def login(login_form: DoctorLogin, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    result = await session.execute(select(Doctor).where(Doctor.email == login_form.email))
    doctor = result.scalar_one_or_none()
    
    if doctor is None or not doctor.verify_password(login_form.password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Неправильная почта или пароль"}
        )

    # Создание токена (если это необходимо)
    token = create_access_token(data={"uid": doctor.id, "role": "doctor"})
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token}
    )

@router.post("/register", response_model=JWTResponse)
async def register(user_data: DoctorCreate, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    existing_email = await session.execute(select(Doctor).where(Doctor.email == user_data.email))
    if existing_email.scalar_one_or_none() is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail': "Почта уже занята"}
        )
    
    if len(user_data.password) < 8:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать минимум 8 символов."}
        )
    if not any(char.isdigit() for char in user_data.password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать хотя бы одну цифру."}
        )
    if not any(char.isalpha() for char in user_data.password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать хотя бы одну букву."}
        )
        
    doctor = Doctor(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        gender=user_data.gender,
        age=user_data.age,
        experience_age=user_data.experience_age,
        university=user_data.university,
        speciality=user_data.speciality
    )
    
    doctor.set_password(user_data.password)  # Устанавливаем хешированный пароль
    session.add(doctor)
    await session.commit()
    await session.refresh(doctor)
    
    token = create_access_token(data={"uid": doctor.id, "role": "doctor"})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token}
    )
    
    

@router.post("/update_profile",response_model=DetailResponse)
async def update_profile(user_data: DoctorProfileUpdate, doctor: Doctor|None = Depends(get_current_doctor), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(doctor, JSONResponse):
        return doctor

    if user_data.email:
        existing_email = await session.execute(
            select(Doctor).where(Doctor.email == user_data.email, Doctor.id != doctor.id)
        )
        if existing_email.scalar_one_or_none() is not None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'detail': "Почта уже занята"}
            )
    
    if user_data.email is not None and doctor.email != user_data.email:
        doctor.email = user_data.email
    if user_data.first_name is not None and doctor.first_name != user_data.first_name:
        doctor.first_name = user_data.first_name
    if user_data.last_name is not None and doctor.last_name != user_data.last_name:
        doctor.last_name = user_data.last_name
    if user_data.gender is not None and doctor.gender != user_data.gender:
        doctor.gender = user_data.gender
    if user_data.experience_age is not None and doctor.experience_age != user_data.experience_age:
        doctor.experience_age = user_data.experience_age
    if user_data.age is not None and doctor.age != user_data.age:
        doctor.age = user_data.age
    if user_data.university is not None and doctor.university != user_data.university:
        doctor.university = user_data.university
    if user_data.speciality is not None and doctor.speciality != user_data.speciality:
        doctor.speciality = user_data.speciality


    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Профиль упсешно обновлен"}
    )



@router.post("/edit_password",response_model=DetailResponse)
async def edit_password(user_data: PasswordChange, doctor: Doctor|None = Depends(get_current_doctor), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(doctor, JSONResponse):
        return doctor
    
    if user_data.new_password != user_data.confirm_password:
        return JSONResponse(
            status=status.HTTP_400_BAD_REQUEST,
            detail="Пароли не совпадают"
        )
    
    # Проверка длины и наличия символов в новом пароле
    if len(user_data.new_password) < 8:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать минимум 8 символов."}
        )
    if not any(char.isdigit() for char in user_data.new_password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать хотя бы одну цифру."}
        )
    if not any(char.isalpha() for char in user_data.new_password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароль должен содержать хотя бы одну букву."}
        )

        
    # Проверка пароля
    if not doctor.verify_password(user_data.current_password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неправильная почта или пароль"}
        )
    
    doctor.set_password(user_data.new_password)
    await session.commit()
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Пароль успешно изменен"}
    )


@router.post("/logout",response_model=DetailResponse)
async def logout(token: str = Depends(get_jwt_doctor)) -> JSONResponse:
    
    exists = await redis_fastapi.exists(token)
    if exists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Вы уже вышли с аккаунта"}
        )
        
    await redis_fastapi.setex(name=token, time=ACCESS_TOKEN_EXPIRE_MINUTES*60, value="blacklisted")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Успешный выход"}
    )


@router.get("/get_doctor/{doctor_id}", response_model=DoctorRead)
async def get_doctor_by_id(doctor_id : int, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    result = await session.execute(select(Doctor).where(Doctor.id == doctor_id))
    
    # Extract the first user from the result
    doctor = result.scalars().first()  # Use scalars() to get the actual user object

    # Check if the user exists
    if doctor is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Врач не найден"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=DoctorRead.model_validate(doctor).model_dump()
    )

@router.get("/get_me", response_model=DoctorRead)
async def get_me(doctor: Doctor|None = Depends(get_current_doctor), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(doctor, JSONResponse):
        return doctor
    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=DoctorRead.model_validate(doctor).model_dump()
    )

@router.get("/get_all_doctors", response_model=List[DoctorRead])
async def get_doctors(session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    doctors = await session.execute(select(Doctor))
    
    all_doctors = [
        DoctorRead.model_validate(doctor).model_dump()
        for doctor in (doctors.scalars().all())
    ]
    
    return all_doctors

  
  
@router.post("/send_new", response_model=DoctorScanResponse)
async def scan(new_scan: DoctorScanAddNew, doctor: Doctor|None = Depends(get_current_doctor), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(doctor, JSONResponse):
        return doctor
    
    new_message = DoctorScan(
        sender_id=doctor.id,
        gender=new_scan.gender,
        age=new_scan.age,
        body_part=new_scan.body_part,
        image_base64=new_scan.image_base64,
    )
    
    session.add(new_message)
    await session.commit()  # Подтверждаем изменения в базе данных
    await session.refresh(new_message)  # Обновляем экземпляр, чтобы получить новые значения (например, ID)
    
    '''
    обработка сообщения с помощью нейронки
    '''
    ai_aswer = await validate_body_scan(image_base64=new_message.image_base64)
    
    new_message.contains_skin = ai_aswer['contains_skin']
    new_message.ai_result = ai_aswer['description']
    await session.commit()
    
    if not new_message.contains_skin:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "id": new_message.id,
                "detail": new_message.ai_result,
            }
        )
    
    result = await run_in_threadpool(get_result,age=int(new_message.age),gender=new_message.gender,body_part=new_scan.body_part,image_base64=new_message.image_base64)
    
    more_info = await generate_user_report(
        gender = new_scan.gender,
        age = new_scan.age,
        skin_type = None,
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