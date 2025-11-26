from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserInfo(BaseModel):
    """Información básica del usuario para responses"""
    user_id: int = Field(..., description="ID único del usuario")
    name: str = Field(..., description="Nombre del usuario")
    email: str = Field(..., description="Email del usuario")
    level: int = Field(..., description="Nivel actual del usuario")
    xp: int = Field(..., description="Puntos de experiencia")
    is_active: bool = Field(..., description="Si el usuario está activo")
    created_at: str = Field(..., description="Fecha de creación (ISO format)")

class RegisterUserResponse(BaseModel):
    """Response para registro de usuario exitoso"""
    success: bool = Field(True, description="Si la operación fue exitosa")
    message: str = Field("User registered successfully", description="Mensaje descriptivo")
    data: UserInfo = Field(..., description="Información del usuario creado")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user_id": 1,
                    "name": "Usuario Ejemplo",
                    "email": "usuario@ejemplo.com",
                    "level": 1,
                    "xp": 0,
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                }
            }
        }

class LoginUserResponse(BaseModel):
    """Response para login de usuario exitoso"""
    success: bool = Field(True, description="Si la operación fue exitosa")
    message: str = Field("Login successful", description="Mensaje descriptivo")
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field("Bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Minutos hasta expiración")
    user_info: UserInfo = Field(..., description="Información del usuario autenticado")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20ifQ.signature",
                "token_type": "Bearer",
                "expires_in": 60,
                "user_info": {
                    "user_id": 1,
                    "name": "Usuario Ejemplo",
                    "email": "usuario@ejemplo.com",
                    "level": 2,
                    "xp": 150,
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                }
            }
        }

class ValidateTokenResponse(BaseModel):
    """Response para validación de token"""
    is_valid: bool = Field(..., description="Si el token es válido")
    user_info: Optional[UserInfo] = Field(None, description="Info del usuario si token válido")
    token_type: Optional[str] = Field(None, description="Tipo de token")
    expires_at: Optional[str] = Field(None, description="Fecha de expiración del token")
    error: Optional[str] = Field(None, description="Mensaje de error si token inválido")
    
    class Config:
        schema_extra = {
            "example": {
                "is_valid": True,
                "user_info": {
                    "user_id": 1,
                    "name": "Usuario Ejemplo",
                    "email": "usuario@ejemplo.com",
                    "level": 2,
                    "xp": 150,
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "token_type": "Bearer",
                "expires_at": "2024-01-15T11:30:00Z"
            }
        }

class GetUserProfileResponse(BaseModel):
    """Response para obtener perfil del usuario"""
    success: bool = Field(True, description="Si la operación fue exitosa")
    message: str = Field("Profile retrieved successfully", description="Mensaje descriptivo")
    data: UserInfo = Field(..., description="Información del perfil del usuario")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Profile retrieved successfully",
                "data": {
                    "user_id": 1,
                    "name": "Usuario Ejemplo",
                    "email": "usuario@ejemplo.com",
                    "level": 3,
                    "xp": 250,
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                }
            }
        }

class ErrorResponse(BaseModel):
    """Response estándar para errores"""
    success: bool = Field(False, description="Indica que hubo un error")
    error_code: str = Field(..., description="Código del error")
    error_message: str = Field(..., description="Mensaje de error legible")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales del error")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Timestamp del error")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error_code": "INVALID_CREDENTIALS",
                "error_message": "Invalid email or password",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

class ValidationErrorResponse(BaseModel):
    """Response para errores de validación específicos"""
    success: bool = Field(False, description="Indica que hubo errores de validación")
    error_code: str = Field("VALIDATION_ERROR", description="Código del error")
    error_message: str = Field("Validation failed", description="Mensaje principal")
    validation_errors: list = Field(..., description="Lista de errores específicos de validación")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "error_message": "Validation failed",
                "validation_errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "rejected_value": "invalid-email"
                    },
                    {
                        "field": "password", 
                        "message": "Password must be at least 8 characters",
                        "rejected_value": "123"
                    }
                ],
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

