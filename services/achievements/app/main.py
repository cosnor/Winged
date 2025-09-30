from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .infrastructure.database.config import engine, Base
from .presentation.api.controllers import achievement_controller, user_controller, leaderboard_controller
from .presentation.dependencies import get_achievement_service
from .application.services.achievement_application_service import AchievementApplicationService
import logging

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)