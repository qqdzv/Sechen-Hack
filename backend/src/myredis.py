from src.config import REDIS_HOST,REDIS_PORT
from redis import asyncio as aioredis


redis_fastapi = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")