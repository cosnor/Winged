from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

# Base para todos los modelos de SQLAlchemy
Base = declarative_base()

class UserModel(Base):
    """
    Modelo de SQLAlchemy para la tabla de usuarios
    
    Representa la estructura de la tabla 'users' en PostgreSQL.
    Este es el mapeo entre la entidad User del dominio y la tabla de BD.
    """
    
    __tablename__ = "users"
    
    # Columnas de la tabla
    id = Column(
        Integer, 
        primary_key=True, 
        index=True, 
        autoincrement=True,
        comment="ID único del usuario"
    )
    
    email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="Email del usuario (único)"
    )
    
    password_hash = Column(
        Text,  # Text para hashes largos
        nullable=False,
        comment="Hash de la contraseña del usuario"
    )
    
    xp = Column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Puntos de experiencia del usuario"
    )
    
    level = Column(
        Integer, 
        default=1, 
        nullable=False,
        comment="Nivel actual del usuario"
    )
    
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        comment="Indica si el usuario está activo"
    )
    
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),  # PostgreSQL genera automáticamente
        nullable=False,
        comment="Fecha de creación del usuario"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),  # PostgreSQL genera automáticamente
        onupdate=func.now(),        # Se actualiza automáticamente en UPDATE
        nullable=False,
        comment="Fecha de última actualización"
    )
    
    last_login_at = Column(
        DateTime(timezone=True),
        nullable=True,  # Puede ser null si nunca ha hecho login
        comment="Fecha del último login del usuario"
    )
    
    def __repr__(self) -> str:
        """Representación del modelo para debugging"""
        return (f"<UserModel(id={self.id}, email='{self.email}', "
                f"level={self.level}, xp={self.xp}, active={self.is_active})>")
    
    def to_dict(self) -> dict:
        """
        Convierte el modelo a diccionario (útil para debugging/logging)
        
        Returns:
            dict: Representación en diccionario del usuario
        """
        return {
            "id": self.id,
            "email": self.email,
            "xp": self.xp,
            "level": self.level,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None
        }
    
    @classmethod
    def from_domain_entity(cls, user_entity) -> 'UserModel':
        """
        Factory method para crear UserModel desde User entity
        
        Args:
            user_entity: Instancia de User del dominio
            
        Returns:
            UserModel: Instancia del modelo de SQLAlchemy
        """
        return cls(
            id=user_entity.id,
            email=user_entity.email,
            password_hash=user_entity.password_hash,
            xp=user_entity.xp,
            level=user_entity.level,
            is_active=user_entity.is_active,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at
        )
    
    def to_domain_entity(self):
        """
        Convierte el modelo a entidad de dominio
        
        Returns:
            User: Entidad User del dominio
        """
        # Import aquí para evitar imports circulares
        from domain.entities.user import User
        
        return User(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash,
            xp=self.xp,
            level=self.level,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )