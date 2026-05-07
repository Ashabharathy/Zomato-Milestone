"""
Logging configuration for the Restaurant Recommendation System
"""

import structlog
import logging
import sys
from typing import Any
from .config import settings


def setup_logging():
    """Setup structured logging configuration"""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Configure structlog
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    if settings.LOG_FORMAT == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=settings.DEBUG))
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class LoggingMixin:
    """Mixin class to add logging to any class"""
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__)


# Context logger for request tracing
def get_context_logger(**kwargs) -> structlog.stdlib.BoundLogger:
    """Get logger with additional context"""
    logger = get_logger()
    return logger.bind(**kwargs)


# Performance logging decorator
def log_performance(operation_name: str = None):
    """Decorator to log function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            logger = get_logger()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.info(
                    "operation_completed",
                    operation=operation_name or func.__name__,
                    duration_ms=duration * 1000,
                    success=True
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                logger.error(
                    "operation_failed",
                    operation=operation_name or func.__name__,
                    duration_ms=duration * 1000,
                    error=str(e),
                    success=False
                )
                
                raise
                
        return wrapper
    return decorator


# Request logging middleware helper
def log_request(request_id: str, method: str, path: str, user_id: str = None):
    """Log incoming request"""
    logger = get_context_logger(
        request_id=request_id,
        method=method,
        path=path,
        user_id=user_id
    )
    
    logger.info(
        "request_received",
        request_id=request_id,
        method=method,
        path=path,
        user_id=user_id
    )


def log_response(request_id: str, status_code: int, duration_ms: float):
    """Log outgoing response"""
    logger = get_context_logger(request_id=request_id)
    
    logger.info(
        "response_sent",
        request_id=request_id,
        status_code=status_code,
        duration_ms=duration_ms
    )
