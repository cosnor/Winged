from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
import bcrypt
from domain.services.auth_service import AuthService
from domain.entities.user import User


class JWTAuthService(AuthService):
    """
    Implementación del AuthService usando JWT y bcrypt
    
    Responsabilidades:
    - Hash y verificación de contraseñas con bcrypt
    - Generación y validación de tokens JWT
    - Manejo de refresh tokens
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        Args:
            secret_key: Clave secreta para firmar JWT (debe ser segura)
            algorithm: Algoritmo para JWT (HS256)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def hash_password(self, plain_password: str) -> str:
        """
        Hashea una contraseña usando bcrypt
        
        Args:
            plain_password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        # Generar salt y hashear
        salt = bcrypt.gensalt()
        password_bytes = plain_password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña contra su hash
        
        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash almacenado
            
        Returns:
            True si coinciden, False si no
        """
        try:
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    
    def generate_access_token(self, user: User, expires_in_minutes: int = 60) -> str:
        """
        Genera un token de acceso JWT
        
        Args:
            user: Usuario para el cual generar el token
            expires_in_minutes: Minutos hasta la expiración
            
        Returns:
            Token JWT
        """
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user.id,
            "email": user.email,
            "level": user.level,
            "xp": user.xp,
            "is_active": user.is_active,
            "iat": now,  # Issued at
            "exp": now + timedelta(minutes=expires_in_minutes),  # Expiration
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_refresh_token(self, user: User, expires_in_days: int = 30) -> str:
        """
        Genera un token de refresh JWT (Usamos para larga duración)
        
        Args:
            user: Usuario para el cual generar el token
            expires_in_days: Días hasta la expiración
            
        Returns:
            Refresh token JWT
        """
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user.id,
            "iat": now,
            "exp": now + timedelta(days=expires_in_days),
            "type": "refresh"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token JWT y extrae su payload
        
        Args:
            token: Token a validar
            
        Returns:
            Payload del token si es válido, None si no
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            # Token ha expirado
            return None
        except jwt.InvalidTokenError:
            # Token inválido (firma incorrecta, malformado, etc.)
            return None
        except Exception:
            # Cualquier otro error
            return None
    
    def extract_user_id_from_token(self, token: str) -> Optional[int]:
        """
        Extrae el user_id de un token válido
        
        Args:
            token: Token del cual extraer el user_id
            
        Returns:
            User ID si el token es válido, None si no
        """
        payload = self.validate_token(token)
        if payload:
            return payload.get("user_id")
        return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica si un token ha expirado
        
        Args:
            token: Token a verificar
            
        Returns:
            True si ha expirado, False si es válido
        """
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return False  # Si no lanza excepción, no ha expirado
        except jwt.ExpiredSignatureError:
            return True   # Ha expirado
        except jwt.InvalidTokenError:
            return True   # Inválido = consideramos como expirado
    
    
    def generate_reset_password_token(self, user: User, expires_in_minutes: int = 15) -> str:
        """
        Genera token especial para reset de contraseña (corta duración)
        
        Args:
            user: Usuario que solicita reset
            expires_in_minutes: Minutos hasta expiración (corto por seguridad)
            
        Returns:
            Token para reset de contraseña
        """
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user.id,
            "email": user.email,
            "iat": now,
            "exp": now + timedelta(minutes=expires_in_minutes),
            "type": "password_reset"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def validate_reset_password_token(self, token: str) -> Optional[int]:
        """
        Valida token de reset de contraseña
        
        Args:
            token: Token de reset a validar
            
        Returns:
            User ID si el token es válido y es de tipo reset, None si no
        """
        payload = self.validate_token(token)
        if payload and payload.get("type") == "password_reset":
            return payload.get("user_id")
        return None