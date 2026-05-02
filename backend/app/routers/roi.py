from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.schemas.roi import ROIDetectionResponse, ROIStats
from app.services.roi_store import ROIStore
from app.core.security import limiter

router = APIRouter(prefix="/api/roi", tags=["ROI"])

@router.get("", response_model=List[ROIDetectionResponse])
@limiter.limit("100/minute")
async def get_rois(
    request: Request,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        rois = await ROIStore.get_rois(db, session_id=session_id, limit=limit, offset=offset)
        return rois
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=ROIStats)
@limiter.limit("100/minute")
async def get_roi_stats(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        stats = await ROIStore.get_stats(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{roi_id}", response_model=ROIDetectionResponse)
@limiter.limit("100/minute")
async def get_roi(request: Request, roi_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        roi = await ROIStore.get_roi(db, roi_id)
        if not roi:
            raise HTTPException(status_code=404, detail="ROI not found")
        return roi
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
