from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator

# Infrastructure imports
from infrastructure.database.connection import DatabaseConnection, get_db_session

# Domain imports
from domain.repositories.user_repository import UserRepository
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl

# Singleton para la conexión de DB
_db_connection = None

def get_database_connection() -> DatabaseConnection:
    """
    Dependency para obtener la conexión a la base de datos (singleton)
    
    Returns:
        DatabaseConnection: Instancia de conexión a DB
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection

def get_db_session_dependency() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos
    
    Yields:
        Session: Sesión de SQLAlchemy
        
    Note:
        Se cierra automáticamente después del request
    """
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()

def get_user_repository(session: Session = Depends(get_db_session_dependency)) -> UserRepository:
    """
    Dependency para obtener el repositorio de usuarios
    
    Args:
        session: Sesión de base de datos (FastAPI automáticamente resuelve el generator)
        
    Returns:
        UserRepository: Implementación del repositorio de usuarios
    """
    return UserRepositoryImpl(session)