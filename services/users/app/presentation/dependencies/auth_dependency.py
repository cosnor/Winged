# presentation/dependencies/auth_dependency.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import os
from infrastructure.auth.jwt_handler import JWTAuthService
from domain.use_cases.validate_token import ValidateTokenUseCase, ValidateTokenRequest
from .db_dependency import get_user_repository

security = HTTPBearer()  

def get_auth_service() -> JWTAuthService:
    """Obtener servicio de autenticación"""
    secret_key = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
    return JWTAuthService(secret_key=secret_key)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: JWTAuthService = Depends(get_auth_service),
    user_repository = Depends(get_user_repository)
) -> Dict[str, Any]:
    """Obtener usuario actual desde token"""
    token = credentials.credentials  # JWT limpio (sin "Bearer ")

    use_case = ValidateTokenUseCase(user_repository, auth_service)
    request = ValidateTokenRequest(token=token)
    response = use_case.execute(request)
    
    if not response.is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return {
        "user_id": response.user_id,
        "email": response.email,
        "level": response.level,
        "xp": response.xp,
        "is_active": response.is_active
    }
