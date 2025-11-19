from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterUserRequest(BaseModel):
    """Request para registro de usuario"""
    name: str = Field(..., description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")
    
    class Config:
        json_schema_extra = {  # ← Pydantic V2
            "example": {
                "name": "Usuario Ejemplo",
                "email": "usuario@ejemplo.com",
                "password": "Password123!"
            }
        }

class LoginUserRequest(BaseModel):
    """Request para login de usuario"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "Password123!"
            }
        }

class ValidateTokenRequest(BaseModel):
    """Request para validar token"""
    token: str = Field(..., description="Token JWT a validar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }