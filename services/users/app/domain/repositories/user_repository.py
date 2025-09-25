from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.user import User

class UserRepository(ABC):
 
    
    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guarda un usuario (crear nuevo o actualizar existente)
        
        Args:
            user: Usuario a guardar
            
        Returns:
            Usuario guardado (con ID si es nuevo)
            
        Raises:
            EmailAlreadyExistsError: Si el email ya existe
        """
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            User si lo encuentra, None si no existe
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            User si lo encuentra, None si no existe
        """
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con ese email
        
        Args:
            email: Email a verificar
            
        Returns:
            True si existe, False si no
        """
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por ID
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[User]:
        """
        Obtiene todos los usuarios activos
        
        Returns:
            Lista de usuarios activos
        """
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: int) -> None:
        """
        Actualiza la fecha del último login
        
        Args:
            user_id: ID del usuario
        """
        pass