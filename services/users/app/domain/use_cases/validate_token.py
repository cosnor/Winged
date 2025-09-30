from dataclasses import dataclass
from typing import Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.services.auth_service import AuthService
from domain.exceptions.user_exceptions import (
    InvalidTokenError,
    UserNotActiveError,
    UserNotFoundError
)

@dataclass
class ValidateTokenRequest:
    """DTO de entrada para el caso de uso ValidateToken"""
    token: str

@dataclass
class ValidateTokenResponse:
    """DTO de salida para el caso de uso ValidateToken"""
    is_valid: bool
    user_id: Optional[int] = None
    email: Optional[str] = None
    level: Optional[int] = None
    xp: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None  # ISO formatz
    token_type: Optional[str] = None
    expires_at: Optional[str] = None  # ISO format

class ValidateTokenUseCase:
    """
    Caso de uso: Validar un token de acceso
    
    Responsabilidades:
    1. Verificar que el token es válido (formato, firma, expiración)
    2. Extraer información del usuario del token
    3. Verificar que el usuario aún existe y está activo
    4. Retornar información del usuario si el token es válido
    
    Uso típico:
    - API Gateway valida tokens antes de hacer proxy
    - Otros microservicios verifican permisos
    - Middleware de autenticación en endpoints protegidos
    """
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        """     
        Args:
            user_repository: Contrato para acceso a datos de usuarios
            auth_service: Contrato para servicios de autenticación
        """
        self._user_repository = user_repository
        self._auth_service = auth_service
    
    def execute(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        """
        Ejecuta el caso de uso de validación de token
        
        Args:
            request: Token a validar
            
        Returns:
            ValidateTokenResponse: Resultado de la validación e info del usuario
        """
        
        # PASO 1: Validar entrada básica
        if not request.token or not request.token.strip():
            return ValidateTokenResponse(is_valid=False)
        
        try:
            # PASO 2: Validar token (formato, firma, expiración)
            token_payload = self._validate_token_format_and_signature(request.token)
            if not token_payload:
                return ValidateTokenResponse(is_valid=False)
            
            # PASO 3: Extraer user_id del token
            user_id = self._extract_user_id_from_payload(token_payload)
            if not user_id:
                return ValidateTokenResponse(is_valid=False)
            
            # PASO 4: Verificar que el usuario aún existe y está activo
            user = self._verify_user_exists_and_active(user_id)
            if not user:
                return ValidateTokenResponse(is_valid=False)
            
            # PASO 5: Extraer información adicional del token
            expires_at = self._extract_expiration_from_payload(token_payload)
            token_type = token_payload.get("type", "access")
            
            # PASO 6: Retornar respuesta exitosa con info del usuario
            return ValidateTokenResponse(
                is_valid=True,
                user_id=user.id,
                email=user.email,
                level=user.level,
                xp=user.xp,
                is_active=user.is_active,
                created_at=user.created_at.isoformat() if user.created_at else None,
                token_type=token_type,
                expires_at=expires_at
            )
            
        except Exception as e:
            # Si cualquier paso falla, el token es inválido
            # Log del error para debugging (no exponer al cliente)
            print(f"Token validation failed: {e}")
            return ValidateTokenResponse(is_valid=False)
    
    def _validate_token_format_and_signature(self, token: str) -> Optional[dict]:
        """
        Valida el formato del token, firma y expiración
        
        Args:
            token: Token a validar
            
        Returns:
            dict: Payload del token si es válido, None si no
        """
        try:
            payload = self._auth_service.validate_token(token)
            return payload
        except Exception:
            return None
    
    def _extract_user_id_from_payload(self, payload: dict) -> Optional[int]:
        """
        Extrae el user_id del payload del token
        
        Args:
            payload: Payload decodificado del token
            
        Returns:
            int: ID del usuario si existe, None si no
        """
        try:
            user_id = payload.get("user_id")
            return int(user_id) if user_id else None
        except (ValueError, TypeError):
            return None
    
    def _verify_user_exists_and_active(self, user_id: int) -> Optional[User]:
        """
        Verifica que el usuario existe y está activo
        
        Args:
            user_id: ID del usuario a verificar
            
        Returns:
            User: Usuario si existe y está activo, None si no
        """
        try:
            user = self._user_repository.find_by_id(user_id)
            if user and user.is_active:
                return user
            return None
        except Exception:
            return None
    
    def _extract_expiration_from_payload(self, payload: dict) -> Optional[str]:
        """
        Extrae la fecha de expiración del payload
        
        Args:
            payload: Payload del token
            
        Returns:
            str: Fecha de expiración en formato ISO, None si no existe
        """
        try:
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                from datetime import datetime
                exp_date = datetime.fromtimestamp(exp_timestamp, tz=datetime.timezone.utc)
                return exp_date.isoformat()
            return None
        except Exception:
            return None