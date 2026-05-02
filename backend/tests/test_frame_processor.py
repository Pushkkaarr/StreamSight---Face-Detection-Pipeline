import pytest
import io
from PIL import Image
from app.services.frame_processor import FrameProcessor
from app.services.face_detector import DetectionResult

def test_frame_processor_no_face():
    img = Image.new("RGB", (640, 480), "white")
    bio = io.BytesIO()
    img.save(bio, format="JPEG")
    image_bytes = bio.getvalue()
    
    detection = DetectionResult(found=False, x=0, y=0, width=0, height=0, confidence=0.0, frame_width=640, frame_height=480)
    result_bytes = FrameProcessor.process_and_draw(image_bytes, detection)
    
    assert result_bytes == image_bytes

def test_frame_processor_with_face():
    img = Image.new("RGB", (640, 480), "white")
    bio = io.BytesIO()
    img.save(bio, format="JPEG")
    image_bytes = bio.getvalue()
    
    detection = DetectionResult(found=True, x=10, y=10, width=100, height=100, confidence=0.9, frame_width=640, frame_height=480)
    result_bytes = FrameProcessor.process_and_draw(image_bytes, detection)
    
    assert len(result_bytes) > 0
    
    reopened = Image.open(io.BytesIO(result_bytes))
    assert reopened.size == (640, 480)
