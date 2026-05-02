from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.roi import ROIDetection
from app.schemas.roi import ROIDetectionCreate
from uuid import UUID
from typing import List, Optional

class ROIStore:
    @staticmethod
    async def create_roi(db: AsyncSession, roi_in: ROIDetectionCreate) -> ROIDetection:
        db_roi = ROIDetection(**roi_in.model_dump())
        db.add(db_roi)
        await db.commit()
        await db.refresh(db_roi)
        return db_roi

    @staticmethod
    async def get_rois(db: AsyncSession, session_id: Optional[UUID] = None, limit: int = 50, offset: int = 0) -> List[ROIDetection]:
        query = select(ROIDetection).order_by(ROIDetection.detected_at.desc()).limit(limit).offset(offset)
        if session_id:
            query = query.where(ROIDetection.session_id == session_id)
        
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_roi(db: AsyncSession, roi_id: UUID) -> Optional[ROIDetection]:
        query = select(ROIDetection).where(ROIDetection.id == roi_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_stats(db: AsyncSession) -> dict:
        total_q = select(func.count(ROIDetection.id))
        avg_conf_q = select(func.avg(ROIDetection.confidence))
        avg_area_q = select(func.avg(ROIDetection.width * ROIDetection.height))
        
        min_max_time_q = select(func.min(ROIDetection.detected_at), func.max(ROIDetection.detected_at))
        
        total = (await db.execute(total_q)).scalar() or 0
        avg_conf = (await db.execute(avg_conf_q)).scalar() or 0.0
        avg_area = (await db.execute(avg_area_q)).scalar() or 0.0
        
        times = (await db.execute(min_max_time_q)).first()
        dps = 0.0
        if times and times[0] and times[1] and total > 1:
            diff = (times[1] - times[0]).total_seconds()
            if diff > 0:
                dps = total / diff
                
        return {
            "total_detections": total,
            "average_confidence": float(avg_conf),
            "average_area": float(avg_area),
            "detections_per_second": float(dps)
        }
