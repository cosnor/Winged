from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # "species_count", "rare_species", "location", "streak", etc.
    criteria = Column(Text)  # JSON string with achievement criteria
    xp_reward = Column(Integer, default=0)
    icon = Column(String)  # Icon identifier or URL
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to user achievements
    user_achievements = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    progress = Column(Float, default=0.0)  # Progress towards achievement (0.0 to 1.0)
    
    # Relationships
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    # Ensure a user can only have one record per achievement
    __table_args__ = (UniqueConstraint('user_id', 'achievement_id', name='_user_achievement_uc'),)

class BirdCollection(Base):
    __tablename__ = "bird_collections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    species_name = Column(String, nullable=False)
    common_name = Column(String)
    first_sighted_at = Column(DateTime(timezone=True), server_default=func.now())
    sighting_count = Column(Integer, default=1)
    last_sighted_at = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(Float)  # Best confidence score for this species
    location_lat = Column(Float)  # Location of first sighting
    location_lon = Column(Float)
    
    # Ensure a user can only have one record per species
    __table_args__ = (UniqueConstraint('user_id', 'species_name', name='_user_species_uc'),)

class UserStats(Base):
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    total_sightings = Column(Integer, default=0)
    unique_species = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    achievements_unlocked = Column(Integer, default=0)
    first_sighting_date = Column(DateTime(timezone=True))
    last_sighting_date = Column(DateTime(timezone=True))
    longest_streak = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())