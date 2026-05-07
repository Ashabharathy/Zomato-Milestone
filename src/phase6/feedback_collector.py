"""
Feedback Collector Module for Phase 6: Feedback, Evaluation, and Improvement Loop
Collects and processes user feedback for recommendation improvement.
"""

import json
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime, timezone

# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result


class FeedbackType(Enum):
    """Types of user feedback"""
    LIKE = "like"
    DISLIKE = "dislike"
    NEUTRAL = "neutral"
    BOOKMARK = "bookmark"
    VISIT = "visit"
    SKIP = "skip"
    SHARE = "share"
    RATING = "rating"


class FeedbackSource(Enum):
    """Sources of feedback"""
    UI_BUTTON = "ui_button"
    SURVEY = "survey"
    INTERVIEW = "interview"
    AUTOMATIC = "automatic"
    API = "api"
    EMAIL = "email"


@dataclass
class UserFeedback:
    """Individual user feedback data"""
    user_id: str
    session_id: str
    recommendation_id: str
    restaurant_id: str
    feedback_type: FeedbackType
    feedback_source: FeedbackSource
    rating: Optional[int] = None  # 1-5 scale
    helpfulness: Optional[int] = None  # 1-5 scale
    comment: Optional[str] = None
    reasons: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    processed: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if self.reasons is None:
            self.reasons = []
        if self.context is None:
            self.context = {}


@dataclass
class FeedbackAggregation:
    """Aggregated feedback metrics"""
    restaurant_id: str
    total_feedback: int
    positive_feedback: int
    negative_feedback: int
    neutral_feedback: int
    average_rating: Optional[float]
    average_helpfulness: Optional[float]
    feedback_types: Dict[str, int]
    common_reasons: List[str]
    sentiment_score: float
    confidence_score: float
    last_updated: datetime


@dataclass
class FeedbackInsights:
    """Insights derived from feedback analysis"""
    total_recommendations: int
    total_feedback: int
    feedback_rate: float
    average_rating: float
    top_performing_restaurants: List[Dict[str, Any]]
    underperforming_restaurants: List[Dict[str, Any]]
    common_issues: List[str]
    improvement_suggestions: List[str]
    user_satisfaction_trend: List[Dict[str, Any]]
    generated_at: datetime


class FeedbackCollector:
    """Collects and processes user feedback for recommendation improvement"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.feedback_storage: List[UserFeedback] = []
        self.aggregated_feedback: Dict[str, FeedbackAggregation] = {}
        
    def collect_feedback(
        self,
        user_id: str,
        session_id: str,
        recommendation_id: str,
        restaurant_id: str,
        feedback_type: Union[FeedbackType, str],
        feedback_source: Union[FeedbackSource, str] = FeedbackSource.UI_BUTTON,
        rating: Optional[int] = None,
        helpfulness: Optional[int] = None,
        comment: Optional[str] = None,
        reasons: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> UserFeedback:
        """
        Collect user feedback for a recommendation
        
        Args:
            user_id: Unique user identifier
            session_id: Session identifier
            recommendation_id: Recommendation session identifier
            restaurant_id: Restaurant identifier
            feedback_type: Type of feedback
            feedback_source: Source of feedback collection
            rating: User rating (1-5)
            helpfulness: Helpfulness rating (1-5)
            comment: User comment
            reasons: Reasons for feedback
            context: Additional context
            
        Returns:
            UserFeedback object
        """
        try:
            # Convert string enums to enum objects
            if isinstance(feedback_type, str):
                feedback_type = FeedbackType(feedback_type)
            if isinstance(feedback_source, str):
                feedback_source = FeedbackSource(feedback_source)
            
            # Validate feedback data
            self._validate_feedback_data(
                feedback_type, rating, helpfulness, reasons, context
            )
            
            # Create feedback object
            feedback = UserFeedback(
                user_id=user_id,
                session_id=session_id,
                recommendation_id=recommendation_id,
                restaurant_id=restaurant_id,
                feedback_type=feedback_type,
                feedback_source=feedback_source,
                rating=rating,
                helpfulness=helpfulness,
                comment=comment,
                reasons=reasons,
                context=context
            )
            
            # Store feedback
            self.feedback_storage.append(feedback)
            
            # Log feedback collection
            self.logger.info(
                "feedback_collected",
                user_id=user_id,
                restaurant_id=restaurant_id,
                feedback_type=feedback_type.value,
                rating=rating
            )
            
            return feedback
            
        except Exception as e:
            self.logger.error(f"Error collecting feedback: {str(e)}")
            raise
    
    def collect_batch_feedback(
        self,
        feedback_list: List[Dict[str, Any]]
    ) -> List[UserFeedback]:
        """
        Collect multiple feedback items in batch
        
        Args:
            feedback_list: List of feedback dictionaries
            
        Returns:
            List of UserFeedback objects
        """
        collected_feedback = []
        
        for feedback_data in feedback_list:
            try:
                feedback = self.collect_feedback(**feedback_data)
                collected_feedback.append(feedback)
            except Exception as e:
                self.logger.error(f"Error collecting batch feedback: {str(e)}")
                continue
        
        return collected_feedback
    
    def collect_recommendation_feedback(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_interactions: List[Dict[str, Any]]
    ) -> List[UserFeedback]:
        """
        Collect feedback from recommendation session interactions
        
        Args:
            phase4_result: Phase 4 recommendation result
            phase5_result: Phase 5 presentation result
            user_interactions: List of user interaction events
            
        Returns:
            List of UserFeedback objects
        """
        feedback_list = []
        
        try:
            # Extract session information
            session_id = user_interactions[0].get("session_id", "unknown") if user_interactions else "unknown"
            recommendation_id = phase4_result.metadata.get("request_id", "unknown")
            user_id = user_interactions[0].get("user_id", "anonymous") if user_interactions else "anonymous"
            
            # Process each interaction
            for interaction in user_interactions:
                interaction_type = interaction.get("type", "unknown")
                restaurant_id = interaction.get("restaurant_id")
                
                if not restaurant_id:
                    continue
                
                # Map interaction types to feedback types
                feedback_mapping = {
                    "like": FeedbackType.LIKE,
                    "dislike": FeedbackType.DISLIKE,
                    "bookmark": FeedbackType.BOOKMARK,
                    "visit": FeedbackType.VISIT,
                    "skip": FeedbackType.SKIP,
                    "share": FeedbackType.SHARE,
                    "rating": FeedbackType.RATING
                }
                
                feedback_type = feedback_mapping.get(interaction_type, FeedbackType.NEUTRAL)
                
                # Extract additional data
                rating = interaction.get("rating")
                helpfulness = interaction.get("helpfulness")
                comment = interaction.get("comment")
                reasons = interaction.get("reasons", [])
                context = {
                    "interaction_type": interaction_type,
                    "timestamp": interaction.get("timestamp"),
                    "duration": interaction.get("duration"),
                    "scroll_depth": interaction.get("scroll_depth"),
                    "device_type": interaction.get("device_type")
                }
                
                feedback = self.collect_feedback(
                    user_id=user_id,
                    session_id=session_id,
                    recommendation_id=recommendation_id,
                    restaurant_id=restaurant_id,
                    feedback_type=feedback_type,
                    feedback_source=FeedbackSource.AUTOMATIC,
                    rating=rating,
                    helpfulness=helpfulness,
                    comment=comment,
                    reasons=reasons,
                    context=context
                )
                
                feedback_list.append(feedback)
            
            self.logger.info(
                "recommendation_feedback_collected",
                session_id=session_id,
                feedback_count=len(feedback_list)
            )
            
            return feedback_list
            
        except Exception as e:
            self.logger.error(f"Error collecting recommendation feedback: {str(e)}")
            return []
    
    def aggregate_feedback(
        self,
        restaurant_id: Optional[str] = None,
        time_range: Optional[tuple] = None
    ) -> Dict[str, FeedbackAggregation]:
        """
        Aggregate feedback by restaurant
        
        Args:
            restaurant_id: Specific restaurant to aggregate (optional)
            time_range: Time range for aggregation (optional)
            
        Returns:
            Dictionary of restaurant_id -> FeedbackAggregation
        """
        try:
            # Filter feedback based on criteria
            filtered_feedback = self._filter_feedback(restaurant_id, time_range)
            
            # Group by restaurant
            feedback_by_restaurant = {}
            for feedback in filtered_feedback:
                if feedback.restaurant_id not in feedback_by_restaurant:
                    feedback_by_restaurant[feedback.restaurant_id] = []
                feedback_by_restaurant[feedback.restaurant_id].append(feedback)
            
            # Aggregate for each restaurant
            aggregated = {}
            for rid, feedbacks in feedback_by_restaurant.items():
                aggregated[rid] = self._calculate_aggregation(rid, feedbacks)
            
            # Update stored aggregations
            self.aggregated_feedback.update(aggregated)
            
            return aggregated
            
        except Exception as e:
            self.logger.error(f"Error aggregating feedback: {str(e)}")
            return {}
    
    def generate_insights(
        self,
        time_range: Optional[tuple] = None
    ) -> FeedbackInsights:
        """
        Generate insights from collected feedback
        
        Args:
            time_range: Time range for analysis (optional)
            
        Returns:
            FeedbackInsights object
        """
        try:
            # Filter feedback for analysis
            filtered_feedback = self._filter_feedback(None, time_range)
            
            if not filtered_feedback:
                return FeedbackInsights(
                    total_recommendations=0,
                    total_feedback=0,
                    feedback_rate=0.0,
                    average_rating=0.0,
                    top_performing_restaurants=[],
                    underperforming_restaurants=[],
                    common_issues=[],
                    improvement_suggestions=[],
                    user_satisfaction_trend=[],
                    generated_at=datetime.now(timezone.utc)
                )
            
            # Calculate basic metrics
            total_feedback = len(filtered_feedback)
            unique_recommendations = len(set(f.recommendation_id for f in filtered_feedback))
            feedback_rate = total_feedback / max(unique_recommendations, 1)
            
            # Calculate average rating
            ratings = [f.rating for f in filtered_feedback if f.rating is not None]
            average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Analyze restaurant performance
            restaurant_performance = self._analyze_restaurant_performance(filtered_feedback)
            
            # Identify common issues
            common_issues = self._identify_common_issues(filtered_feedback)
            
            # Generate improvement suggestions
            improvement_suggestions = self._generate_improvement_suggestions(
                filtered_feedback, common_issues
            )
            
            # Analyze satisfaction trend
            satisfaction_trend = self._analyze_satisfaction_trend(filtered_feedback)
            
            return FeedbackInsights(
                total_recommendations=unique_recommendations,
                total_feedback=total_feedback,
                feedback_rate=feedback_rate,
                average_rating=average_rating,
                top_performing_restaurants=restaurant_performance["top"],
                underperforming_restaurants=restaurant_performance["bottom"],
                common_issues=common_issues,
                improvement_suggestions=improvement_suggestions,
                user_satisfaction_trend=satisfaction_trend,
                generated_at=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            return FeedbackInsights(
                total_recommendations=0,
                total_feedback=0,
                feedback_rate=0.0,
                average_rating=0.0,
                top_performing_restaurants=[],
                underperforming_restaurants=[],
                common_issues=[],
                improvement_suggestions=[],
                user_satisfaction_trend=[],
                generated_at=datetime.now(timezone.utc)
            )
    
    def export_feedback(
        self,
        format: str = "json",
        restaurant_id: Optional[str] = None,
        time_range: Optional[tuple] = None
    ) -> str:
        """
        Export feedback data
        
        Args:
            format: Export format (json, csv)
            restaurant_id: Specific restaurant to export (optional)
            time_range: Time range for export (optional)
            
        Returns:
            Exported data as string
        """
        try:
            # Filter feedback
            filtered_feedback = self._filter_feedback(restaurant_id, time_range)
            
            # Convert to serializable format
            data = [asdict(f) for f in filtered_feedback]
            
            # Convert datetime objects
            for item in data:
                if item.get("timestamp"):
                    item["timestamp"] = item["timestamp"].isoformat()
            
            if format.lower() == "json":
                return json.dumps(data, indent=2)
            elif format.lower() == "csv":
                return self._convert_to_csv(data)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.logger.error(f"Error exporting feedback: {str(e)}")
            return ""
    
    def get_feedback_statistics(
        self,
        restaurant_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get feedback statistics
        
        Args:
            restaurant_id: Specific restaurant (optional)
            
        Returns:
            Dictionary of statistics
        """
        try:
            # Filter feedback
            filtered_feedback = self._filter_feedback(restaurant_id)
            
            if not filtered_feedback:
                return {
                    "total_feedback": 0,
                    "feedback_types": {},
                    "average_rating": 0.0,
                    "average_helpfulness": 0.0,
                    "sentiment_distribution": {}
                }
            
            # Calculate statistics
            total_feedback = len(filtered_feedback)
            
            # Feedback type distribution
            feedback_types = {}
            for feedback in filtered_feedback:
                ftype = feedback.feedback_type.value
                feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
            
            # Rating statistics
            ratings = [f.rating for f in filtered_feedback if f.rating is not None]
            average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Helpfulness statistics
            helpfulness = [f.helpfulness for f in filtered_feedback if f.helpfulness is not None]
            average_helpfulness = sum(helpfulness) / len(helpfulness) if helpfulness else 0.0
            
            # Sentiment distribution
            sentiment_distribution = {
                "positive": len([f for f in filtered_feedback if f.feedback_type in [FeedbackType.LIKE, FeedbackType.BOOKMARK, FeedbackType.VISIT, FeedbackType.SHARE]]),
                "negative": len([f for f in filtered_feedback if f.feedback_type == FeedbackType.DISLIKE]),
                "neutral": len([f for f in filtered_feedback if f.feedback_type == FeedbackType.NEUTRAL])
            }
            
            return {
                "total_feedback": total_feedback,
                "feedback_types": feedback_types,
                "average_rating": average_rating,
                "average_helpfulness": average_helpfulness,
                "sentiment_distribution": sentiment_distribution
            }
            
        except Exception as e:
            self.logger.error(f"Error getting feedback statistics: {str(e)}")
            return {}
    
    def _validate_feedback_data(
        self,
        feedback_type: FeedbackType,
        rating: Optional[int],
        helpfulness: Optional[int],
        reasons: Optional[List[str]],
        context: Optional[Dict[str, Any]]
    ):
        """Validate feedback data"""
        # Validate rating
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError("Rating must be between 1 and 5")
        
        # Validate helpfulness
        if helpfulness is not None and (helpfulness < 1 or helpfulness > 5):
            raise ValueError("Helpfulness must be between 1 and 5")
        
        # Validate reasons
        if reasons is not None and len(reasons) > 10:
            raise ValueError("Too many reasons provided (max 10)")
        
        # Validate context
        if context is not None and len(context) > 50:
            raise ValueError("Too much context data provided (max 50 keys)")
    
    def _filter_feedback(
        self,
        restaurant_id: Optional[str] = None,
        time_range: Optional[tuple] = None
    ) -> List[UserFeedback]:
        """Filter feedback based on criteria"""
        filtered = self.feedback_storage.copy()
        
        # Filter by restaurant
        if restaurant_id:
            filtered = [f for f in filtered if f.restaurant_id == restaurant_id]
        
        # Filter by time range
        if time_range:
            start_time, end_time = time_range
            filtered = [
                f for f in filtered 
                if start_time <= f.timestamp <= end_time
            ]
        
        return filtered
    
    def _calculate_aggregation(
        self,
        restaurant_id: str,
        feedbacks: List[UserFeedback]
    ) -> FeedbackAggregation:
        """Calculate aggregated feedback for a restaurant"""
        total_feedback = len(feedbacks)
        
        # Count feedback types
        feedback_types = {}
        for feedback in feedbacks:
            ftype = feedback.feedback_type.value
            feedback_types[ftype] = feedback_types.get(ftype, 0) + 1
        
        # Count sentiment
        positive = len([f for f in feedbacks if f.feedback_type in [FeedbackType.LIKE, FeedbackType.BOOKMARK, FeedbackType.VISIT, FeedbackType.SHARE]])
        negative = len([f for f in feedbacks if f.feedback_type == FeedbackType.DISLIKE])
        neutral = len([f for f in feedbacks if f.feedback_type == FeedbackType.NEUTRAL])
        
        # Calculate averages
        ratings = [f.rating for f in feedbacks if f.rating is not None]
        average_rating = sum(ratings) / len(ratings) if ratings else None
        
        helpfulness = [f.helpfulness for f in feedbacks if f.helpfulness is not None]
        average_helpfulness = sum(helpfulness) / len(helpfulness) if helpfulness else None
        
        # Find common reasons
        all_reasons = []
        for feedback in feedbacks:
            all_reasons.extend(feedback.reasons)
        
        reason_counts = {}
        for reason in all_reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        
        common_reasons = sorted(reason_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        common_reasons = [reason for reason, count in common_reasons]
        
        # Calculate sentiment score
        sentiment_score = (positive - negative) / max(total_feedback, 1)
        
        # Calculate confidence score
        confidence_score = min(total_feedback / 10, 1.0)  # More feedback = higher confidence
        
        return FeedbackAggregation(
            restaurant_id=restaurant_id,
            total_feedback=total_feedback,
            positive_feedback=positive,
            negative_feedback=negative,
            neutral_feedback=neutral,
            average_rating=average_rating,
            average_helpfulness=average_helpfulness,
            feedback_types=feedback_types,
            common_reasons=common_reasons,
            sentiment_score=sentiment_score,
            confidence_score=confidence_score,
            last_updated=datetime.now(timezone.utc)
        )
    
    def _analyze_restaurant_performance(
        self,
        feedbacks: List[UserFeedback]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze restaurant performance based on feedback"""
        # Group by restaurant
        restaurant_feedbacks = {}
        for feedback in feedbacks:
            if feedback.restaurant_id not in restaurant_feedbacks:
                restaurant_feedbacks[feedback.restaurant_id] = []
            restaurant_feedbacks[feedback.restaurant_id].append(feedback)
        
        # Calculate performance metrics
        performance_scores = {}
        for restaurant_id, restaurant_feedbacks_list in restaurant_feedbacks.items():
            # Calculate score based on feedback
            positive = len([f for f in restaurant_feedbacks_list if f.feedback_type in [FeedbackType.LIKE, FeedbackType.BOOKMARK, FeedbackType.VISIT, FeedbackType.SHARE]])
            negative = len([f for f in restaurant_feedbacks_list if f.feedback_type == FeedbackType.DISLIKE])
            total = len(restaurant_feedbacks_list)
            
            # Calculate weighted score
            score = (positive * 1.0 + negative * -1.0) / max(total, 1)
            
            # Add rating bonus
            ratings = [f.rating for f in restaurant_feedbacks_list if f.rating is not None]
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                score += (avg_rating - 3) * 0.2  # Bonus/penalty for rating
            
            performance_scores[restaurant_id] = {
                "restaurant_id": restaurant_id,
                "score": score,
                "total_feedback": total,
                "positive_feedback": positive,
                "negative_feedback": negative,
                "average_rating": sum(ratings) / len(ratings) if ratings else None
            }
        
        # Sort restaurants
        sorted_restaurants = sorted(
            performance_scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return {
            "top": sorted_restaurants[:5],
            "bottom": sorted_restaurants[-5:] if len(sorted_restaurants) > 5 else []
        }
    
    def _identify_common_issues(self, feedbacks: List[UserFeedback]) -> List[str]:
        """Identify common issues from feedback"""
        # Collect negative feedback reasons
        negative_reasons = []
        for feedback in feedbacks:
            if feedback.feedback_type == FeedbackType.DISLIKE and feedback.reasons:
                negative_reasons.extend(feedback.reasons)
        
        # Count reasons
        reason_counts = {}
        for reason in negative_reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        
        # Get most common issues
        common_issues = sorted(reason_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [issue for issue, count in common_issues[:5]]
    
    def _generate_improvement_suggestions(
        self,
        feedbacks: List[UserFeedback],
        common_issues: List[str]
    ) -> List[str]:
        """Generate improvement suggestions based on feedback"""
        suggestions = []
        
        # Analyze common issues and generate suggestions
        issue_suggestions = {
            "expensive": "Consider including more budget-friendly options",
            "poor service": "Prioritize restaurants with better service ratings",
            "bad location": "Improve location-based filtering",
            "limited options": "Increase variety in recommendations",
            "outdated information": "Update restaurant data more frequently",
            "not accurate": "Improve recommendation algorithm accuracy"
        }
        
        for issue in common_issues:
            for keyword, suggestion in issue_suggestions.items():
                if keyword.lower() in issue.lower():
                    suggestions.append(suggestion)
                    break
        
        # Add general suggestions based on feedback patterns
        low_rating_feedback = [f for f in feedbacks if f.rating and f.rating <= 2]
        if len(low_rating_feedback) > len(feedbacks) * 0.3:
            suggestions.append("Overall recommendation quality needs improvement")
        
        # Remove duplicates
        suggestions = list(set(suggestions))
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _analyze_satisfaction_trend(
        self,
        feedbacks: List[UserFeedback]
    ) -> List[Dict[str, Any]]:
        """Analyze user satisfaction trend over time"""
        # Group feedback by day
        daily_feedback = {}
        for feedback in feedbacks:
            date_key = feedback.timestamp.date()
            if date_key not in daily_feedback:
                daily_feedback[date_key] = []
            daily_feedback[date_key].append(feedback)
        
        # Calculate daily satisfaction
        trend_data = []
        for date, date_feedbacks in sorted(daily_feedback.items()):
            # Calculate satisfaction score for the day
            positive = len([f for f in date_feedbacks if f.feedback_type in [FeedbackType.LIKE, FeedbackType.BOOKMARK, FeedbackType.VISIT, FeedbackType.SHARE]])
            negative = len([f for f in date_feedbacks if f.feedback_type == FeedbackType.DISLIKE])
            total = len(date_feedbacks)
            
            satisfaction_score = (positive - negative) / max(total, 1)
            
            # Calculate average rating
            ratings = [f.rating for f in date_feedbacks if f.rating is not None]
            average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            trend_data.append({
                "date": date.isoformat(),
                "satisfaction_score": satisfaction_score,
                "average_rating": average_rating,
                "total_feedback": total
            })
        
        return trend_data
    
    def _convert_to_csv(self, data: List[Dict[str, Any]]) -> str:
        """Convert data to CSV format"""
        if not data:
            return ""
        
        # Get headers
        headers = list(data[0].keys())
        
        # Create CSV
        csv_lines = [",".join(headers)]
        
        for item in data:
            values = []
            for header in headers:
                value = item.get(header, "")
                if isinstance(value, str) and ("," in value or "\n" in value):
                    value = f'"{value.replace('"', '""')}"'
                values.append(str(value))
            csv_lines.append(",".join(values))
        
        return "\n".join(csv_lines)
