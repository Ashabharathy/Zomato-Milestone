"""
JWT service for token management
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
import structlog

from core.config import settings
from core.exceptions import TokenExpiredError, InvalidTokenError

logger = structlog.get_logger()


class JWTService:
    """Service for JWT token operations"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def create_access_token(self, subject: str, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        """Create access token"""
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expires = datetime.now(timezone.utc) + expires_delta
        
        to_encode = {
            "sub": subject,
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, subject: str) -> str:
        """Create refresh token"""
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        expires = datetime.now(timezone.utc) + expires_delta
        
        to_encode = {
            "sub": subject,
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "type": "refresh"
        }
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")
    
    def get_user_id_from_token(self, token: str) -> str:
        """Extract user ID from token"""
        payload = self.verify_token(token)
        return payload.get("sub")
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return self.pwd_context.verify(plain_password, hashed_password)
