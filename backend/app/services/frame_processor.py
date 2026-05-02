import io
from PIL import Image, ImageDraw
from app.services.face_detector import DetectionResult
from app.config import settings

class FrameProcessor:
    @staticmethod
    def process_and_draw(image_bytes: bytes, detection: DetectionResult) -> bytes:
        if not detection.found:
            return image_bytes
            
        try:
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            draw = ImageDraw.Draw(image)
            
            x1 = detection.x
            y1 = detection.y
            x2 = detection.x + detection.width
            y2 = detection.y + detection.height
            
            draw.rectangle([x1, y1, x2, y2], outline="#00FF41", width=2)
            
            out_io = io.BytesIO()
            image.save(out_io, format="JPEG", quality=settings.JPEG_QUALITY)
            return out_io.getvalue()
        except Exception:
            return image_bytes
