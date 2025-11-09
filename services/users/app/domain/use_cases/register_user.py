from dataclasses import dataclass
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.services.auth_service import AuthService
from domain.exceptions.user_exceptions import (
    EmailAlreadyExistsError, 
    InvalidEmailError, 
    InvalidPasswordError
)

@dataclass
class RegisterUserRequest:
    """DTO de entrada para el caso de uso RegisterUser"""
    name: str
    email: str
    password: str

@dataclass  
class RegisterUserResponse:
    """DTO de salida para el caso de uso RegisterUser"""
    user_id: int
    name: str
    email: str
    xp: int
    level: int
    is_active: bool
    created_at: str  # ISO format

class RegisterUserUseCase:
    """
    Caso de uso: Registrar un nuevo usuario en el sistema
    
    Responsabilidades:
    1. Validar que el email no exista
    2. Validar fortaleza de la contraseña  
    3. Hashear la contraseña
    4. Crear la entidad User
    5. Guardar el usuario en el repositorio
    6. Retornar la respuesta estructurada
    """
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        """
        Args:
            user_repository: Contrato para acceso a datos de usuarios
            auth_service: Contrato para servicios de autenticación
        """
        self._user_repository = user_repository
        self._auth_service = auth_service
    
    def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """
        Ejecuta el caso de uso de registro de usuario
        
        Args:
            request: Datos necesarios para registrar el usuario
            
        Returns:
            RegisterUserResponse: Datos del usuario creado
            
        Raises:
            EmailAlreadyExistsError: Si el email ya está registrado
            InvalidEmailError: Si el email no es válido
            InvalidPasswordError: Si la contraseña no cumple los requisitos
        """
        
        # PASO 1: Validar entrada básica
        self._validate_input(request)
        
        # PASO 2: Verificar que el email no esté registrado
        self._ensure_email_is_unique(request.email)
        
        # PASO 3: Validar fortaleza de contraseña (lógica de negocio)
        self._validate_password_strength(request.password)
        
        # PASO 4: Hashear la contraseña usando el servicio de auth
        password_hash = self._auth_service.hash_password(request.password)
        
        # PASO 5: Crear la entidad User
        user = User(
            name=request.name,
            email=request.email.lower().strip(),  # Normalizar email
            password_hash=password_hash
            # xp=0, level=1, is_active=True se asignan por defecto en User
        )
        # PASO 6: Guardar el usuario usando el repositorio
        saved_user = self._user_repository.save(user)
        
        # PASO 7: Retornar respuesta estructurada (sin datos sensibles)
        return RegisterUserResponse(
            user_id=saved_user.id,
            name=saved_user.name,
            email=saved_user.email,
            xp=saved_user.xp,
            level=saved_user.level,
            is_active=saved_user.is_active,
            created_at=saved_user.created_at.isoformat()
        )
    
    def _validate_input(self, request: RegisterUserRequest) -> None:
        """Valida la entrada básica del request"""
        if not request.email or not request.email.strip():
            raise InvalidEmailError("Email is required")
        
        if not request.password:
            raise InvalidPasswordError("Password is required")
        
        # Trimear y normalizar email
        request.email = request.email.strip().lower()
    
    def _ensure_email_is_unique(self, email: str) -> None:
        """Verifica que el email no esté ya registrado"""
        if self._user_repository.exists_by_email(email):
            raise EmailAlreadyExistsError(f"A user with email '{email}' already exists")
    
    def _validate_password_strength(self, password: str) -> None:
        """
        Valida la fortaleza de la contraseña
        
        Reglas:
        - Mínimo 8 caracteres
        - Al menos una mayúscula
        - Al menos un número
        """
        if len(password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            raise InvalidPasswordError("Password must contain at least one uppercase letter")
        
        if not any(c.isdigit() for c in password):
            raise InvalidPasswordError("Password must contain at least one number")
        