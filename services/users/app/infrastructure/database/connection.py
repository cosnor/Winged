from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import os
import logging

# Configurar logging para SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Base para todos los modelos
Base = declarative_base()

class DatabaseConnection:
    """
    Maneja la conexión a la base de datos PostgreSQL
    
    Responsabilidades:
    - Crear y configurar el engine de SQLAlchemy
    - Manejar el pool de conexiones
    - Proporcionar sesiones de base de datos
    - Crear/eliminar tablas
    """
    
    def __init__(self, database_url: str = None, echo: bool = False):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            database_url: URL de conexión a PostgreSQL
            echo: Si True, muestra las queries SQL en consola
        """
        self.database_url = database_url or self._get_database_url()
        self.echo = echo
        self.engine = None
        self.session_local = None
        
        self._create_engine()
        self._create_session_factory()
    
    def _get_database_url(self) -> str:
        """
        Obtiene la URL de base de datos desde variables de entorno
        
        Returns:
            str: URL de conexión a PostgreSQL
        """
        # Variables de entorno para configuración
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "winged_users")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "password")
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def _create_engine(self) -> None:
        """Crea el engine de SQLAlchemy con configuración optimizada"""
        self.engine = create_engine(
            self.database_url,
            # Pool de conexiones
            pool_size=20,           # Número base de conexiones
            max_overflow=30,        # Conexiones adicionales en picos
            pool_pre_ping=True,     # Verifica conexiones antes de usarlas
            pool_recycle=3600,      # Recicla conexiones cada hora
            
            # Configuración de logging
            echo=self.echo,
            echo_pool=False,
            
            # Configuración específica para PostgreSQL
            connect_args={
                "options": "-c timezone=utc"  # Forzar UTC en PostgreSQL
            }
        )
        
    
    def _create_session_factory(self) -> None:
        """Crea el factory de sesiones"""
        self.session_local = sessionmaker(
            bind=self.engine,
            autocommit=False,   # Transacciones manuales
            autoflush=False,    # No flush automático
            expire_on_commit=False  # Los objetos siguen válidos después del commit
        )
    
    def get_session(self) -> Session:
        """
        Obtiene una nueva sesión de base de datos
        
        Returns:
            Session: Nueva sesión de SQLAlchemy
            
        Note:
            Recuerda cerrar la sesión con session.close()
        """
        return self.session_local()
    
    def get_session_dependency(self) -> Generator[Session, None, None]:
        """
        Dependency injection para FastAPI
        
        Yields:
            Session: Sesión de base de datos que se cierra automáticamente
        """
        session = self.get_session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_all_tables(self) -> None:
        """
        Crea todas las tablas definidas en los modelos
        """
        try:
            # Importar todos los modelos aquí para registrarlos
            from infrastructure.database.models.user_model import UserModel
            
            Base.metadata.create_all(bind=self.engine)
            print("✅ Tablas creadas exitosamente")
        except Exception as e:
            print(f"❌ Error creando tablas: {e}")
            raise
    
    def drop_all_tables(self) -> None:
        """
        Elimina todas las tablas (útil para tests y development)
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
            print("✅ Tablas eliminadas exitosamente")
        except Exception as e:
            print(f"❌ Error eliminando tablas: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                return result.scalar() == 1
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def get_engine_info(self) -> dict:
        """
        Obtiene información del engine para debugging
        
        Returns:
            dict: Información de la conexión
        """
        return {
            "url": str(self.engine.url),
            "pool_size": self.engine.pool.size(),
            "checked_in": self.engine.pool.checkedin(),
            "checked_out": self.engine.pool.checkedout(),
            "overflow": self.engine.pool.overflow(),
        }
    
    def close_all_connections(self) -> None:
        """
        Cierra todas las conexiones del pool
        """
        if self.engine:
            self.engine.dispose()
            print("✅ Conexiones cerradas")


# Singleton global para la aplicación
_db_connection: DatabaseConnection = None

def get_database_connection(database_url: str = None, echo: bool = False) -> DatabaseConnection:
    """
    Obtiene la conexión singleton de base de datos
    
    Args:
        database_url: URL de conexión (solo en primera llamada)
        echo: Mostrar SQL queries (solo en primera llamada)
        
    Returns:
        DatabaseConnection: Instancia singleton
    """
    global _db_connection
    
    if _db_connection is None:
        _db_connection = DatabaseConnection(database_url, echo)
    
    return _db_connection

# En connection.py
def get_db_session() -> Session:
    """Get database session - retorna Session directa"""
    db_connection = get_database_connection()
    return db_connection.get_session()

# Funciones de utilidad para development/testing
def init_database(database_url: str = None, echo: bool = False) -> None:
    """
    Inicializa la base de datos y crea las tablas
    
    Args:
        database_url: URL de conexión
        echo: Mostrar queries SQL
    """
    db_connection = get_database_connection(database_url, echo)
    
    print("🔌 Probando conexión...")
    if db_connection.test_connection():
        print("✅ Conexión exitosa")
        print("🏗️ Creando tablas...")
        db_connection.create_all_tables()
    else:
        print("❌ Error de conexión a la base de datos")
        raise Exception("No se pudo conectar a la base de datos")

def reset_database() -> None:
    """
    Elimina y recrea todas las tablas (útil para development)
    """
    db_connection = get_database_connection()
    print("🗑️ Eliminando tablas...")
    db_connection.drop_all_tables()
    print("🏗️ Recreando tablas...")
    db_connection.create_all_tables()