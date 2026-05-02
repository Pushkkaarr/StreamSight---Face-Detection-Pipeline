from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.queue import frame_queue
from app.services.face_detector import FaceDetector
from app.services.frame_processor import FrameProcessor
from app.services.roi_store import ROIStore
from app.schemas.roi import ROIDetectionCreate
from app.database import AsyncSessionLocal
import uuid
import logging
import asyncio

router = APIRouter()
logger = logging.getLogger(__name__)
face_detector = FaceDetector()

MAX_SIZE = 5 * 1024 * 1024

@router.websocket("/ws/ingest")
async def ingest_video(websocket: WebSocket):
    await websocket.accept()
    session_id = uuid.uuid4()
    frame_index = 0
    
    try:
        while True:
            try:
                message = await websocket.receive_bytes()
            except RuntimeError as e:
                if "WebSocket is not connected" in str(e):
                    break
                raise
                
            if len(message) > MAX_SIZE:
                await websocket.send_json({"error": "Message too large"})
                continue
                
            detection = face_detector.detect(message)
            
            processed_frame = FrameProcessor.process_and_draw(message, detection)
            
            try:
                frame_queue.put_nowait(processed_frame)
            except asyncio.QueueFull:
                try:
                    frame_queue.get_nowait()
                    frame_queue.put_nowait(processed_frame)
                except Exception:
                    pass
            
            if detection.found:
                roi_create = ROIDetectionCreate(
                    session_id=session_id,
                    frame_index=frame_index,
                    x=detection.x,
                    y=detection.y,
                    width=detection.width,
                    height=detection.height,
                    confidence=detection.confidence,
                    frame_width=detection.frame_width,
                    frame_height=detection.frame_height
                )
                try:
                    async with AsyncSessionLocal() as db:
                        await ROIStore.create_roi(db, roi_create)
                except Exception as e:
                    logger.error(f"DB Error storing ROI: {e}")
            
            frame_index += 1
            
    except WebSocketDisconnect:
        logger.info(f"Ingest client disconnected: {session_id}")
    except Exception as e:
        logger.error(f"Error in ingest: {e}")
