"""
Authentication service for user management
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import Optional
import structlog

from models.user import User
from schemas.auth import RegisterRequest, UserCreate
from core.exceptions import AuthenticationError, NotFoundError
from core.config import settings
from services.jwt import JWTService

logger = structlog.get_logger()


class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.jwt_service = JWTService()
    
    async def register_user(self, user_data: RegisterRequest) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise AuthenticationError("User with this email already exists")
        
        # Create new user
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            is_active=True,
            is_verified=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        # Set password (hashing would go here)
        user.set_password(user_data.password)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info("User registered successfully", user_id=user.id, email=user.email)
        return user
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        if not user or not user.check_password(password):
            return None
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create_user_tokens(self, user: User) -> dict:
        """Create access and refresh tokens for user"""
        access_token = self.jwt_service.create_access_token(
            subject=user.id,
            additional_claims={"email": user.email}
        )
        refresh_token = self.jwt_service.create_refresh_token(
            subject=user.id
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get list of users"""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def update_session_last_used(self, user_id: int, token: str) -> None:
        """Update session last used timestamp"""
        # TODO: Implement session tracking
        pass
    
    async def verify_email(self, token: str) -> User:
        """Verify user email"""
        # TODO: Implement email verification
        raise AuthenticationError("Email verification not implemented")
