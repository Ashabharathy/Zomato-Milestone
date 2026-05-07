"""
Core module for Restaurant Recommendation System
Configuration, database, logging, and exceptions
"""

from .config import settings, get_settings
from .database import Base, get_async_session, init_db, close_db
from .logging import setup_logging, get_logger, log_performance
from .exceptions import (
    CustomException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    RecommendationError,
    LLMError,
    DatabaseError
)

__all__ = [
    # Configuration
    "settings",
    "get_settings",
    
    # Database
    "Base",
    "get_async_session",
    "init_db",
    "close_db",
    
    # Logging
    "setup_logging",
    "get_logger",
    "log_performance",
    
    # Exceptions
    "CustomException",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "RecommendationError",
    "LLMError",
    "DatabaseError"
]
