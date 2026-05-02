from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class ROIDetectionBase(BaseModel):
    session_id: UUID
    frame_index: int
    x: int
    y: int
    width: int
    height: int
    confidence: float
    frame_width: int
    frame_height: int

class ROIDetectionCreate(ROIDetectionBase):
    pass

class ROIDetectionResponse(ROIDetectionBase):
    id: UUID
    detected_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ROIStats(BaseModel):
    total_detections: int
    average_confidence: float
    average_area: float
    detections_per_second: float
