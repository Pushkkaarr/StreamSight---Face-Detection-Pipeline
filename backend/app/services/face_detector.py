from dataclasses import dataclass
import io
import numpy as np
from PIL import Image
import mediapipe as mp

@dataclass
class DetectionResult:
    found: bool
    x: int
    y: int
    width: int
    height: int
    confidence: float
    frame_width: int
    frame_height: int

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=min_detection_confidence
        )

    def detect(self, image_bytes: bytes) -> DetectionResult:
        frame_width, frame_height = 0, 0
        try:
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            frame_width, frame_height = image.size
            image_np = np.array(image)
            
            results = self.face_detection.process(image_np)
            
            if results and results.detections:
                detection = results.detections[0]
                bboxC = detection.location_data.relative_bounding_box
                
                x = int(bboxC.xmin * frame_width)
                y = int(bboxC.ymin * frame_height)
                width = int(bboxC.width * frame_width)
                height = int(bboxC.height * frame_height)
                confidence = detection.score[0]
                
                return DetectionResult(
                    found=True,
                    x=x, y=y, width=width, height=height,
                    confidence=float(confidence),
                    frame_width=frame_width,
                    frame_height=frame_height
                )
        except Exception:
            pass
            
        return DetectionResult(
            found=False,
            x=0, y=0, width=0, height=0,
            confidence=0.0,
            frame_width=frame_width,
            frame_height=frame_height
        )
