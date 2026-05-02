import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_get_rois():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/roi")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_nonexistent_roi():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        nonexistent = uuid.uuid4()
        response = await ac.get(f"/api/roi/{nonexistent}")
        assert response.status_code == 404
