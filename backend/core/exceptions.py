"""
Custom exceptions for the Restaurant Recommendation System
"""

from typing import Optional, Any, Dict


class CustomException(Exception):
    """Base custom exception class"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "GENERIC_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# Authentication Exceptions
class AuthenticationError(CustomException):
    """Authentication failed"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
            details=details
        )


class AuthorizationError(CustomException):
    """Authorization failed"""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
            details=details
        )


class TokenExpiredError(CustomException):
    """Token has expired"""
    
    def __init__(self, message: str = "Token has expired", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="TOKEN_EXPIRED",
            status_code=401,
            details=details
        )


class InvalidTokenError(CustomException):
    """Invalid token"""
    
    def __init__(self, message: str = "Invalid token", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="INVALID_TOKEN",
            status_code=401,
            details=details
        )


# Validation Exceptions
class ValidationError(CustomException):
    """Validation failed"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class NotFoundError(CustomException):
    """Resource not found"""
    
    def __init__(self, resource: str = "Resource", details: Optional[Dict[str, Any]] = None):
        message = f"{resource} not found"
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details=details
        )


class ConflictError(CustomException):
    """Resource conflict"""
    
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFLICT",
            status_code=409,
            details=details
        )


# Business Logic Exceptions
class RecommendationError(CustomException):
    """Recommendation generation failed"""
    
    def __init__(self, message: str = "Failed to generate recommendations", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="RECOMMENDATION_ERROR",
            status_code=500,
            details=details
        )


class LLMError(CustomException):
    """LLM API error"""
    
    def __init__(self, message: str = "LLM service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            status_code=503,
            details=details
        )


class DataProcessingError(CustomException):
    """Data processing error"""
    
    def __init__(self, message: str = "Data processing error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATA_PROCESSING_ERROR",
            status_code=500,
            details=details
        )


# Database Exceptions
class DatabaseError(CustomException):
    """Database operation error"""
    
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details
        )


class ConnectionError(CustomException):
    """Database connection error"""
    
    def __init__(self, message: str = "Database connection error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONNECTION_ERROR",
            status_code=503,
            details=details
        )


# Rate Limiting Exceptions
class RateLimitError(CustomException):
    """Rate limit exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details
        )


# File Upload Exceptions
class FileUploadError(CustomException):
    """File upload error"""
    
    def __init__(self, message: str = "File upload error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="FILE_UPLOAD_ERROR",
            status_code=400,
            details=details
        )


class InvalidFileTypeError(CustomException):
    """Invalid file type"""
    
    def __init__(self, message: str = "Invalid file type", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="INVALID_FILE_TYPE",
            status_code=400,
            details=details
        )


class FileSizeError(CustomException):
    """File size too large"""
    
    def __init__(self, message: str = "File size too large", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="FILE_SIZE_ERROR",
            status_code=400,
            details=details
        )


# External API Exceptions
class ExternalAPIError(CustomException):
    """External API error"""
    
    def __init__(self, message: str = "External API error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="EXTERNAL_API_ERROR",
            status_code=502,
            details=details
        )


class ConfigurationError(CustomException):
    """Configuration error"""
    
    def __init__(self, message: str = "Configuration error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
            details=details
        )
