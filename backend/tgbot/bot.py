from aiogram import Bot, Dispatcher, types
from src.config import NOTIFICATIONS_TGBOT_TOKEN
from sqlalchemy import update, select
from src.database import get_async_session
from src.logger import logger
from src.auth.models import User

bot = Bot(token=NOTIFICATIONS_TGBOT_TOKEN)
dp = Dispatcher(bot)

@dp.errors_handler()
async def error_handler(update, exception):
    # Логируем информацию об обновлении и исключении
    logger.error(f'An error occurred while processing update {update}: {exception}')
    return True  # Возвращаем True, чтобы обработать ошибку

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('привет')
    args = message.get_args()
    if args:
        target_id = int(args)
    
        tg_id = message.from_user.id
        # Проверяем наличие аргумента (id строки)
        
        # Обновляем поле tg_id у записи с указанным id
        
        async for session in get_async_session():
            user_exists = await session.execute(select(User).where(User.id==target_id))
            user_exists = user_exists.scalar_one_or_none()
            if user_exists == None:
                return False
            stmt = (
                update(User)
                .where(User.id == target_id)
                .values(tg_id=tg_id)
            )
            # Выполняем запрос через сессию
            await session.execute(stmt)
            await session.commit()
        
        await message.answer(f"{user_exists.last_name} {user_exists.first_name}, вы успешно привязали свой телеграм аккаунт к учетной записи.")
     


# async def schedule_tg_message(tg_id: int, text: str, seconds: int):
#     """Функция для планирования отправки сообщения в Telegram через указанное количество секунд."""
#     logger.info(f"Запланировано сообщение для {tg_id}: '{text}' через {seconds} секунд.")
#     await asyncio.sleep(seconds)
#     logger.info(f"дошел до отправки")
#     await bot.send_message(tg_id, text)  # Запускаем задачу в фоновом режиме
    