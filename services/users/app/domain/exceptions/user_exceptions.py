class UserDomainException(Exception):
    """Excepción base para errores de dominio del usuario"""
    pass

class InvalidEmailError(UserDomainException):
    """Se lanza cuando el email no es válido"""
    pass

class InvalidPasswordError(UserDomainException):
    """Se lanza cuando la contraseña no cumple los requisitos"""
    pass

class EmailAlreadyExistsError(UserDomainException):
    """Se lanza cuando el email ya está registrado"""
    pass

class UserNotFoundError(UserDomainException):
    """Se lanza cuando no se encuentra un usuario"""
    pass

class UserNotActiveError(UserDomainException):
    """Se lanza cuando se intenta acceder con usuario inactivo"""
    pass

class InvalidCredentialsError(UserDomainException):
    """Se lanza cuando email/contraseña son incorrectos"""
    pass

class InvalidTokenError(UserDomainException):
    """Se lanza cuando el token JWT es inválido o ha expirado"""
    pass

class InvalidNameError(UserDomainException):
    """Se lanza cuando el nombre no es válido"""
    pass