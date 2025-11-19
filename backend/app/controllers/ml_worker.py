import os
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
import httpx

from ..schemas import HeatmapResponse, BirdIdentificationResponse

router = APIRouter(prefix="/ml_worker", tags=["ml_worker"])

ML_WORKER_URL = os.getenv("ML_WORKER_URL", "http://ml_worker:8003")


@router.post("/identify-bird", response_model=BirdIdentificationResponse)
async def identify_bird(
	audio: UploadFile = File(...),
	user_id: Optional[int] = Query(None),
	latitude: Optional[float] = Query(None),
	longitude: Optional[float] = Query(None),
):
	"""Proxy endpoint: forward uploaded audio and params to the ML worker service

	Accepts multipart/form-data with field `audio` (file) and optional query
	params `user_id`, `latitude`, `longitude`. Returns the ML worker's
	identification response.
	"""
	# Basic validation of uploaded file
	if not audio.filename:
		raise HTTPException(status_code=400, detail="Missing audio file")

	try:
		file_bytes = await audio.read()
	except Exception:
		raise HTTPException(status_code=400, detail="Unable to read uploaded file")

	# Forward to ML worker service as multipart/form-data
	files = {"audio": (audio.filename, file_bytes, audio.content_type or "application/octet-stream")}
	params = {}
	if user_id is not None:
		params["user_id"] = str(user_id)
	if latitude is not None:
		params["latitude"] = str(latitude)
	if longitude is not None:
		params["longitude"] = str(longitude)

	async with httpx.AsyncClient(timeout=30.0) as client:
		try:
			resp = await client.post(f"{ML_WORKER_URL}/identify-bird", files=files, params=params)
		except httpx.RequestError:
			raise HTTPException(status_code=503, detail="ML worker service unavailable")

	if resp.status_code >= 400:
		# forward upstream error body when possible
		detail = None
		try:
			detail = resp.json()
		except Exception:
			detail = resp.text
		raise HTTPException(status_code=resp.status_code, detail=detail)

	try:
		body = resp.json()
	except Exception:
		raise HTTPException(status_code=502, detail="ML worker returned invalid JSON")

	# unwrap wrapper { success, message, data }
	if isinstance(body, dict) and "data" in body:
		body = body.get("data") or {}

	return body

