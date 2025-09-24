from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import models, schemas, services
from .database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Achievements Service", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize default achievements on startup"""
    db = SessionLocal()
    try:
        achievement_service = services.AchievementService(db)
        achievement_service.create_default_achievements()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Achievements service is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# User Collection Endpoints
@app.get("/users/{user_id}/collection", response_model=schemas.UserCollectionResponse)
def get_user_collection(user_id: int, db: Session = Depends(get_db)):
    """Get user's bird collection with stats and recent achievements"""
    achievement_service = services.AchievementService(db)
    
    birds = achievement_service.get_user_collection(user_id)
    stats = achievement_service.get_user_stats(user_id)
    recent_achievements = achievement_service.get_user_achievements(user_id)[:5]  # Last 5 achievements
    
    return schemas.UserCollectionResponse(
        user_id=user_id,
        birds=birds,
        stats=stats,
        recent_achievements=recent_achievements
    )

@app.get("/users/{user_id}/stats", response_model=schemas.UserStats)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Get user statistics"""
    achievement_service = services.AchievementService(db)
    stats = achievement_service.get_user_stats(user_id)
    return stats

@app.get("/users/{user_id}/achievements", response_model=List[schemas.UserAchievement])
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    """Get user's unlocked achievements"""
    achievement_service = services.AchievementService(db)
    return achievement_service.get_user_achievements(user_id)

@app.get("/users/{user_id}/achievements/progress", response_model=List[schemas.AchievementProgress])
def get_achievement_progress(user_id: int, db: Session = Depends(get_db)):
    """Get user's progress on all achievements"""
    achievement_service = services.AchievementService(db)
    return achievement_service.get_achievement_progress(user_id)

# Sighting Processing Endpoint
@app.post("/sightings/process", response_model=List[schemas.UserAchievement])
def process_sighting(sighting: schemas.SightingEvent, db: Session = Depends(get_db)):
    """Process a new sighting and return any newly unlocked achievements"""
    achievement_service = services.AchievementService(db)
    newly_unlocked = achievement_service.process_sighting(sighting)
    return newly_unlocked

# Achievement Management Endpoints
@app.get("/achievements", response_model=List[schemas.Achievement])
def get_all_achievements(db: Session = Depends(get_db)):
    """Get all available achievements"""
    return db.query(models.Achievement).filter(models.Achievement.is_active == True).all()

@app.get("/achievements/{achievement_id}", response_model=schemas.Achievement)
def get_achievement(achievement_id: int, db: Session = Depends(get_db)):
    """Get specific achievement details"""
    achievement = db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    return achievement

@app.post("/achievements", response_model=schemas.Achievement)
def create_achievement(achievement: schemas.AchievementCreate, db: Session = Depends(get_db)):
    """Create a new achievement (admin endpoint)"""
    db_achievement = models.Achievement(**achievement.dict())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

# Bird Collection Endpoints
@app.get("/birds/species", response_model=List[str])
def get_all_species(db: Session = Depends(get_db)):
    """Get list of all bird species that have been sighted"""
    species = db.query(models.BirdCollection.species_name).distinct().all()
    return [s[0] for s in species]

@app.get("/birds/species/{species_name}/users", response_model=List[int])
def get_users_with_species(species_name: str, db: Session = Depends(get_db)):
    """Get list of user IDs who have sighted a specific species"""
    users = db.query(models.BirdCollection.user_id).filter(
        models.BirdCollection.species_name == species_name
    ).distinct().all()
    return [u[0] for u in users]

# Leaderboard Endpoints
@app.get("/leaderboard/species")
def get_species_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get leaderboard of users by unique species count"""
    leaderboard = db.query(models.UserStats).order_by(
        models.UserStats.unique_species.desc()
    ).limit(limit).all()
    
    return [
        {
            "user_id": stats.user_id,
            "unique_species": stats.unique_species,
            "total_sightings": stats.total_sightings,
            "level": stats.current_level,
            "rank": idx + 1
        }
        for idx, stats in enumerate(leaderboard)
    ]

@app.get("/leaderboard/xp")
def get_xp_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get leaderboard of users by total XP"""
    leaderboard = db.query(models.UserStats).order_by(
        models.UserStats.total_xp.desc()
    ).limit(limit).all()
    
    return [
        {
            "user_id": stats.user_id,
            "total_xp": stats.total_xp,
            "level": stats.current_level,
            "achievements_unlocked": stats.achievements_unlocked,
            "rank": idx + 1
        }
        for idx, stats in enumerate(leaderboard)
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
