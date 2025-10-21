from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import logging
import os
import tempfile
from typing import Optional, List, Dict, Any
import httpx
from datetime import datetime
from pydantic import BaseModel

# Import integrations
from .services.achievements_client import AchievementsServiceClient, SightingsServiceClient
from .integrations.birdnet_client import BirdNetServiceClient, BirdNetToWingedIntegrator
from .integrations.birdnet_database import BirdNetDatabaseClient, BirdNetDataSyncer
from .models.species_mapping import SPECIES_MAPPING, get_species_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Winged ML Worker Service",
    description="Machine Learning worker service for bird identification and achievements integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
ACHIEVEMENTS_URL = os.getenv("ACHIEVEMENTS_SERVICE_URL", "http://achievements:8006")
SIGHTINGS_URL = os.getenv("SIGHTINGS_SERVICE_URL", "http://sightings:8002")
BIRDNET_API_URL = os.getenv("BIRDNET_API_URL", "http://host.docker.internal:8000")

# MongoDB configuration for BirdNet database integration  
MONGODB_URL = os.getenv("BIRDNET_MONGODB_URL", "mongodb://admin:birdnet123@host.docker.internal:27017/birdnet_db?authSource=admin")
MONGODB_DATABASE = os.getenv("BIRDNET_DATABASE_NAME", "birdnet_db")
SESSIONS_COLLECTION = os.getenv("BIRDNET_SESSIONS_COLLECTION", "sessions")
DETECTIONS_COLLECTION = os.getenv("BIRDNET_DETECTIONS_COLLECTION", "detections")

# Response models
class BirdIdentificationResponse(BaseModel):
    species: str
    confidence: float
    species_code: Optional[str] = None
    common_name: Optional[str] = None
    scientific_name: Optional[str] = None
    achievements_triggered: List[str] = []
    sighting_created: bool = False

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    dependencies: Dict[str, str]

class BirdNetSessionRequest(BaseModel):
    session_id: str
    user_id: Optional[int] = None
    process_achievements: bool = True

class DatabaseSyncRequest(BaseModel):
    limit: int = 50
    min_confidence: float = 0.7
    default_user_id: Optional[int] = None

class UserSyncRequest(BaseModel):
    winged_user_id: int
    limit: int = 50
    min_confidence: float = 0.7

# Global clients (initialized on startup)
achievements_client = None
sightings_client = None
birdnet_client = None
database_client = None
integrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize service clients on startup"""
    global achievements_client, sightings_client, birdnet_client, database_client, integrator
    
    logger.info("Initializing ML Worker Service...")
    
    # Initialize HTTP clients
    achievements_client = AchievementsServiceClient(base_url=ACHIEVEMENTS_URL)
    sightings_client = SightingsServiceClient(base_url=SIGHTINGS_URL)
    birdnet_client = BirdNetServiceClient(base_url=BIRDNET_API_URL)
    
    # Initialize database client if MongoDB URL is provided
    if MONGODB_URL:
        database_client = BirdNetDatabaseClient(
            mongodb_url=MONGODB_URL,
            database_name=MONGODB_DATABASE,
            sessions_collection=SESSIONS_COLLECTION,
            detections_collection=DETECTIONS_COLLECTION
        )
        await database_client.connect()
        logger.info("BirdNet database client initialized")
    else:
        logger.warning("MongoDB URL not provided - database integration disabled")
    
    # Initialize integrator
    integrator = BirdNetToWingedIntegrator(
        achievements_client=achievements_client,
        sightings_client=sightings_client
    )
    
    logger.info("ML Worker Service initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global database_client
    
    if database_client:
        await database_client.disconnect()
    
    logger.info("ML Worker Service shutdown complete")

def simulate_bird_identification(audio_data: bytes) -> Dict[str, Any]:
    """
    Simulate bird identification using a mock ML model
    In production, this would use actual BirdNet or similar ML model
    """
    
    # Mock species detection - in production this would be real ML inference
    mock_species = [
        ("RUBHUM", "Ruby-throated Hummingbird", 0.85),
        ("AMECRO", "American Crow", 0.78),
        ("NORCAD", "Northern Cardinal", 0.92),
        ("BLUJAY", "Blue Jay", 0.71),
        ("AMEGFI", "American Goldfinch", 0.88),
        ("HOUFIN", "House Finch", 0.76),
        ("MOUWAR", "Mourning Warbler", 0.83),
        ("REHWOO", "Red-headed Woodpecker", 0.79)
    ]
    
    # Simulate processing based on audio characteristics
    np.random.seed(len(audio_data) % 1000)
    species_code, common_name, base_confidence = np.random.choice(
        len(mock_species), p=[0.15, 0.12, 0.18, 0.1, 0.15, 0.1, 0.12, 0.08]
    )[mock_species]
    
    # Add some randomness to confidence
    confidence = max(0.5, min(0.99, base_confidence + np.random.normal(0, 0.05)))
    
    return {
        "species_code": species_code,
        "common_name": common_name,
        "confidence": confidence
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    
    dependencies = {}
    
    # Check achievements service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{ACHIEVEMENTS_URL}/health")
            dependencies["achievements"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        dependencies["achievements"] = "unavailable"
    
    # Check sightings service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{SIGHTINGS_URL}/health")
            dependencies["sightings"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        dependencies["sightings"] = "unavailable"
    
    # Check BirdNet API
    try:
        if birdnet_client:
            health_status = await birdnet_client.health_check()
            dependencies["birdnet_api"] = "healthy" if health_status else "unhealthy"
        else:
            dependencies["birdnet_api"] = "not_configured"
    except Exception:
        dependencies["birdnet_api"] = "unavailable"
    
    # Check database connection
    if database_client:
        try:
            is_connected = await database_client.is_connected()
            dependencies["birdnet_database"] = "healthy" if is_connected else "unhealthy"
        except Exception:
            dependencies["birdnet_database"] = "unavailable"
    else:
        dependencies["birdnet_database"] = "not_configured"
    
    return HealthResponse(
        status="healthy",
        service="ml_worker",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        dependencies=dependencies
    )

@app.post("/identify-bird", response_model=BirdIdentificationResponse)
async def identify_bird(
    audio: UploadFile = File(...),
    user_id: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    """
    Identify bird from audio file and trigger achievements
    """
    
    if not audio.content_type or not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    try:
        # Read audio data
        audio_data = await audio.read()
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Perform bird identification
        identification = simulate_bird_identification(audio_data)
        
        # Get species information
        species_info = get_species_info(identification["species_code"])
        
        response = BirdIdentificationResponse(
            species=identification["common_name"],
            confidence=identification["confidence"],
            species_code=identification["species_code"],
            common_name=species_info.get("common_name", identification["common_name"]),
            scientific_name=species_info.get("scientific_name", "Unknown"),
            achievements_triggered=[],
            sighting_created=False
        )
        
        # Process achievements if user_id is provided
        if user_id and achievements_client and sightings_client:
            try:
                # Create sighting first
                sighting_data = {
                    "user_id": user_id,
                    "species_code": identification["species_code"],
                    "species_name": identification["common_name"],
                    "confidence": identification["confidence"],
                    "latitude": latitude,
                    "longitude": longitude,
                    "recorded_at": datetime.utcnow().isoformat()
                }
                
                sighting_result = await sightings_client.create_sighting(sighting_data)
                response.sighting_created = bool(sighting_result)
                
                # Process achievements
                achievement_data = {
                    "user_id": user_id,
                    "species_detected": identification["species_code"],
                    "confidence": identification["confidence"],
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude
                    } if latitude and longitude else None
                }
                
                achievements = await achievements_client.process_species_detection(achievement_data)
                if achievements:
                    response.achievements_triggered = [ach.get("name", "Unknown") for ach in achievements]
                
            except Exception as e:
                logger.warning(f"Failed to process achievements for user {user_id}: {e}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in bird identification: {e}")
        raise HTTPException(status_code=500, detail=f"Identification failed: {str(e)}")

@app.post("/birdnet/analyze-audio", response_model=BirdIdentificationResponse)
async def analyze_audio_with_birdnet(
    audio: UploadFile = File(...),
    user_id: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    """
    Analyze audio file using BirdNET microservice and trigger achievements
    """
    
    if not birdnet_client:
        raise HTTPException(status_code=503, detail="BirdNet microservice client not configured")
    
    if not audio.content_type or not audio.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    try:
        # Read audio data
        audio_data = await audio.read()
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Save audio to temporary file for BirdNET analysis
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Create a session for processing via BirdNET microservice
            import uuid
            session_id = str(uuid.uuid4())
            
            # You can implement WebSocket communication or use REST API
            # For now, let's use the session-based approach
            
            # Process the audio and get recent detections
            recent_sessions = await birdnet_client.get_recent_sessions(limit=1, hours_back=1)
            
            if not recent_sessions:
                # No recent sessions found - this would be improved with direct audio upload
                logger.warning("No recent BirdNET sessions found")
                raise HTTPException(status_code=404, detail="No recent bird detections available")
            
            # Get the most recent session
            latest_session = recent_sessions[0]
            session_detections = await birdnet_client.get_session_detections(latest_session['session_id'])
            
            if not session_detections:
                raise HTTPException(status_code=404, detail="No detections found in recent session")
            
            # Get the best detection (highest confidence)
            best_detection = max(session_detections, key=lambda x: x.get('confidence', 0))
            
            # Get species information
            species_code = best_detection.get('species_code', '')
            species_info = get_species_info(species_code)
            
            response = BirdIdentificationResponse(
                species=best_detection.get('species_name', 'Unknown'),
                confidence=best_detection.get('confidence', 0.0),
                species_code=species_code,
                common_name=species_info.get('common_name', best_detection.get('species_name', 'Unknown')),
                scientific_name=species_info.get('scientific_name', 'Unknown'),
                achievements_triggered=[],
                sighting_created=False
            )
            
            # Process achievements if user_id is provided
            if user_id and achievements_client:
                try:
                    detection_data = {
                        "user_id": user_id,
                        "species_name": best_detection.get('species_name', 'Unknown'),
                        "confidence": best_detection.get('confidence', 0.0),
                        "location": {"latitude": latitude or 0.0, "longitude": longitude or 0.0},
                        "detection_time": datetime.now().isoformat()
                    }
                    
                    achievements = await achievements_client.process_species_detection(detection_data)
                    if achievements:
                        response.achievements_triggered = [ach.get("name", "Unknown") for ach in achievements]
                        
                    # Create sighting record if sightings client is available
                    if sightings_client:
                        sighting_data = {
                            "user_id": user_id,
                            "species_name": best_detection.get('species_name', 'Unknown'),
                            "location": {"lat": latitude or 0.0, "lon": longitude or 0.0},
                            "confidence": best_detection.get('confidence', 0.0),
                            "timestamp": datetime.now().isoformat(),
                            "source": "birdnet_microservice"
                        }
                        
                        sighting_result = await sightings_client.create_sighting(sighting_data)
                        if sighting_result:
                            response.sighting_created = True
                
                except Exception as e:
                    logger.warning(f"Failed to process achievements/sightings for user {user_id}: {e}")
            
            return response
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in BirdNET audio analysis: {e}")
        raise HTTPException(status_code=500, detail=f"BirdNET analysis failed: {str(e)}")

# BirdNet HTTP API Integration endpoints
@app.post("/birdnet/process-session")
async def process_birdnet_session(request: BirdNetSessionRequest):
    """Process a BirdNet session from the HTTP API"""
    
    if not birdnet_client:
        raise HTTPException(status_code=503, detail="BirdNet API client not configured")
    
    try:
        # Get session data from BirdNet API
        session_data = await birdnet_client.get_session(request.session_id)
        
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Process with integrator
        if request.process_achievements and integrator:
            results = await integrator.process_birdnet_session(
                session_data, 
                default_user_id=request.user_id
            )
            return {
                "session_id": request.session_id,
                "processed": True,
                "results": results
            }
        
        return {
            "session_id": request.session_id,
            "processed": False,
            "session_data": session_data
        }
        
    except Exception as e:
        logger.error(f"Error processing BirdNet session {request.session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/birdnet/health")
async def birdnet_health():
    """Check BirdNet API health"""
    
    if not birdnet_client:
        return {"status": "not_configured", "message": "BirdNet API client not configured"}
    
    try:
        is_healthy = await birdnet_client.health_check()
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "api_url": BIRDNET_API_URL
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/birdnet/sync-recent")
async def sync_recent_birdnet_sessions(limit: int = 10, hours_back: int = 24):
    """Sync recent sessions from BirdNet API"""
    
    if not birdnet_client or not integrator:
        raise HTTPException(status_code=503, detail="BirdNet integration not configured")
    
    try:
        # Get recent sessions
        sessions = await birdnet_client.get_recent_sessions(limit=limit, hours_back=hours_back)
        
        results = []
        for session in sessions:
            try:
                result = await integrator.process_birdnet_session(session)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process session {session.get('session_id', 'unknown')}: {e}")
                results.append({"session_id": session.get("session_id"), "error": str(e)})
        
        return {
            "sessions_processed": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error syncing recent BirdNet sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/birdnet/sync-user-detections/{user_id}")
async def sync_user_detections_to_achievements(
    user_id: int,
    hours_back: int = 24,
    min_confidence: float = 0.7
):
    """
    Sync recent BirdNET detections for a specific user and process achievements
    """
    
    if not birdnet_client or not achievements_client:
        raise HTTPException(status_code=503, detail="BirdNet or achievements service not configured")
    
    try:
        # Get recent sessions (since we don't have user mapping yet, get all recent)
        sessions = await birdnet_client.get_recent_sessions(limit=50, hours_back=hours_back)
        
        processed_detections = []
        achievements_triggered = []
        
        for session in sessions:
            session_id = session.get('session_id')
            if not session_id:
                continue
                
            # Get detections for this session
            detections = await birdnet_client.get_session_detections(session_id)
            
            for detection in detections:
                confidence = detection.get('confidence', 0.0)
                if confidence < min_confidence:
                    continue
                
                try:
                    # Process detection for achievements
                    detection_data = {
                        "user_id": user_id,
                        "species_name": detection.get('species_name', 'Unknown'),
                        "confidence": confidence,
                        "location": {"latitude": 0.0, "longitude": 0.0},  # Default location
                        "detection_time": detection.get('detected_at', datetime.now().isoformat())
                    }
                    
                    # Send to achievements service
                    achievements = await achievements_client.process_species_detection(detection_data)
                    
                    if achievements:
                        achievements_triggered.extend(achievements)
                    
                    processed_detections.append({
                        "session_id": session_id,
                        "species": detection.get('species_name'),
                        "confidence": confidence,
                        "achievements": len(achievements) if achievements else 0
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to process detection {detection.get('species_name', 'Unknown')}: {e}")
        
        return {
            "user_id": user_id,
            "detections_processed": len(processed_detections),
            "achievements_triggered": len(achievements_triggered),
            "detections": processed_detections,
            "achievements": achievements_triggered
        }
        
    except Exception as e:
        logger.error(f"Error syncing user detections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Database Integration endpoints
@app.get("/database/health")
async def database_health():
    """Check database integration health"""
    
    database_integration = "not_configured" if not database_client else "configured"
    database_healthy = False
    
    if database_client:
        try:
            database_healthy = await database_client.is_connected()
        except Exception:
            database_healthy = False
    
    return {
        "database_integration": database_integration,
        "database_healthy": database_healthy,
        "mongodb_url": MONGODB_URL if MONGODB_URL else None,
        "database_name": MONGODB_DATABASE,
        "sessions_collection": SESSIONS_COLLECTION,
        "detections_collection": DETECTIONS_COLLECTION
    }

@app.get("/database/statistics")
async def database_statistics():
    """Get database and sync statistics"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        syncer = BirdNetDataSyncer(database_client, achievements_client, sightings_client)
        
        # Get unprocessed sessions count
        unprocessed_count = await syncer.get_unprocessed_sessions_count()
        
        # Get general database stats
        is_connected = await database_client.is_connected()
        
        # Get species statistics
        species_stats = await syncer.get_species_statistics()
        
        return {
            "database_statistics": {
                "database_connected": is_connected,
                "unprocessed_sessions": unprocessed_count,
                "species_statistics": species_stats
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting database statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/database/sessions/recent")
async def get_recent_database_sessions(limit: int = 10, hours_back: int = 24):
    """Get recent sessions from database"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        sessions = await database_client.get_recent_sessions(limit=limit, hours_back=hours_back)
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error getting recent sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/database/sessions/unprocessed")
async def get_unprocessed_sessions(limit: int = 50):
    """Get unprocessed sessions from database"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        syncer = BirdNetDataSyncer(database_client, achievements_client, sightings_client)
        sessions = await syncer.get_unprocessed_sessions(limit=limit)
        return {"unprocessed_sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error getting unprocessed sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/database/sessions/{session_id}")
async def get_session_details(session_id: str):
    """Get detailed session information"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        session_data = await database_client.get_session_with_detections(session_id)
        
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return session_data
        
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/database/sync-unprocessed")
async def sync_unprocessed_sessions(request: DatabaseSyncRequest):
    """Sync unprocessed sessions from database"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        syncer = BirdNetDataSyncer(database_client, achievements_client, sightings_client)
        
        results = await syncer.sync_unprocessed_sessions(
            limit=request.limit,
            min_confidence=request.min_confidence,
            default_user_id=request.default_user_id
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error syncing unprocessed sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/database/sync-user/{birdnet_user_id}")
async def sync_user_sessions(birdnet_user_id: str, request: UserSyncRequest):
    """Sync sessions for a specific user"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        syncer = BirdNetDataSyncer(database_client, achievements_client, sightings_client)
        
        results = await syncer.sync_user_sessions(
            birdnet_user_id=birdnet_user_id,
            winged_user_id=request.winged_user_id,
            limit=request.limit,
            min_confidence=request.min_confidence
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error syncing user {birdnet_user_id} sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/database/species/statistics")
async def get_species_statistics(days_back: int = 7):
    """Get species detection statistics from database"""
    
    if not database_client:
        raise HTTPException(status_code=503, detail="Database client not configured")
    
    try:
        syncer = BirdNetDataSyncer(database_client, achievements_client, sightings_client)
        stats = await syncer.get_species_statistics(days_back=days_back)
        
        return {"species_statistics": stats}
        
    except Exception as e:
        logger.error(f"Error getting species statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)