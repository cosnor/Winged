from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class SpeciesModel(Base):
    """SQLAlchemy model for Species."""
    __tablename__ = "species"
    
    id = Column(Integer, primary_key=True, index=True)
    scientific_name = Column(String(255), unique=True, nullable=False, index=True)
    common_name = Column(String(255), nullable=False, index=True)
    common_name_es = Column(String(255), nullable=True)
    family = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    habitat = Column(Text, nullable=True)
    rarity_level = Column(String(20), nullable=False, index=True)
    conservation_status = Column(String(50), nullable=True)
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    size_cm = Column(Float, nullable=True)
    weight_g = Column(Float, nullable=True)
    wingspan_cm = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_species = relationship("UserSpeciesModel", back_populates="species")


class UserSpeciesModel(Base):
    """SQLAlchemy model for UserSpecies."""
    __tablename__ = "user_species"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False, index=True)
    discovered_at = Column(DateTime(timezone=True), nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    location_name = Column(String(255), nullable=True)
    confidence_score = Column(Float, nullable=False, default=1.0)
    photo_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    verified = Column(Boolean, default=False)
    verification_source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    species = relationship("SpeciesModel", back_populates="user_species")
    
    # Unique constraint to prevent duplicate discoveries
    __table_args__ = (
        {"extend_existing": True}
    )


class CollectionModel(Base):
    """SQLAlchemy model for Collection."""
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)
    species_ids = Column(JSON, nullable=False, default=list)  # Array of species IDs
    is_system_collection = Column(Boolean, default=False, index=True)
    created_by = Column(String(255), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AchievementModel(Base):
    """SQLAlchemy model for Achievement."""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    achievement_type = Column(String(50), nullable=False, index=True)
    tier = Column(String(20), nullable=False, index=True)
    icon = Column(String(100), nullable=False)
    points = Column(Integer, nullable=False)
    requirement_value = Column(Integer, nullable=False)
    requirement_description = Column(String(500), nullable=False)
    is_hidden = Column(Boolean, default=False)
    is_repeatable = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievementModel", back_populates="achievement")


class UserAchievementModel(Base):
    """SQLAlchemy model for UserAchievement."""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False, index=True)
    unlocked_at = Column(DateTime(timezone=True), nullable=False)
    progress_value = Column(Integer, nullable=False, default=0)
    is_completed = Column(Boolean, default=False, index=True)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    achievement = relationship("AchievementModel", back_populates="user_achievements")
    
    # Unique constraint to prevent duplicate user achievements (unless repeatable)
    __table_args__ = (
        {"extend_existing": True}
    )


class UserProgressModel(Base):
    """SQLAlchemy model for UserProgress."""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    total_species_discovered = Column(Integer, default=0)
    total_points = Column(Integer, default=0, index=True)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    last_discovery_date = Column(DateTime(timezone=True), nullable=True)
    achievements_unlocked = Column(Integer, default=0)
    rare_species_count = Column(Integer, default=0)
    collections_completed = Column(Integer, default=0)
    total_identifications = Column(Integer, default=0)
    high_confidence_identifications = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())