from src.config import TG_ID_ADMIN, TGBOT_TOKEN_ADMIN
from loguru import logger
import aiohttp
import asyncio
import sys


# Админские логи в тг телеграм и запись их в файл hh-test.log
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TGBOT_TOKEN_ADMIN}/sendMessage"

async def send_log_to_telegram(message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(TELEGRAM_API_URL, data={'chat_id': TG_ID_ADMIN, 'text': message}) as response:
                if response.status != 200:
                    logger.error(f"Failed to send log to Telegram: {await response.text()}")
        except Exception as e:
            logger.error(f"Failed to send log to Telegram: {e}")

def send_log(message):
    loop = asyncio.get_event_loop()
    # loop.create_task(send_log_to_telegram(message))

def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")
    logger.add("hh-test.log", rotation="50 MB", compression="zip", format=format_info, level="TRACE")
    
    logger.add(
        send_log,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        filter=lambda record: record['level'].name == 'INFO'
    )
            
logging_setup()
