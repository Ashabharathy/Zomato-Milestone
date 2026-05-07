"""
User models for the Restaurant Recommendation System
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional, Dict, Any

from core.database import Base


class User(Base):
    """User model for authentication and profiles"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    
    # Preferences and settings
    preferences = Column(JSON, default=dict)
    settings = Column(JSON, default=dict)
    
    # Status and timestamps
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    user_sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    user_preferences = relationship("UserPreference", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def full_name(self) -> Optional[str]:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "preferences": self.preferences or {},
            "settings": self.settings or {},
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


class UserSession(Base):
    """User session model for JWT token management"""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    refresh_token = Column(String(500), unique=True, nullable=False)
    
    # Session metadata
    device_info = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="user_sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "is_active": self.is_active
        }


class UserPreference(Base):
    """User preference model for restaurant recommendations"""
    
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Location preferences
    location = Column(String(255))
    latitude = Column(String(20))
    longitude = Column(String(20))
    radius = Column(Integer, default=10)  # km
    
    # Budget preferences
    budget_min = Column(Integer)
    budget_max = Column(Integer)
    price_range = Column(String(10))  # $, $$, $$$, $$$$
    
    # Cuisine preferences
    cuisine = Column(String(100))
    excluded_cuisines = Column(JSON, default=list)
    
    # Rating preferences
    min_rating = Column(Integer)  # 1-5 scale
    
    # Dietary constraints
    dietary_constraints = Column(JSON, default=list)
    
    # Meal preferences
    meal_type = Column(String(50))  # breakfast, lunch, dinner, snacks
    group_size = Column(Integer, default=2)
    
    # Ambiance preferences
    ambiance = Column(JSON, default=list)  # casual, formal, romantic, etc.
    
    # Feature preferences
    required_features = Column(JSON, default=list)
    avoided_features = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="user_preferences")
    
    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id}, location={self.location})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert preference to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "radius": self.radius,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max,
            "price_range": self.price_range,
            "cuisine": self.cuisine,
            "excluded_cuisines": self.excluded_cuisines or [],
            "min_rating": self.min_rating,
            "dietary_constraints": self.dietary_constraints or [],
            "meal_type": self.meal_type,
            "group_size": self.group_size,
            "ambiance": self.ambiance or [],
            "required_features": self.required_features or [],
            "avoided_features": self.avoided_features or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active
        }
    
    def validate(self) -> Dict[str, Any]:
        """Validate preference data"""
        errors = {}
        
        # Validate budget
        if self.budget_min and self.budget_max and self.budget_min > self.budget_max:
            errors["budget"] = "Minimum budget cannot be greater than maximum budget"
        
        # Validate rating
        if self.min_rating and (self.min_rating < 1 or self.min_rating > 5):
            errors["rating"] = "Rating must be between 1 and 5"
        
        # Validate group size
        if self.group_size and (self.group_size < 1 or self.group_size > 20):
            errors["group_size"] = "Group size must be between 1 and 20"
        
        # Validate radius
        if self.radius and (self.radius < 1 or self.radius > 100):
            errors["radius"] = "Radius must be between 1 and 100 km"
        
        return errors
