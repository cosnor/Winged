from dataclasses import dataclass
from typing import Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.services.auth_service import AuthService
from domain.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserNotActiveError,
    UserNotFoundError
)

@dataclass
class AuthenticateUserRequest:
    """DTO de entrada para el caso de uso AuthenticateUser"""
    email: str
    password: str

@dataclass
class AuthenticateUserResponse:
    """DTO de salida para el caso de uso AuthenticateUser"""
    access_token: str
    token_type: str
    expires_in: int  # Minutos hasta que expire
    user_info: dict  # Información básica del usuario

class AuthenticateUserUseCase:
    """
    Caso de uso: Autenticar un usuario (Login)
    
    Responsabilidades:
    1. Buscar usuario por email
    2. Verificar que el usuario existe y está activo
    3. Validar la contraseña
    4. Generar token de acceso
    5. Actualizar última fecha de login
    6. Retornar token y información básica del usuario
    """
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        """ 
        Args:
            user_repository: Contrato para acceso a datos de usuarios
            auth_service: Contrato para servicios de autenticación
        """
        self._user_repository = user_repository
        self._auth_service = auth_service
    
    def execute(self, request: AuthenticateUserRequest) -> AuthenticateUserResponse:
        """
        Ejecuta el caso de uso de autenticación de usuario
        
        Args:
            request: Credenciales del usuario (email y contraseña)
            
        Returns:
            AuthenticateUserResponse: Token de acceso e info del usuario
            
        Raises:
            InvalidCredentialsError: Si email/contraseña son incorrectos
            UserNotActiveError: Si el usuario está desactivado
            UserNotFoundError: Si el usuario no existe
        """
        # PASO 1: Validar entrada básica
        self._validate_input(request)
        # PASO 2: Buscar usuario por email
        user = self._find_user_by_email(request.email)
        
        # PASO 3: Verificar que el usuario está activo
        self._ensure_user_is_active(user)
        
        # PASO 4: Verificar contraseña
        self._verify_password(request.password, user.password_hash)
        
        # PASO 5: Generar token de acceso
        access_token = self._auth_service.generate_access_token(user)
        
        # PASO 6: Actualizar última fecha de login (opcional)
        self._update_last_login(user)
        
        # PASO 7: Retornar respuesta con token e info del usuario
        return AuthenticateUserResponse(
            access_token=access_token,
            token_type="Bearer",
            expires_in=60,  # 60 minutos por defecto
            user_info={
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "level": user.level,
                "xp": user.xp,
                "is_active": user.is_active
            }
        )
    
    def _validate_input(self, request: AuthenticateUserRequest) -> None:
        """Valida la entrada básica del request"""
        if not request.email or not request.email.strip():
            raise InvalidCredentialsError("Email is required")
        
        if not request.password:
            raise InvalidCredentialsError("Password is required")
        
        # Normalizar email
        request.email = request.email.strip().lower()
    
    def _find_user_by_email(self, email: str) -> User:
        """
        Busca el usuario por email
        
        Returns:
            User: El usuario encontrado
            
        Raises:
            InvalidCredentialsError: Si no se encuentra el usuario
        """
        user = self._user_repository.find_by_email(email)
        if not user:
            # Por seguridad, usamos el mismo error que para contraseña incorrecta
            raise InvalidCredentialsError("Invalid email or password")
        
        return user
    
    def _ensure_user_is_active(self, user: User) -> None:
        """
        Verifica que el usuario esté activo
        
        Args:
            user: Usuario a verificar
            
        Raises:
            UserNotActiveError: Si el usuario está desactivado
        """
        if not user.is_active:
            raise UserNotActiveError("User account is deactivated")
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> None:
        """
        Verifica que la contraseña sea correcta
        
        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash almacenado en base de datos
            
        Raises:
            InvalidCredentialsError: Si la contraseña es incorrecta
        """
        if not self._auth_service.verify_password(plain_password, hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
    
    def _update_last_login(self, user: User) -> None:
        """
        Actualiza la fecha del último login del usuario
        
        Args:
            user: Usuario que acaba de hacer login
        """
        try:
            self._user_repository.update_last_login(user.id)
        except Exception as e:
            # Si falla la actualización, no afecta el login
            # Solo registrar el error para debugging
            print(f"Warning: Could not update last login for user {user.id}: {e}")