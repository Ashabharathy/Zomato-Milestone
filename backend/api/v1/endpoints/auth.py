"""
Authentication endpoints for the Restaurant Recommendation System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from typing import Optional
import structlog

from core.database import get_async_session
from core.exceptions import AuthenticationError, TokenExpiredError, InvalidTokenError
from core.config import settings
from models.user import User, UserSession
from schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserResponse
)
from services.auth import AuthService
from services.jwt import JWTService

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Register a new user"""
    try:
        auth_service = AuthService(db)
        user = await auth_service.register(request)
        logger.info("user_registered", user_id=user.id, email=user.email)
        return UserResponse.from_user(user)
    
    except AuthenticationError as e:
        logger.warning("registration_failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("registration_error", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Authenticate user and return tokens"""
    try:
        auth_service = AuthService(db)
        tokens = await auth_service.login(request)
        logger.info("user_logged_in", email=request.email)
        return tokens
    
    except AuthenticationError as e:
        logger.warning("login_failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as e:
        logger.error("login_error", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """Refresh access token using refresh token"""
    try:
        jwt_service = JWTService()
        auth_service = AuthService(db)
        
        # Validate refresh token
        payload = jwt_service.decode_token(request.refresh_token)
        if payload.get("token_type") != "refresh":
            raise InvalidTokenError("Invalid token type")
        
        # Get user session
        session = await auth_service.get_session_by_refresh_token(request.refresh_token)
        if not session or session.is_expired():
            raise TokenExpiredError("Refresh token expired")
        
        # Generate new tokens
        user = await auth_service.get_user_by_id(session.user_id)
        new_tokens = jwt_service.create_tokens(user.id)
        
        # Update session
        await auth_service.update_session_tokens(session, new_tokens)
        
        logger.info("token_refreshed", user_id=user.id)
        return RefreshTokenResponse(
            access_token=new_tokens["access_token"],
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    except (InvalidTokenError, TokenExpiredError) as e:
        logger.warning("token_refresh_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as e:
        logger.error("token_refresh_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.delete("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
):
    """Logout user and invalidate tokens"""
    try:
        jwt_service = JWTService()
        auth_service = AuthService(db)
        
        # Get user from token
        payload = jwt_service.decode_token(credentials.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise InvalidTokenError("Invalid token")
        
        # Invalidate user sessions
        await auth_service.logout_user(user_id)
        
        logger.info("user_logged_out", user_id=user_id)
        return {"message": "Successfully logged out"}
    
    except InvalidTokenError as e:
        logger.warning("logout_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as e:
        logger.error("logout_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """Dependency to get current authenticated user"""
    try:
        jwt_service = JWTService()
        auth_service = AuthService(db)
        
        # Validate access token
        payload = jwt_service.verify_token(credentials.credentials)
        if payload.get("token_type") != "access":
            raise InvalidTokenError("Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Invalid token")
        
        # Get user
        user = await auth_service.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Update session last used
        await auth_service.update_session_last_used(user_id, credentials.credentials)
        
        return user
    
    except (InvalidTokenError, AuthenticationError) as e:
        logger.warning("authentication_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.get("/me", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return UserResponse.model_validate(current_user)


@router.get("/verify/{token}")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Verify user email"""
    try:
        auth_service = AuthService(db)
        user = await auth_service.verify_email(token)
        
        logger.info("email_verified", user_id=user.id, email=user.email)
        return {"message": "Email verified successfully"}
    
    except AuthenticationError as e:
        logger.warning("email_verification_failed", token=token, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("email_verification_error", token=token, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Send password reset email"""
    try:
        auth_service = AuthService(db)
        await auth_service.send_password_reset_email(email)
        
        logger.info("password_reset_sent", email=email)
        return {"message": "Password reset email sent"}
    
    except Exception as e:
        logger.error("password_reset_error", email=email, error=str(e))
        # Always return success to prevent email enumeration
        return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Reset password with token"""
    try:
        auth_service = AuthService(db)
        user = await auth_service.reset_password(token, new_password)
        
        logger.info("password_reset", user_id=user.id, email=user.email)
        return {"message": "Password reset successfully"}
    
    except AuthenticationError as e:
        logger.warning("password_reset_failed", token=token, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        logger.error("password_reset_error", token=token, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
