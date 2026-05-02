import pytest
import io
from PIL import Image
from app.services.face_detector import FaceDetector, DetectionResult

def test_no_face_detection():
    detector = FaceDetector()
    img = Image.new("RGB", (640, 480), "white")
    bio = io.BytesIO()
    img.save(bio, format="JPEG")
    image_bytes = bio.getvalue()
    
    result = detector.detect(image_bytes)
    
    assert isinstance(result, DetectionResult)
    assert result.found is False
    assert result.x == 0
    assert result.y == 0
    assert result.width == 0
    assert result.height == 0
    assert result.confidence == 0.0
    assert result.frame_width == 640
    assert result.frame_height == 480
