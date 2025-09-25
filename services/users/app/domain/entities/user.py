from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass
from domain.exceptions.user_exceptions import InvalidEmailError, InvalidPasswordError

@dataclass
class User:
    """Entidad User - Contiene la lógica de negocio pura del usuario"""
    
    id: Optional[int] = None
    email: str = ""
    password_hash: str = ""
    xp: int = 0
    level: int = 1
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones automáticas al crear/modificar el usuario"""
        if self.email:
            self.validate_email()
        if self.xp < 0:
            self.xp = 0
        if self.level < 1:
            self.level = 1
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def validate_email(self) -> None:
        """Valida el formato del email (regla de negocio)"""
        if not self.email or "@" not in self.email or "." not in self.email:
            raise InvalidEmailError(f"Invalid email format: {self.email}")
        
        if len(self.email) > 255:
            raise InvalidEmailError("Email too long (max 255 characters)")
    
    def validate_password_strength(self, plain_password: str) -> None:
        """Valida la fortaleza de la contraseña (regla de negocio)"""
        if len(plain_password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in plain_password):
            raise InvalidPasswordError("Password must contain at least one uppercase letter")
        
        if not any(c.isdigit() for c in plain_password):
            raise InvalidPasswordError("Password must contain at least one number")
    
    def add_experience(self, points: int) -> None:
        """Agrega experiencia al usuario (lógica de negocio)"""
        if points < 0:
            raise ValueError("Experience points cannot be negative")
        
        old_level = self.level
        self.xp += points
        
        # Calcular nuevo nivel (ejemplo: cada 100 XP = 1 nivel)
        new_level = (self.xp // 100) + 1
        
        if new_level > self.level:
            self.level = new_level
            self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Desactiva el usuario (lógica de negocio)"""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self) -> None:
        """Activa el usuario (lógica de negocio)"""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
        
    def reset_progress(self) -> None:
        """Reinicia el progreso del usuario (lógica de negocio)"""
        self.xp = 0
        self.level = 1
        self.updated_at = datetime.now(timezone.utc)
    
    def __eq__(self, other) -> bool:
        """Igualdad basada en el ID del usuario"""
        if not isinstance(other, User):
            return False
        return self.id is not None and self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en el ID del usuario"""
        return hash(self.id) if self.id else hash(self.email)
    
    def __str__(self) -> str:
        """Representación string del usuario"""
        return f"User(id={self.id}, email={self.email}, level={self.level}, xp={self.xp})"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return (f"User(id={self.id}, email='{self.email}', "
                f"level={self.level}, xp={self.xp}, active={self.is_active})")