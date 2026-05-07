"""
Recommendation models for the Restaurant Recommendation System
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional, Dict, Any, List

from core.database import Base


class Recommendation(Base):
    """Recommendation model for storing AI-generated recommendations"""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Request information
    session_id = Column(String(255), index=True)
    request_id = Column(String(255), unique=True, index=True)
    
    # User preferences snapshot
    user_preferences = Column(JSON, nullable=False)
    
    # LLM configuration
    model_used = Column(String(100))
    prompt_version = Column(String(50))
    temperature = Column(Float)
    max_tokens = Column(Integer)
    
    # Processing metrics
    processing_time = Column(Float)  # seconds
    tokens_used = Column(Integer)
    api_calls_count = Column(Integer, default=1)
    
    # Results
    total_candidates = Column(Integer)
    filtered_candidates = Column(Integer)
    final_recommendations = Column(Integer)
    
    # LLM response
    llm_response = Column(Text)
    parsed_response = Column(JSON)
    
    # Status
    status = Column(String(20), default="completed")  # pending, processing, completed, failed
    fallback_used = Column(Boolean, default=False)
    error_message = Column(Text)
    
    # Quality metrics
    confidence_score = Column(Float)
    validation_passed = Column(Boolean, default=True)
    validation_errors = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    items = relationship("RecommendationItem", back_populates="recommendation", cascade="all, delete-orphan")
    feedback = relationship("RecommendationFeedback", back_populates="recommendation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, status={self.status})>"
    
    def to_dict(self, include_items: bool = True, include_feedback: bool = False) -> Dict[str, Any]:
        """Convert recommendation to dictionary"""
        result = {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "user_preferences": self.user_preferences,
            "model_used": self.model_used,
            "prompt_version": self.prompt_version,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "processing_time": self.processing_time,
            "tokens_used": self.tokens_used,
            "api_calls_count": self.api_calls_count,
            "total_candidates": self.total_candidates,
            "filtered_candidates": self.filtered_candidates,
            "final_recommendations": self.final_recommendations,
            "llm_response": self.llm_response,
            "parsed_response": self.parsed_response,
            "status": self.status,
            "fallback_used": self.fallback_used,
            "error_message": self.error_message,
            "confidence_score": self.confidence_score,
            "validation_passed": self.validation_passed,
            "validation_errors": self.validation_errors or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_items and self.items:
            result["items"] = [item.to_dict() for item in self.items]
        
        if include_feedback and self.feedback:
            result["feedback"] = [fb.to_dict() for fb in self.feedback]
        
        return result
    
    def get_top_recommendations(self, limit: int = 5) -> List["RecommendationItem"]:
        """Get top N recommendations"""
        return sorted(self.items, key=lambda x: x.rank)[:limit]
    
    def get_average_score(self) -> Optional[float]:
        """Get average recommendation score"""
        if not self.items:
            return None
        return sum(item.score for item in self.items) / len(self.items)


class RecommendationItem(Base):
    """Individual recommendation item"""
    
    __tablename__ = "recommendation_items"
    
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)
    
    # Ranking information
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    
    # LLM-generated content
    explanation = Column(Text)
    highlights = Column(JSON, default=list)
    considerations = Column(JSON, default=list)
    
    # Additional metadata
    match_reasons = Column(JSON, default=list)
    confidence_factors = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendation = relationship("Recommendation", back_populates="items")
    restaurant = relationship("Restaurant", back_populates="recommendation_items")
    
    def __repr__(self):
        return f"<RecommendationItem(id={self.id}, rank={self.rank}, score={self.score})>"
    
    def to_dict(self, include_restaurant: bool = True) -> Dict[str, Any]:
        """Convert recommendation item to dictionary"""
        result = {
            "id": self.id,
            "recommendation_id": self.recommendation_id,
            "restaurant_id": self.restaurant_id,
            "rank": self.rank,
            "score": self.score,
            "explanation": self.explanation,
            "highlights": self.highlights or [],
            "considerations": self.considerations or [],
            "match_reasons": self.match_reasons or [],
            "confidence_factors": self.confidence_factors or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_restaurant and self.restaurant:
            result["restaurant"] = self.restaurant.to_dict()
        
        return result


class RecommendationFeedback(Base):
    """User feedback on recommendations"""
    
    __tablename__ = "recommendation_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Feedback types
    feedback_type = Column(String(20), nullable=False)  # like, dislike, neutral, bookmark, visit
    
    # Ratings
    rating = Column(Integer)  # 1-5 scale for detailed feedback
    helpfulness = Column(Integer)  # 1-5 scale for recommendation helpfulness
    
    # Feedback content
    comment = Column(Text)
    reasons = Column(JSON, default=list)  # Reasons for feedback
    
    # Context
    context = Column(JSON, default=dict)  # Additional context about the feedback
    
    # Status
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendation = relationship("Recommendation", back_populates="feedback")
    restaurant = relationship("Restaurant")
    user = relationship("User")
    
    def __repr__(self):
        return f"<RecommendationFeedback(id={self.id}, type={self.feedback_type}, rating={self.rating})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert feedback to dictionary"""
        return {
            "id": self.id,
            "recommendation_id": self.recommendation_id,
            "restaurant_id": self.restaurant_id,
            "user_id": self.user_id,
            "feedback_type": self.feedback_type,
            "rating": self.rating,
            "helpfulness": self.helpfulness,
            "comment": self.comment,
            "reasons": self.reasons or [],
            "context": self.context or {},
            "is_processed": self.is_processed,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class RecommendationHistory(Base):
    """Historical record of recommendation requests and outcomes"""
    
    __tablename__ = "recommendation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Request summary
    request_date = Column(DateTime(timezone=True), nullable=False, index=True)
    preferences_summary = Column(JSON)
    
    # Results summary
    recommendations_count = Column(Integer)
    top_restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    average_score = Column(Float)
    
    # User interaction
    viewed_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    feedback_count = Column(Integer, default=0)
    positive_feedback_count = Column(Integer, default=0)
    
    # Business outcomes
    conversion_rate = Column(Float)  # Users who actually visited
    satisfaction_score = Column(Float)  # Average satisfaction from feedback
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    top_restaurant = relationship("Restaurant")
    
    def __repr__(self):
        return f"<RecommendationHistory(id={self.id}, user_id={self.user_id}, date={self.request_date})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert history record to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_date": self.request_date.isoformat() if self.request_date else None,
            "preferences_summary": self.preferences_summary,
            "recommendations_count": self.recommendations_count,
            "top_restaurant_id": self.top_restaurant_id,
            "average_score": self.average_score,
            "viewed_count": self.viewed_count,
            "clicked_count": self.clicked_count,
            "feedback_count": self.feedback_count,
            "positive_feedback_count": self.positive_feedback_count,
            "conversion_rate": self.conversion_rate,
            "satisfaction_score": self.satisfaction_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
