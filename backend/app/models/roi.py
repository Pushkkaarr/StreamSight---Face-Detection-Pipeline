import uuid
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class ROIDetection(Base):
    __tablename__ = "roi_detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    frame_index = Column(Integer, nullable=False)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    frame_width = Column(Integer, nullable=False)
    frame_height = Column(Integer, nullable=False)
