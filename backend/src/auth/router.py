
from fastapi import APIRouter,Depends,status

from sqlalchemy import select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

from src.auth.models import User
from pydantic import BaseModel

from src.test.schemas import TestBase
from src.test.models import Test

from src.auth.base_config import create_access_token
from src.auth.base_config import get_current_user, get_jwt_user
from fastapi.responses import JSONResponse
from src.auth.schemas import UserCreate, UserLogin, UserProfileUpdate, PasswordChange, UserRead
from src.myredis import redis_fastapi
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.logger import logger

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

class JWTResponse(BaseModel):
    access_token : str

class DetailResponse(BaseModel):
    detail: str

@router.post("/login", response_model=JWTResponse)
async def login(login_form: UserLogin, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    result = await session.execute(select(User).where(User.email == login_form.email))
    user = result.scalar_one_or_none()
    
    if user is None or not user.verify_password(login_form.password):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Неправильная почта или пароль"}
        )
    
    token = create_access_token(data={"uid": user.id, "role": "user"})
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token}
    )


@router.post("/register", response_model=JWTResponse)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    existing_email = await session.execute(select(User).where(User.email == user_data.email))
    if existing_email.scalar_one_or_none() is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Почта уже занята"}
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


    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        gender=user_data.gender,
        skin_type=user_data.skin_type.value,
        age=user_data.age
    )
    
    user.set_password(user_data.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    token = create_access_token(data={"uid": user.id, "role": "user"})

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"access_token": token}
    )

    
    

@router.post("/update_profile", response_model=DetailResponse)
async def update_profile(user_data: UserProfileUpdate, user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user

    if user_data.email:
        existing_email = await session.execute(
            select(User).where(User.email == user_data.email, User.id != user.id)
        )
        if existing_email.scalar_one_or_none() is not None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'detail':"Почта уже занята"}
            )
    
    
    if user_data.email is not None and user.email != user_data.email:
        user.email = user_data.email
    if user_data.first_name is not None and user.first_name != user_data.first_name:
        user.first_name = user_data.first_name
    if user_data.last_name is not None and user.last_name != user_data.last_name:
        user.last_name = user_data.last_name
    if user_data.gender is not None and user.gender != user_data.gender:
        user.gender = user_data.gender
    if user_data.skin_type is not None and user.skin_type != user_data.skin_type:
        user.skin_type = user_data.skin_type
    if user_data.age is not None and user.age != user_data.age:
        user.age = user_data.age


    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail':"Профиль успешно обновлен"}
    )


@router.post("/edit_password", response_model=DetailResponse)
async def edit_password(user_data: PasswordChange, user: User|None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user
    
    if user_data.new_password != user_data.confirm_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Пароли не совпадают"}
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

    # Проверка текущего пароля
    if not user.verify_password(user_data.current_password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неправильная почта или пароль"}
        )
    
    user.set_password(user_data.new_password)
    await session.commit()
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Пароль успешно изменен"}
    )



@router.post("/logout", response_model=DetailResponse)
async def logout(token: str = Depends(get_jwt_user)) -> JSONResponse:
    
    exists = await redis_fastapi.exists(token)
    if exists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Вы уже вышли с аккаунта"}
        )
        
    await redis_fastapi.setex(name=token, time=ACCESS_TOKEN_EXPIRE_MINUTES * 60, value="blacklisted")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Успешный выход"}
    )


@router.get("/get_user/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    # Execute the query to get the user
    result = await session.execute(select(User).where(User.id == user_id))
    
    # Extract the first user from the result
    user = result.scalars().first()  # Use scalars() to get the actual user object
    
    # Check if the user exists
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Пользователь не найден"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=UserRead.model_validate(user).model_dump()
    )


@router.get("/get_me", response_model=UserRead)
async def get_me(user: User | None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    
    if isinstance(user, JSONResponse):
        return user
    
    # Check if the user has an associated test
    existing_test = await session.execute(
        select(Test).filter(Test.user_id == user.id)
    )
    existing_test = existing_test.scalar_one_or_none()
    logger.info(existing_test)
    
    # Convert the user to a dictionary and add the `has_test` field
    user_data = user.__dict__  # Copy to avoid mutating the original
    user_data['has_test'] = bool(existing_test)
    
    # Return the response as JSON with the updated user data
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=UserRead.model_validate(user_data).model_dump()
    )


  
@router.post("/test", response_model=DetailResponse)
async def upload_test(test: TestBase, user: User | None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    # Check if the `get_current_user` dependency returned a JSON response
    if isinstance(user, JSONResponse):
        return user
    
    # Create a new test instance
    new_test = Test(
        user_id=user.id,
        task1=test.task1,
        task2=test.task2,
        task3=test.task3,
        task4=test.task4,
        task5=test.task5,
        task6=test.task6,
        task7=test.task7
    )
    
    # Add the new test instance to the session
    session.add(new_test)
    await session.commit()  # Commit the new test instance
    await session.refresh(new_test)  # Refresh to get updated fields (e.g., `id`)
    
    # Remove any old test instances for this user except the newly created one
    await session.execute(
        delete(Test).filter(Test.user_id == user.id, Test.id != new_test.id)
    )
    await session.commit()  # Commit the deletion of old tests

    # Return a success message as JSON response
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Тест успешно пройден"}
    )

@router.get("/set_notification", response_model=DetailResponse)
async def set_notification(user: User | None = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    if isinstance(user, JSONResponse):
        return user
    
    if not user.tg_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'detail':"Вы не привязали свой телеграм аккаунт."}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail':"Успешно поставлено напоминание через 30 дней."}
    )