import os
from fastapi import APIRouter, HTTPException
import httpx

from ..schemas import HeatmapResponse

router = APIRouter(prefix="/maps", tags=["maps"])

MAPS_URL = os.getenv("MAPS_URL", "http://maps:8004")


@router.get("/heatmap", response_model=HeatmapResponse)
async def get_heatmap():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{MAPS_URL}/maps/heatmap")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
