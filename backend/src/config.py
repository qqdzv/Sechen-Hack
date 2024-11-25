from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
TGBOT_TOKEN_ADMIN = os.environ.get('TGBOT_TOKEN_ADMIN')
TG_ID_ADMIN = os.environ.get('TG_ID_ADMIN')
SECRET_JWT = os.environ.get('SECRET_JWT')
NOTIFICATIONS_TGBOT_TOKEN = os.environ.get('NOTIFICATIONS_TGBOT_TOKEN')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

CHAT_BOT_API = os.environ.get('CHAT_BOT_API')