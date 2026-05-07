"""
Restaurant models for the Restaurant Recommendation System
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional, Dict, Any, List

from core.database import Base


class Restaurant(Base):
    """Restaurant model for storing restaurant information"""
    
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    
    # Location information
    address = Column(Text)
    city = Column(String(100), index=True)
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Contact information
    phone = Column(String(20))
    website = Column(String(500))
    email = Column(String(255))
    
    # Restaurant details
    cuisine = Column(String(100), index=True)
    cuisine_tags = Column(JSON, default=list)  # Multiple cuisine types
    
    # Rating and reviews
    rating = Column(Float, index=True)
    review_count = Column(Integer, default=0)
    
    # Price information
    price_range = Column(String(10), index=True)  # $, $$, $$$, $$$$
    avg_cost_for_two = Column(Integer)
    avg_cost_for_one = Column(Integer)
    
    # Operating hours
    opening_hours = Column(JSON, default=dict)
    
    # Features and amenities
    features = Column(JSON, default=list)
    amenities = Column(JSON, default=list)
    
    # Dietary options
    dietary_options = Column(JSON, default=list)
    
    # Service options
    service_options = Column(JSON, default=list)
    
    # Description and additional info
    description = Column(Text)
    special_notes = Column(Text)
    
    # Media
    logo_url = Column(String(500))
    cover_image_url = Column(String(500))
    
    # Status and verification
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_verified = Column(DateTime(timezone=True))
    
    # External IDs
    zomato_id = Column(String(100), unique=True, index=True)
    google_places_id = Column(String(255))
    
    # Relationships
    images = relationship("RestaurantImage", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship("RestaurantReview", back_populates="restaurant", cascade="all, delete-orphan")
    recommendation_items = relationship("RecommendationItem", back_populates="restaurant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Restaurant(id={self.id}, name={self.name}, city={self.city})>"
    
    def to_dict(self, include_images: bool = False, include_reviews: bool = False) -> Dict[str, Any]:
        """Convert restaurant to dictionary"""
        result = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "postal_code": self.postal_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "website": self.website,
            "email": self.email,
            "cuisine": self.cuisine,
            "cuisine_tags": self.cuisine_tags or [],
            "rating": self.rating,
            "review_count": self.review_count,
            "price_range": self.price_range,
            "avg_cost_for_two": self.avg_cost_for_two,
            "avg_cost_for_one": self.avg_cost_for_one,
            "opening_hours": self.opening_hours or {},
            "features": self.features or [],
            "amenities": self.amenities or [],
            "dietary_options": self.dietary_options or [],
            "service_options": self.service_options or [],
            "description": self.description,
            "special_notes": self.special_notes,
            "logo_url": self.logo_url,
            "cover_image_url": self.cover_image_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_verified": self.last_verified.isoformat() if self.last_verified else None,
            "zomato_id": self.zomato_id,
            "google_places_id": self.google_places_id
        }
        
        if include_images and self.images:
            result["images"] = [img.to_dict() for img in self.images]
        
        if include_reviews and self.reviews:
            result["reviews"] = [review.to_dict() for review in self.reviews[:10]]  # Limit to 10 recent reviews
        
        return result
    
    def get_primary_image(self) -> Optional["RestaurantImage"]:
        """Get primary image for restaurant"""
        for image in self.images:
            if image.is_primary:
                return image
        return self.images[0] if self.images else None
    
    def is_open_now(self) -> bool:
        """Check if restaurant is currently open"""
        if not self.opening_hours:
            return False
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        day_name = now.strftime("%A").lower()
        
        if day_name not in self.opening_hours:
            return False
        
        today_hours = self.opening_hours[day_name]
        if not today_hours or today_hours.get("closed", False):
            return False
        
        try:
            open_time = datetime.strptime(today_hours["open"], "%H:%M").time()
            close_time = datetime.strptime(today_hours["close"], "%H:%M").time()
            current_time = now.time()
            
            return open_time <= current_time <= close_time
        except (ValueError, KeyError):
            return False
    
    def get_distance_from(self, lat: float, lon: float) -> Optional[float]:
        """Calculate distance from given coordinates in kilometers"""
        if not self.latitude or not self.longitude:
            return None
        
        from math import radians, sin, cos, sqrt, atan2
        
        # Convert to radians
        lat1, lon1 = radians(self.latitude), radians(self.longitude)
        lat2, lon2 = radians(lat), radians(lon)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return r * c


class RestaurantImage(Base):
    """Restaurant image model"""
    
    __tablename__ = "restaurant_images"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)
    
    # Image information
    url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    caption = Column(Text)
    
    # Image metadata
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)
    format = Column(String(10))  # jpg, png, webp, etc.
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="images")
    
    def __repr__(self):
        return f"<RestaurantImage(id={self.id}, restaurant_id={self.restaurant_id})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert image to dictionary"""
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "url": self.url,
            "alt_text": self.alt_text,
            "caption": self.caption,
            "width": self.width,
            "height": self.height,
            "file_size": self.file_size,
            "format": self.format,
            "is_primary": self.is_primary,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class RestaurantReview(Base):
    """Restaurant review model"""
    
    __tablename__ = "restaurant_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Review content
    rating = Column(Integer, nullable=False, index=True)  # 1-5
    title = Column(String(255))
    content = Column(Text)
    
    # Review metadata
    helpful_count = Column(Integer, default=0)
    response = Column(Text)  # Restaurant owner response
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="reviews")
    user = relationship("User")
    
    def __repr__(self):
        return f"<RestaurantReview(id={self.id}, restaurant_id={self.restaurant_id}, rating={self.rating})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert review to dictionary"""
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id,
            "rating": self.rating,
            "title": self.title,
            "content": self.content,
            "helpful_count": self.helpful_count,
            "response": self.response,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
