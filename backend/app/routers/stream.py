from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.queue import frame_queue
import asyncio
import logging
from typing import Set

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: bytes):
        for connection in list(self.active_connections):
            try:
                await connection.send_bytes(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

async def broadcast_frames():
    while True:
        try:
            try:
                frame = await asyncio.wait_for(frame_queue.get(), timeout=1.0)
                if manager.active_connections:
                    await manager.broadcast(frame)
            except asyncio.TimeoutError:
                if manager.active_connections:
                    await manager.broadcast(b"keepalive")
        except Exception as e:
            logger.error(f"Error broadcasting frame: {e}")
            await asyncio.sleep(0.1)

@router.websocket("/ws/stream")
async def stream_video(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
