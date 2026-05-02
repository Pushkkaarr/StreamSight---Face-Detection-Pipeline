import asyncio
from app.config import settings

frame_queue = asyncio.Queue(maxsize=settings.MAX_QUEUE_SIZE)
