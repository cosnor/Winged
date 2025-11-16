import os
from fastapi import APIRouter, HTTPException
import httpx
from ..schemas import SightingRequest, SightingResponse

router = APIRouter(prefix="/sightings", tags=["sightings"])

SIGHTINGS_URL = os.getenv("SIGHTINGS_URL", "http://sightings:8002")


@router.post("/", response_model=SightingResponse)
async def create_sighting(sighting: SightingRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{SIGHTINGS_URL}/sightings/", json=sighting.dict())
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return resp.json()


@router.get("/{sighting_id}")
async def get_sighting(sighting_id: int):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{SIGHTINGS_URL}/sightings/{sighting_id}")
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return resp.json()
