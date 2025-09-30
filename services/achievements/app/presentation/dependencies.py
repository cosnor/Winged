from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database.config import get_db
from ..infrastructure.database.repositories import (
    SQLAlchemyAchievementRepository,
    SQLAlchemyUserAchievementRepository,
    SQLAlchemyBirdCollectionRepository,
    SQLAlchemyUserStatsRepository
)
from ..infrastructure.external.notification_service import (
    LoggingNotificationService,
    LoggingEventPublisher
)
from ..domain.services.achievement_domain_service import AchievementDomainService
from ..application.services.achievement_application_service import AchievementApplicationService


def get_achievement_repository(db: Session = Depends(get_db)):
    """Get achievement repository instance"""
    return SQLAlchemyAchievementRepository(db)


def get_user_achievement_repository(db: Session = Depends(get_db)):
    """Get user achievement repository instance"""
    return SQLAlchemyUserAchievementRepository(db)


def get_bird_collection_repository(db: Session = Depends(get_db)):
    """Get bird collection repository instance"""
    return SQLAlchemyBirdCollectionRepository(db)


def get_user_stats_repository(db: Session = Depends(get_db)):
    """Get user stats repository instance"""
    return SQLAlchemyUserStatsRepository(db)


def get_achievement_domain_service():
    """Get achievement domain service instance"""
    return AchievementDomainService()


def get_notification_service():
    """Get notification service instance"""
    return LoggingNotificationService()


def get_event_publisher():
    """Get event publisher instance"""
    return LoggingEventPublisher()


def get_achievement_service(
    achievement_repo=Depends(get_achievement_repository),
    user_achievement_repo=Depends(get_user_achievement_repository),
    bird_collection_repo=Depends(get_bird_collection_repository),
    user_stats_repo=Depends(get_user_stats_repository),
    domain_service=Depends(get_achievement_domain_service),
    notification_service=Depends(get_notification_service),
    event_publisher=Depends(get_event_publisher)
):
    """Get achievement application service instance with all dependencies"""
    return AchievementApplicationService(
        achievement_repo=achievement_repo,
        user_achievement_repo=user_achievement_repo,
        bird_collection_repo=bird_collection_repo,
        user_stats_repo=user_stats_repo,
        achievement_domain_service=domain_service,
        notification_service=notification_service,
        event_publisher=event_publisher
    )