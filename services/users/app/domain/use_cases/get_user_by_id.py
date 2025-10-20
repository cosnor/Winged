# domain/use_cases/get_user_by_id.py
from dataclasses import dataclass
from typing import Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.exceptions.user_exceptions import UserNotFoundError

@dataclass
class GetUserByIdRequest:
    """DTO de entrada para buscar usuario por ID"""
    user_id: int

@dataclass
class GetUserByIdResponse:
    """DTO de salida para buscar usuario por ID"""
    user_id: int
    email: str
    level: int
    xp: int
    is_active: bool
    created_at: str

class GetUserByIdUseCase:
    """
    Caso de uso: Obtener usuario por ID
    
    Responsabilidades:
    1. Buscar usuario por ID
    2. Verificar que existe
    3. Retornar información del usuario
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def execute(self, request: GetUserByIdRequest) -> GetUserByIdResponse:
        """
        Ejecuta el caso de uso de obtener usuario por ID
        
        Args:
            request: Request con el user_id
            
        Returns:
            GetUserByIdResponse: Información del usuario
            
        Raises:
            UserNotFoundError: Si el usuario no existe
        """
        # Validar entrada
        if not request.user_id or request.user_id <= 0:
            raise UserNotFoundError("Invalid user ID")
        
        # Buscar usuario
        user = self._user_repository.find_by_id(request.user_id)
        
        if not user:
            raise UserNotFoundError(f"User with ID {request.user_id} not found")
        
        # Retornar respuesta
        return GetUserByIdResponse(
            user_id=user.id,
            email=user.email,
            level=user.level,
            xp=user.xp,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else ""
        )