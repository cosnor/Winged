from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from domain.entities.user import User

class AuthService(ABC):

    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        """
        Convierte una contraseña en texto plano a un hash seguro
        
        Args:
            plain_password: Contraseña en texto plano
            
        Returns:
            Hash seguro de la contraseña
            
        """
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash almacenado en la base de datos
            
        Returns:
            True si coincide, False si no
            
        Example:
            verify_password("mi_password123", "$2b$12$abc123...") → True
            verify_password("password_incorrecta", "$2b$12$abc123...") → False
        """
        pass
    
    @abstractmethod
    def generate_access_token(self, user: User, expires_in_minutes: int = 60) -> str:
        """
        Genera un token de acceso para el usuario
        
        Args:
            user: Usuario para quien generar el token
            expires_in_minutes: Minutos hasta que expire el token
            
        Returns:
            Token de acceso (JWT, UUID, etc.)
            
        """
        pass
    
    @abstractmethod
    def generate_refresh_token(self, user: User, expires_in_days: int = 30) -> str:
        """
        Genera un token de refresh para renovar el acceso
        
        Args:
            user: Usuario para quien generar el token
            expires_in_days: Días hasta que expire el token
            
        Returns:
            Token de refresh
        """
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token y extrae su información
        
        Args:
            token: Token a validar
            
        Returns:
            Diccionario con info del token si es válido, None si no
            
        """
        pass
    
    @abstractmethod
    def extract_user_id_from_token(self, token: str) -> Optional[int]:
        """
        Extrae el ID del usuario de un token válido
        
        Args:
            token: Token del que extraer el user_id
            
        Returns:
            User ID si el token es válido, None si no
            
        """
        pass
    
    @abstractmethod
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica si un token ha expirado
        
        Args:
            token: Token a verificar
            
        Returns:
            True si ha expirado, False si aún es válido
        """
        pass
    

    @abstractmethod
    def generate_reset_password_token(self, user: User, expires_in_minutes: int = 15) -> str:
        """
        Genera un token especial para resetear contraseña
        
        Args:
            user: Usuario que solicita resetear contraseña
            expires_in_minutes: Minutos hasta que expire (corto por seguridad)
            
        Returns:
            Token para reset de contraseña
        """
        pass
    
    @abstractmethod
    def validate_reset_password_token(self, token: str) -> Optional[int]:
        """
        Valida un token de reset de contraseña
        
        Args:
            token: Token de reset a validar
            
        Returns:
            User ID si el token es válido, None si no
        """
        pass