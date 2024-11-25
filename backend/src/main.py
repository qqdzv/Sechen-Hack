from fastapi_cache.backends.redis import RedisCacheBackend
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as router_user
from src.ai_bot.router import router as router_ai
from src.scan.router import router as router_scan
from src.doctor.router import router as router_doctor
from src.messages.router import router as router_messages
from src.private_api.router import router as router_shared
from tgbot.bot import dp
from src.myredis import redis_fastapi
import asyncio
import time

templates = Jinja2Templates(directory="src/templates")

async def start_tgbot():
    await dp.start_polling()
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    time.sleep(3)
    bot_task = asyncio.create_task(start_tgbot())
    RedisCacheBackend(redis_fastapi)
    yield
    
    bot_task.cancel()
    await bot_task

app = FastAPI(
    title="Test",
    lifespan=lifespan,
    root_path="/api",
)
    
app.include_router(router_scan)
app.include_router(router_user)
app.include_router(router_doctor)
app.include_router(router_ai)
app.include_router(router_messages)
app.include_router(router_shared)

origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "https://d037-185-244-218-22.ngrok-free.app",
    "https://skin-cancer.ru"
]

app.add_middleware(
    CORSMiddleware,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
    allow_origins=['*'],
)

