from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .infrastructure.database.config import engine, Base, SessionLocal
from .infrastructure.database.repositories import SQLAlchemyAchievementRepository
from .presentation.api.controllers import achievement_controller, user_controller, leaderboard_controller
from .presentation.dependencies import get_achievement_service
from .application.services.achievement_application_service import AchievementApplicationService
from .application.use_cases.manage_achievements import ManageAchievementsUseCase
from .presentation.schemas.requests import SpeciesDetectionRequest, BatchSpeciesDetectionRequest
from .presentation.schemas.responses import SpeciesDetectionResponse, BatchSpeciesDetectionResponse
import logging


# Database dependency
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication dependency (placeholder - implement based on your auth system)
def get_current_user():
    """Current user dependency - implement based on your authentication system"""
    # For now, return a placeholder - you'll need to implement actual authentication
    return {"user_id": 1, "username": "test_user"}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables (only if database is available)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Could not create database tables: {e}")
    logger.info("Service will start without database connection")

app = FastAPI(
    title="Winged Achievements Service",
    description="Achievement and gamification service for the Winged bird identification app",
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

# Include routers
app.include_router(achievement_controller.router)
app.include_router(user_controller.router)
app.include_router(leaderboard_controller.router)


@app.on_event("startup")
async def startup_event():
    """Initialize default achievements on startup"""
    logger.info("Starting up Achievements Service...")
    
    # This is a bit of a hack to get the service without going through the dependency system
    # In a real application, you might want to handle this differently
    try:
        from .infrastructure.database.config import SessionLocal
        from .infrastructure.database.repositories import SQLAlchemyAchievementRepository
        from .domain.services.achievement_domain_service import AchievementDomainService
        from .application.use_cases.manage_achievements import ManageAchievementsUseCase
        
        db = SessionLocal()
        try:
            achievement_repo = SQLAlchemyAchievementRepository(db)
            manage_use_case = ManageAchievementsUseCase(achievement_repo)
            created_achievements = manage_use_case.create_default_achievements()
            
            if created_achievements:
                logger.info(f"Created {len(created_achievements)} default achievements")
            else:
                logger.info("Default achievements already exist")
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error initializing default achievements: {e}")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Winged Achievements Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/species/detect", response_model=SpeciesDetectionResponse)
async def process_species_detection(
    request: SpeciesDetectionRequest,
    session: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Process individual species detection and trigger achievements"""
    try:
        # Create use case instance
        achievement_repo = SQLAlchemyAchievementRepository(session)
        manage_use_case = ManageAchievementsUseCase(achievement_repo)
        
        # Process species detection
        triggered_achievements = manage_use_case.process_species_detection(
            user_id=request.user_id,
            species_name=request.species_name,
            confidence=request.confidence,
            location=request.location,
            detection_time=request.detection_time
        )
        
        return SpeciesDetectionResponse(
            success=True,
            message=f"Processed detection of {request.species_name}",
            triggered_achievements=[
                {
                    "id": achievement.id,
                    "title": achievement.title,
                    "description": achievement.description,
                    "type": achievement.achievement_type,
                    "category": achievement.category
                }
                for achievement in triggered_achievements
            ],
            species_detected={
                "name": request.species_name,
                "confidence": request.confidence,
                "location": request.location,
                "timestamp": request.detection_time.isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Error processing species detection: {e}")
        return SpeciesDetectionResponse(
            success=False,
            message=f"Error processing detection: {str(e)}",
            triggered_achievements=[],
            species_detected=None
        )


@app.post("/species/detect/batch", response_model=BatchSpeciesDetectionResponse)
async def process_batch_species_detection(
    request: BatchSpeciesDetectionRequest,
    session: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Process batch species detections and trigger achievements"""
    try:
        # Create use case instance
        achievement_repo = SQLAlchemyAchievementRepository(session)
        manage_use_case = ManageAchievementsUseCase(achievement_repo)
        
        all_triggered_achievements = []
        processed_detections = []
        
        # Process each detection
        for detection in request.detections:
            try:
                triggered_achievements = manage_use_case.process_species_detection(
                    user_id=detection.user_id,
                    species_name=detection.species_name,
                    confidence=detection.confidence,
                    location=detection.location,
                    detection_time=detection.detection_time
                )
                
                all_triggered_achievements.extend(triggered_achievements)
                processed_detections.append({
                    "name": detection.species_name,
                    "confidence": detection.confidence,
                    "location": detection.location,
                    "timestamp": detection.detection_time.isoformat(),
                    "success": True
                })
            except Exception as e:
                logger.error(f"Error processing individual detection {detection.species_name}: {e}")
                processed_detections.append({
                    "name": detection.species_name,
                    "confidence": detection.confidence,
                    "location": detection.location,
                    "timestamp": detection.detection_time.isoformat(),
                    "success": False,
                    "error": str(e)
                })
        
        return BatchSpeciesDetectionResponse(
            success=True,
            message=f"Processed {len(request.detections)} detections",
            total_processed=len(request.detections),
            total_achievements_triggered=len(all_triggered_achievements),
            triggered_achievements=[
                {
                    "id": achievement.id,
                    "title": achievement.title,
                    "description": achievement.description,
                    "type": achievement.achievement_type,
                    "category": achievement.category
                }
                for achievement in all_triggered_achievements
            ],
            processed_detections=processed_detections
        )
    except Exception as e:
        logger.error(f"Error processing batch species detection: {e}")
        return BatchSpeciesDetectionResponse(
            success=False,
            message=f"Error processing batch: {str(e)}",
            total_processed=0,
            total_achievements_triggered=0,
            triggered_achievements=[],
            processed_detections=[]
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)