from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from domain.use_cases.update_user_xp import UpdateUserXpUseCase, UpdateUserXpRequest
from domain.use_cases.register_user import RegisterUserUseCase, RegisterUserRequest as DomainRegisterRequest
from domain.use_cases.authenticate_user import AuthenticateUserUseCase, AuthenticateUserRequest as DomainAuthRequest
from domain.use_cases.validate_token import ValidateTokenUseCase, ValidateTokenRequest as DomainValidateRequest
from domain.exceptions.user_exceptions import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError
)

# Infrastructure imports
from infrastructure.auth.jwt_handler import JWTAuthService

# Presentation imports
from presentation.schemas.user_request import (
    RegisterUserRequest,
    LoginUserRequest,
    ValidateTokenRequest
)
from presentation.schemas.user_response import (
    RegisterUserResponse,
    LoginUserResponse,
    ValidateTokenResponse,
    GetUserProfileResponse,
    ErrorResponse,
    UserInfo
)
from presentation.dependencies.auth_dependency import get_current_user, get_auth_service
from presentation.dependencies.db_dependency import get_user_repository

# Crear router
router = APIRouter(
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user with email and password"
)
def register_user(
    request: RegisterUserRequest,
    user_repository = Depends(get_user_repository),
    auth_service: JWTAuthService = Depends(get_auth_service)
):
    try:
        # Create domain request
        domain_request = DomainRegisterRequest(
            email=request.email,
            password=request.password
        )
        
        # Execute use case
        use_case = RegisterUserUseCase(user_repository, auth_service)
        domain_response = use_case.execute(domain_request)
        
        # Create response
        response = RegisterUserResponse(
            success=True,
            message="User registered successfully",
            data=UserInfo(
                user_id=getattr(domain_response, 'user_id', None),
                email=getattr(domain_response, 'email', None),
                level=getattr(domain_response, 'level', 1),
                xp=getattr(domain_response, 'xp', 0),
                is_active=getattr(domain_response, 'is_active', True),
                created_at=getattr(domain_response, 'created_at', '')
            )
        )
        
        return response
        
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
        
@router.post(
    "/login",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and return JWT token"
)
def login_user(
    request: LoginUserRequest,
    user_repository = Depends(get_user_repository),
    auth_service: JWTAuthService = Depends(get_auth_service)
):
    """Login user and get JWT token"""
    try:
        # Create domain request
        domain_request = DomainAuthRequest(
            email=request.email,
            password=request.password
        )
        # Execute use case
        use_case = AuthenticateUserUseCase(user_repository, auth_service)
        domain_response = use_case.execute(domain_request)
        
        # Create response
        response = LoginUserResponse(
            success=True,
            message="Login successful",
            access_token=getattr(domain_response, 'access_token', 'missing'),
            token_type=getattr(domain_response, 'token_type', 'Bearer'),
            expires_in=getattr(domain_response, 'expires_in', 3600),
            user_info=UserInfo(
                user_id=domain_response.user_info.get("user_id", None) if hasattr(domain_response, 'user_info') else None,
                email=domain_response.user_info.get("email", "") if hasattr(domain_response, 'user_info') else "",
                level=domain_response.user_info.get("level", 1) if hasattr(domain_response, 'user_info') else 1,
                xp=domain_response.user_info.get("xp", 0) if hasattr(domain_response, 'user_info') else 0,
                is_active=domain_response.user_info.get("is_active", True) if hasattr(domain_response, 'user_info') else True,
                created_at=domain_response.user_info.get("created_at", "") if hasattr(domain_response, 'user_info') else ""
            )
        )
        
        return response
        
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post(
    "/validate-token",
    response_model=ValidateTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate JWT token",
    description="Validate if JWT token is valid and return user info"
)
def validate_token(
    request: ValidateTokenRequest,
    user_repository = Depends(get_user_repository),
    auth_service: JWTAuthService = Depends(get_auth_service)
):
    """Validate JWT token"""
    try:
        # Create domain request
        domain_request = DomainValidateRequest(
            token=request.token
        )
        
        # Execute use case
        use_case = ValidateTokenUseCase(user_repository, auth_service)
        domain_response = use_case.execute(domain_request)
        
        # Create response
        if domain_response.is_valid:
            return ValidateTokenResponse(
                is_valid=True,
                user_info=UserInfo(
                    user_id=domain_response.user_id,
                    email=domain_response.email,
                    level=domain_response.level,
                    xp=domain_response.xp,
                    is_active=domain_response.is_active,
                    created_at=domain_response.created_at
                ),
                token_type="Bearer",
                expires_at=domain_response.expires_at.isoformat() if domain_response.expires_at else None
            )
        else:
            return ValidateTokenResponse(
                is_valid=False,
                error="Invalid or expired token"
            )
            
    except InvalidTokenError as e:
        return ValidateTokenResponse(
            is_valid=False,
            error=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token validation failed"
        )

@router.get(
    "/profile",
    response_model=GetUserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user profile",
    description="Get current user profile (requires authentication)"
)
def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user profile"""
    try:
        return GetUserProfileResponse(
            success=True,
            message="Profile retrieved successfully",
            data=UserInfo(
                user_id=current_user["user_id"],
                email=current_user["email"],
                level=current_user["level"],
                xp=current_user["xp"],
                is_active=current_user["is_active"],
                created_at=""
            )
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )
        
    
from domain.use_cases.get_user_by_id import GetUserByIdUseCase, GetUserByIdRequest

@router.get(
    "/users/{user_id}",
    response_model=GetUserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Get user information by user ID (for internal service communication)"
)
def get_user_by_id(
    user_id: int,
    user_repository = Depends(get_user_repository)
):
    """Get user by ID - for service-to-service communication"""
    try:
        # Create domain request
        domain_request = GetUserByIdRequest(user_id=user_id)
        
        # Execute use case
        use_case = GetUserByIdUseCase(user_repository)
        domain_response = use_case.execute(domain_request)
        
        # Create response
        return GetUserProfileResponse(
            success=True,
            message="User found",
            data=UserInfo(
                user_id=domain_response.user_id,
                email=domain_response.email,
                level=domain_response.level,
                xp=domain_response.xp,
                is_active=domain_response.is_active,
                created_at=domain_response.created_at
            )
        )
        
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )
        

@router.patch(
    "/users/{user_id}/xp",
    response_model=GetUserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user XP",
    description="Add XP to user (for internal service communication)"
)
def update_user_xp(
    user_id: int,
    xp_to_add: int,
    user_repository = Depends(get_user_repository)
):
    """Update user XP - for service-to-service communication"""
    try:
        domain_request = UpdateUserXpRequest(
            user_id=user_id,
            xp_to_add=xp_to_add
        )
        
        use_case = UpdateUserXpUseCase(user_repository)
        domain_response = use_case.execute(domain_request)
        
        return GetUserProfileResponse(
            success=True,
            message=f"User XP updated (+{xp_to_add})",
            data=UserInfo(
                user_id=domain_response.user_id,
                email=domain_response.email,
                level=domain_response.level,
                xp=domain_response.xp,
                is_active=domain_response.is_active,
                created_at=domain_response.created_at
            )
        )
        
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user XP"
        )