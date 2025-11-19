
from dataclasses import dataclass
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.exceptions.user_exceptions import UserNotFoundError

@dataclass
class UpdateUserXpRequest:
    user_id: int
    xp_to_add: int

@dataclass
class UpdateUserXpResponse:
    user_id: int
    name: str
    email: str
    level: int
    xp: int
    is_active: bool
    created_at: str

class UpdateUserXpUseCase:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def execute(self, request: UpdateUserXpRequest) -> UpdateUserXpResponse:
        
        user = self._user_repository.find_by_id(request.user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {request.user_id} not found")
        
        
        new_xp = max(0, user.xp + request.xp_to_add)
        
        
        new_level = self._calculate_level_from_xp(new_xp)
        
        self._user_repository.update_experience(request.user_id, new_xp)
        self._user_repository.update_level(request.user_id, new_level)
        
        updated_user = self._user_repository.find_by_id(request.user_id)
        
        return UpdateUserXpResponse(
            user_id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            level=updated_user.level,
            xp=updated_user.xp,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at.isoformat() if updated_user.created_at else ""
        )
    
    def _calculate_level_from_xp(self, xp: int) -> int:
        """Calculate level based on XP - customize this logic"""
        if xp < 100:
            return 1
        elif xp < 300:
            return 2
        elif xp < 600:
            return 3
        elif xp < 1000:
            return 4
        else:
            return 5 + (xp - 1000) // 500  # Level 5+ each 500 XP