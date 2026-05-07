"""
Restaurant management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import structlog

from core.database import get_async_session
from .auth import get_current_user
from models.user import User

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_restaurants(
    skip: int = 0,
    limit: int = 100,
    cuisine: Optional[str] = None,
    location: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get list of restaurants"""
    # TODO: Implement restaurant service
    return {"message": "Restaurants endpoint - coming soon"}


@router.get("/{restaurant_id}")
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get restaurant by ID"""
    # TODO: Implement restaurant service
    return {"message": f"Restaurant {restaurant_id} - coming soon"}
