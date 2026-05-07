"""
Evaluation Metrics Tracker Module for Phase 6: Feedback, Evaluation, and Improvement Loop
Tracks and analyzes recommendation system performance metrics.
"""

import json
import time
import statistics
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime, timezone, timedelta
import math

# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result
from .feedback_collector import UserFeedback, FeedbackCollector


class MetricType(Enum):
    """Types of metrics to track"""
    PRECISION_AT_K = "precision_at_k"
    RECALL_AT_K = "recall_at_k"
    SATISFACTION_SCORE = "satisfaction_score"
    RESPONSE_LATENCY = "response_latency"
    CLICK_THROUGH_RATE = "click_through_rate"
    CONVERSION_RATE = "conversion_rate"
    DIVERSITY_SCORE = "diversity_score"
    NOVELTY_SCORE = "novelty_score"
    COVERAGE = "coverage"
    ERROR_RATE = "error_rate"
    TOKEN_EFFICIENCY = "token_efficiency"
    USER_ENGAGEMENT = "user_engagement"


class TimeGranularity(Enum):
    """Time granularity for metrics"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class MetricValue:
    """Individual metric value with metadata"""
    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict[str, Any]
    granularity: TimeGranularity
    sample_size: int
    confidence_interval: Optional[Tuple[float, float]] = None
    
    def __post_init__(self):
        if isinstance(self.metric_type, str):
            self.metric_type = MetricType(self.metric_type)
        if isinstance(self.granularity, str):
            self.granularity = TimeGranularity(self.granularity)


@dataclass
class MetricAggregation:
    """Aggregated metric over time period"""
    metric_type: MetricType
    granularity: TimeGranularity
    start_time: datetime
    end_time: datetime
    values: List[float]
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    trend: str  # increasing, decreasing, stable
    trend_strength: float
    sample_count: int
    
    def __post_init__(self):
        if isinstance(self.metric_type, str):
            self.metric_type = MetricType(self.metric_type)
        if isinstance(self.granularity, str):
            self.granularity = TimeGranularity(self.granularity)


@dataclass
class SystemPerformance:
    """Overall system performance summary"""
    period_start: datetime
    period_end: datetime
    total_recommendations: int
    total_users: int
    average_satisfaction: float
    average_response_time: float
    precision_at_5: float
    recall_at_5: float
    click_through_rate: float
    conversion_rate: float
    error_rate: float
    system_health_score: float
    top_issues: List[str]
    improvement_areas: List[str]


class MetricsTracker:
    """Tracks and analyzes recommendation system performance metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_storage: List[MetricValue] = []
        self.feedback_collector = FeedbackCollector()
        
        # Metric calculation functions
        self.metric_calculators = {
            MetricType.PRECISION_AT_K: self._calculate_precision_at_k,
            MetricType.RECALL_AT_K: self._calculate_recall_at_k,
            MetricType.SATISFACTION_SCORE: self._calculate_satisfaction_score,
            MetricType.RESPONSE_LATENCY: self._calculate_response_latency,
            MetricType.CLICK_THROUGH_RATE: self._calculate_click_through_rate,
            MetricType.CONVERSION_RATE: self._calculate_conversion_rate,
            MetricType.DIVERSITY_SCORE: self._calculate_diversity_score,
            MetricType.NOVELTY_SCORE: self._calculate_novelty_score,
            MetricType.COVERAGE: self._calculate_coverage,
            MetricType.ERROR_RATE: self._calculate_error_rate,
            MetricType.TOKEN_EFFICIENCY: self._calculate_token_efficiency,
            MetricType.USER_ENGAGEMENT: self._calculate_user_engagement
        }
    
    def track_recommendation_metrics(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, MetricValue]:
        """
        Track metrics for a recommendation session
        
        Args:
            phase4_result: Phase 4 recommendation result
            phase5_result: Phase 5 presentation result
            user_feedback: List of user feedback
            context: Additional context
            
        Returns:
            Dictionary of metric_type -> MetricValue
        """
        try:
            metrics = {}
            timestamp = datetime.now(timezone.utc)
            context = context or {}
            
            # Calculate all available metrics
            for metric_type, calculator in self.metric_calculators.items():
                try:
                    value, sample_size, confidence_interval = calculator(
                        phase4_result, phase5_result, user_feedback, context
                    )
                    
                    metric = MetricValue(
                        metric_type=metric_type,
                        value=value,
                        timestamp=timestamp,
                        context=context,
                        granularity=TimeGranularity.DAILY,
                        sample_size=sample_size,
                        confidence_interval=confidence_interval
                    )
                    
                    metrics[metric_type] = metric
                    self.metrics_storage.append(metric)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to calculate {metric_type.value}: {str(e)}")
                    continue
            
            self.logger.info(
                "recommendation_metrics_tracked",
                metrics_count=len(metrics),
                session_id=context.get("session_id", "unknown")
            )
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking recommendation metrics: {str(e)}")
            return {}
    
    def track_system_metrics(
        self,
        system_metrics: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[MetricValue]:
        """
        Track system-level metrics
        
        Args:
            system_metrics: Dictionary of system metrics
            context: Additional context
            
        Returns:
            List of MetricValue objects
        """
        try:
            metrics = []
            timestamp = datetime.now(timezone.utc)
            context = context or {}
            
            # Track system health metrics
            if "cpu_usage" in system_metrics:
                metric = MetricValue(
                    metric_type=MetricType.USER_ENGAGEMENT,
                    value=100.0 - system_metrics["cpu_usage"],  # Inverse for health
                    timestamp=timestamp,
                    context={**context, "metric": "cpu_health"},
                    granularity=TimeGranularity.HOURLY,
                    sample_size=1
                )
                metrics.append(metric)
                self.metrics_storage.append(metric)
            
            if "memory_usage" in system_metrics:
                metric = MetricValue(
                    metric_type=MetricType.USER_ENGAGEMENT,
                    value=100.0 - system_metrics["memory_usage"],  # Inverse for health
                    timestamp=timestamp,
                    context={**context, "metric": "memory_health"},
                    granularity=TimeGranularity.HOURLY,
                    sample_size=1
                )
                metrics.append(metric)
                self.metrics_storage.append(metric)
            
            if "api_response_time" in system_metrics:
                metric = MetricValue(
                    metric_type=MetricType.RESPONSE_LATENCY,
                    value=system_metrics["api_response_time"],
                    timestamp=timestamp,
                    context={**context, "metric": "api_response_time"},
                    granularity=TimeGranularity.HOURLY,
                    sample_size=1
                )
                metrics.append(metric)
                self.metrics_storage.append(metric)
            
            self.logger.info(
                "system_metrics_tracked",
                metrics_count=len(metrics)
            )
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error tracking system metrics: {str(e)}")
            return []
    
    def get_metric_history(
        self,
        metric_type: Union[MetricType, str],
        time_range: Optional[Tuple[datetime, datetime]] = None,
        granularity: Optional[TimeGranularity] = None
    ) -> List[MetricValue]:
        """
        Get historical values for a specific metric
        
        Args:
            metric_type: Type of metric
            time_range: Time range to filter (optional)
            granularity: Time granularity to filter (optional)
            
        Returns:
            List of MetricValue objects
        """
        try:
            if isinstance(metric_type, str):
                metric_type = MetricType(metric_type)
            
            # Filter metrics
            filtered_metrics = [
                m for m in self.metrics_storage
                if m.metric_type == metric_type
            ]
            
            # Filter by time range
            if time_range:
                start_time, end_time = time_range
                filtered_metrics = [
                    m for m in filtered_metrics
                    if start_time <= m.timestamp <= end_time
                ]
            
            # Filter by granularity
            if granularity:
                filtered_metrics = [
                    m for m in filtered_metrics
                    if m.granularity == granularity
                ]
            
            # Sort by timestamp
            filtered_metrics.sort(key=lambda x: x.timestamp)
            
            return filtered_metrics
            
        except Exception as e:
            self.logger.error(f"Error getting metric history: {str(e)}")
            return []
    
    def aggregate_metrics(
        self,
        metric_type: Union[MetricType, str],
        granularity: TimeGranularity,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> MetricAggregation:
        """
        Aggregate metrics over time period
        
        Args:
            metric_type: Type of metric to aggregate
            granularity: Time granularity for aggregation
            time_range: Time range for aggregation (optional)
            
        Returns:
            MetricAggregation object
        """
        try:
            if isinstance(metric_type, str):
                metric_type = MetricType(metric_type)
            
            # Get metrics for the period
            metrics = self.get_metric_history(metric_type, time_range)
            
            if not metrics:
                raise ValueError(f"No metrics found for {metric_type.value}")
            
            # Extract values
            values = [m.value for m in metrics]
            timestamps = [m.timestamp for m in metrics]
            
            # Calculate statistics
            mean = statistics.mean(values)
            median = statistics.median(values)
            std_dev = statistics.stdev(values) if len(values) > 1 else 0.0
            min_value = min(values)
            max_value = max(values)
            
            # Calculate trend
            trend, trend_strength = self._calculate_trend(values)
            
            # Determine time range
            start_time = min(timestamps)
            end_time = max(timestamps)
            
            return MetricAggregation(
                metric_type=metric_type,
                granularity=granularity,
                start_time=start_time,
                end_time=end_time,
                values=values,
                mean=mean,
                median=median,
                std_dev=std_dev,
                min_value=min_value,
                max_value=max_value,
                trend=trend,
                trend_strength=trend_strength,
                sample_count=len(values)
            )
            
        except Exception as e:
            self.logger.error(f"Error aggregating metrics: {str(e)}")
            raise
    
    def generate_performance_report(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> SystemPerformance:
        """
        Generate comprehensive performance report
        
        Args:
            time_range: Time range for report (optional)
            
        Returns:
            SystemPerformance object
        """
        try:
            # Set default time range (last 7 days)
            if time_range is None:
                end_time = datetime.now(timezone.utc)
                start_time = end_time - timedelta(days=7)
                time_range = (start_time, end_time)
            
            start_time, end_time = time_range
            
            # Get metrics for the period
            satisfaction_metrics = self.get_metric_history(
                MetricType.SATISFACTION_SCORE, time_range
            )
            latency_metrics = self.get_metric_history(
                MetricType.RESPONSE_LATENCY, time_range
            )
            precision_metrics = self.get_metric_history(
                MetricType.PRECISION_AT_K, time_range
            )
            recall_metrics = self.get_metric_history(
                MetricType.RECALL_AT_K, time_range
            )
            ctr_metrics = self.get_metric_history(
                MetricType.CLICK_THROUGH_RATE, time_range
            )
            conversion_metrics = self.get_metric_history(
                MetricType.CONVERSION_RATE, time_range
            )
            error_metrics = self.get_metric_history(
                MetricType.ERROR_RATE, time_range
            )
            
            # Calculate averages
            avg_satisfaction = statistics.mean([m.value for m in satisfaction_metrics]) if satisfaction_metrics else 0.0
            avg_latency = statistics.mean([m.value for m in latency_metrics]) if latency_metrics else 0.0
            precision_at_5 = statistics.mean([m.value for m in precision_metrics]) if precision_metrics else 0.0
            recall_at_5 = statistics.mean([m.value for m in recall_metrics]) if recall_metrics else 0.0
            ctr = statistics.mean([m.value for m in ctr_metrics]) if ctr_metrics else 0.0
            conversion = statistics.mean([m.value for m in conversion_metrics]) if conversion_metrics else 0.0
            error_rate = statistics.mean([m.value for m in error_metrics]) if error_metrics else 0.0
            
            # Calculate system health score
            health_score = self._calculate_system_health_score(
                avg_satisfaction, avg_latency, precision_at_5, error_rate
            )
            
            # Identify issues and improvements
            top_issues = self._identify_top_issues(
                avg_satisfaction, avg_latency, error_rate, precision_at_5
            )
            improvement_areas = self._identify_improvement_areas(
                avg_satisfaction, ctr, conversion, recall_at_5
            )
            
            # Count total recommendations and users
            total_recommendations = len(set(m.context.get("session_id") for m in self.metrics_storage if m.context.get("session_id")))
            total_users = len(set(m.context.get("user_id") for m in self.metrics_storage if m.context.get("user_id")))
            
            return SystemPerformance(
                period_start=start_time,
                period_end=end_time,
                total_recommendations=total_recommendations,
                total_users=total_users,
                average_satisfaction=avg_satisfaction,
                average_response_time=avg_latency,
                precision_at_5=precision_at_5,
                recall_at_5=recall_at_5,
                click_through_rate=ctr,
                conversion_rate=conversion,
                error_rate=error_rate,
                system_health_score=health_score,
                top_issues=top_issues,
                improvement_areas=improvement_areas
            )
            
        except Exception as e:
            self.logger.error(f"Error generating performance report: {str(e)}")
            raise
    
    def export_metrics(
        self,
        format: str = "json",
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> str:
        """
        Export metrics data
        
        Args:
            format: Export format (json, csv)
            time_range: Time range for export (optional)
            
        Returns:
            Exported data as string
        """
        try:
            # Filter metrics by time range
            if time_range:
                start_time, end_time = time_range
                filtered_metrics = [
                    m for m in self.metrics_storage
                    if start_time <= m.timestamp <= end_time
                ]
            else:
                filtered_metrics = self.metrics_storage
            
            # Convert to serializable format
            data = []
            for metric in filtered_metrics:
                item = asdict(metric)
                item["metric_type"] = metric.metric_type.value
                item["granularity"] = metric.granularity.value
                item["timestamp"] = metric.timestamp.isoformat()
                if item["confidence_interval"]:
                    item["confidence_interval"] = list(item["confidence_interval"])
                data.append(item)
            
            if format.lower() == "json":
                return json.dumps(data, indent=2)
            elif format.lower() == "csv":
                return self._convert_to_csv(data)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return ""
    
    # Metric calculation methods
    def _calculate_precision_at_k(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate precision@k metric"""
        try:
            k = 5  # Default k value
            if "k" in context:
                k = context["k"]
            
            # Get recommended restaurants
            recommendations = phase4_result.recommendations[:k]
            recommended_ids = {rec.get("restaurant_name", "") for rec in recommendations}
            
            # Get positive feedback
            positive_feedback = [
                f for f in user_feedback
                if f.feedback_type.value in ["like", "bookmark", "visit"]
            ]
            positive_ids = {f.restaurant_id for f in positive_feedback}
            
            # Calculate precision@k
            if recommended_ids:
                precision = len(recommended_ids & positive_ids) / len(recommended_ids)
            else:
                precision = 0.0
            
            # Calculate confidence interval
            sample_size = len(recommended_ids)
            confidence_interval = self._calculate_confidence_interval(precision, sample_size)
            
            return precision, sample_size, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating precision@k: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_recall_at_k(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate recall@k metric"""
        try:
            k = 5  # Default k value
            if "k" in context:
                k = context["k"]
            
            # Get recommended restaurants
            recommendations = phase4_result.recommendations[:k]
            recommended_ids = {rec.get("restaurant_name", "") for rec in recommendations}
            
            # Get all positive feedback (ground truth)
            positive_feedback = [
                f for f in user_feedback
                if f.feedback_type.value in ["like", "bookmark", "visit"]
            ]
            positive_ids = {f.restaurant_id for f in positive_feedback}
            
            # Calculate recall@k
            if positive_ids:
                recall = len(recommended_ids & positive_ids) / len(positive_ids)
            else:
                recall = 0.0
            
            # Calculate confidence interval
            sample_size = len(positive_ids)
            confidence_interval = self._calculate_confidence_interval(recall, sample_size)
            
            return recall, sample_size, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating recall@k: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_satisfaction_score(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate user satisfaction score"""
        try:
            if not user_feedback:
                return 0.0, 0, None
            
            # Calculate satisfaction based on feedback types and ratings
            satisfaction_scores = []
            
            for feedback in user_feedback:
                score = 0.0
                
                # Base score from feedback type
                if feedback.feedback_type.value == "like":
                    score += 4.0
                elif feedback.feedback_type.value == "bookmark":
                    score += 3.5
                elif feedback.feedback_type.value == "visit":
                    score += 5.0
                elif feedback.feedback_type.value == "share":
                    score += 4.5
                elif feedback.feedback_type.value == "neutral":
                    score += 2.5
                elif feedback.feedback_type.value == "dislike":
                    score += 1.0
                elif feedback.feedback_type.value == "skip":
                    score += 1.5
                
                # Adjust based on rating
                if feedback.rating:
                    score = (score + feedback.rating) / 2
                
                # Adjust based on helpfulness
                if feedback.helpfulness:
                    score = (score + feedback.helpfulness) / 2
                
                satisfaction_scores.append(score)
            
            # Calculate average satisfaction
            avg_satisfaction = statistics.mean(satisfaction_scores)
            
            # Normalize to 0-1 scale
            avg_satisfaction = avg_satisfaction / 5.0
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                avg_satisfaction, len(satisfaction_scores)
            )
            
            return avg_satisfaction, len(satisfaction_scores), confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating satisfaction score: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_response_latency(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate response latency"""
        try:
            # Get processing times from results
            phase4_time = phase4_result.processing_time if hasattr(phase4_result, 'processing_time') else 0.0
            phase5_time = phase5_result.processing_time if hasattr(phase5_result, 'processing_time') else 0.0
            
            total_latency = phase4_time + phase5_time
            
            # Sample size is 1 for single request
            sample_size = 1
            
            # No confidence interval for single sample
            confidence_interval = None
            
            return total_latency, sample_size, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating response latency: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_click_through_rate(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate click-through rate"""
        try:
            # Count clicks (bookmarks, visits, shares)
            clicks = len([
                f for f in user_feedback
                if f.feedback_type.value in ["bookmark", "visit", "share"]
            ])
            
            # Count total recommendations shown
            total_recommendations = len(phase4_result.recommendations)
            
            # Calculate CTR
            ctr = clicks / max(total_recommendations, 1)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(ctr, total_recommendations)
            
            return ctr, total_recommendations, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating click-through rate: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_conversion_rate(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate conversion rate (actual visits)"""
        try:
            # Count conversions (visits)
            conversions = len([
                f for f in user_feedback
                if f.feedback_type.value == "visit"
            ])
            
            # Count total recommendations shown
            total_recommendations = len(phase4_result.recommendations)
            
            # Calculate conversion rate
            conversion_rate = conversions / max(total_recommendations, 1)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                conversion_rate, total_recommendations
            )
            
            return conversion_rate, total_recommendations, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating conversion rate: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_diversity_score(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate diversity score of recommendations"""
        try:
            recommendations = phase4_result.recommendations
            
            if len(recommendations) < 2:
                return 0.0, len(recommendations), None
            
            # Calculate diversity based on cuisine types
            cuisines = [rec.get("cuisine", "") for rec in recommendations]
            unique_cuisines = len(set(cuisines))
            cuisine_diversity = unique_cuisines / len(cuisines)
            
            # Calculate diversity based on price ranges
            price_ranges = [rec.get("price_range", "") for rec in recommendations]
            unique_prices = len(set(price_ranges))
            price_diversity = unique_prices / len(price_ranges)
            
            # Combine diversity scores
            overall_diversity = (cuisine_diversity + price_diversity) / 2
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                overall_diversity, len(recommendations)
            )
            
            return overall_diversity, len(recommendations), confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating diversity score: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_novelty_score(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate novelty score of recommendations"""
        try:
            recommendations = phase4_result.recommendations
            
            if not recommendations:
                return 0.0, 0, None
            
            # For this implementation, we'll use rating as a proxy for novelty
            # Lower-rated restaurants might be more novel to users
            ratings = [rec.get("rating", 0) for rec in recommendations if rec.get("rating")]
            
            if not ratings:
                return 0.0, len(recommendations), None
            
            # Calculate novelty as inverse of average rating
            avg_rating = statistics.mean(ratings)
            novelty = 1.0 - (avg_rating / 5.0)  # Normalize to 0-1
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(novelty, len(ratings))
            
            return novelty, len(ratings), confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating novelty score: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_coverage(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate catalog coverage"""
        try:
            # This is a simplified implementation
            # In practice, you'd track all restaurants ever recommended
            total_restaurants = context.get("total_restaurants", 1000)  # Default assumption
            recommended_restaurants = len(phase4_result.recommendations)
            
            coverage = min(recommended_restaurants / total_restaurants, 1.0)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                coverage, recommended_restaurants
            )
            
            return coverage, recommended_restaurants, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating coverage: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_error_rate(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate error rate"""
        try:
            # Check if there were any errors in the pipeline
            phase4_error = not phase4_result.success if hasattr(phase4_result, 'success') else False
            phase5_error = not phase5_result.success if hasattr(phase5_result, 'success') else False
            
            # Error rate is 1.0 if any phase failed, 0.0 otherwise
            error_rate = 1.0 if (phase4_error or phase5_error) else 0.0
            
            # Sample size is 1 for single request
            sample_size = 1
            
            # No confidence interval for single sample
            confidence_interval = None
            
            return error_rate, sample_size, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating error rate: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_token_efficiency(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate token efficiency"""
        try:
            # Get token usage from Phase 4
            tokens_used = context.get("tokens_used", 0)
            recommendations_count = len(phase4_result.recommendations)
            
            if tokens_used == 0 or recommendations_count == 0:
                return 0.0, 0, None
            
            # Efficiency = recommendations per token
            efficiency = recommendations_count / tokens_used
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                efficiency, recommendations_count
            )
            
            return efficiency, recommendations_count, confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating token efficiency: {str(e)}")
            return 0.0, 0, None
    
    def _calculate_user_engagement(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_feedback: List[UserFeedback],
        context: Dict[str, Any]
    ) -> Tuple[float, int, Optional[Tuple[float, float]]]:
        """Calculate user engagement score"""
        try:
            if not user_feedback:
                return 0.0, 0, None
            
            # Calculate engagement based on feedback types and interactions
            engagement_scores = []
            
            for feedback in user_feedback:
                score = 0.0
                
                # High engagement actions
                if feedback.feedback_type.value in ["visit", "share"]:
                    score += 1.0
                elif feedback.feedback_type.value == "bookmark":
                    score += 0.8
                elif feedback.feedback_type.value == "like":
                    score += 0.6
                elif feedback.feedback_type.value == "dislike":
                    score += 0.4
                elif feedback.feedback_type.value == "neutral":
                    score += 0.2
                
                # Bonus for comments
                if feedback.comment:
                    score += 0.3
                
                # Bonus for reasons
                if feedback.reasons:
                    score += 0.2 * len(feedback.reasons)
                
                engagement_scores.append(min(score, 1.0))  # Cap at 1.0
            
            # Calculate average engagement
            avg_engagement = statistics.mean(engagement_scores)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                avg_engagement, len(engagement_scores)
            )
            
            return avg_engagement, len(engagement_scores), confidence_interval
            
        except Exception as e:
            self.logger.error(f"Error calculating user engagement: {str(e)}")
            return 0.0, 0, None
    
    # Helper methods
    def _calculate_confidence_interval(
        self,
        value: float,
        sample_size: int,
        confidence: float = 0.95
    ) -> Optional[Tuple[float, float]]:
        """Calculate confidence interval for a value"""
        try:
            if sample_size < 2:
                return None
            
            # Standard error
            std_error = math.sqrt(value * (1 - value) / sample_size)
            
            # Z-score for 95% confidence
            z_score = 1.96
            
            # Confidence interval
            margin_error = z_score * std_error
            lower_bound = max(0, value - margin_error)
            upper_bound = min(1, value + margin_error)
            
            return (lower_bound, upper_bound)
            
        except Exception:
            return None
    
    def _calculate_trend(self, values: List[float]) -> Tuple[str, float]:
        """Calculate trend direction and strength"""
        try:
            if len(values) < 2:
                return "stable", 0.0
            
            # Simple linear regression
            n = len(values)
            x = list(range(n))
            y = values
            
            # Calculate slope
            x_mean = statistics.mean(x)
            y_mean = statistics.mean(y)
            
            numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                return "stable", 0.0
            
            slope = numerator / denominator
            
            # Determine trend direction
            if abs(slope) < 0.01:
                trend = "stable"
            elif slope > 0:
                trend = "increasing"
            else:
                trend = "decreasing"
            
            # Calculate trend strength (normalized)
            trend_strength = min(abs(slope) * 10, 1.0)
            
            return trend, trend_strength
            
        except Exception:
            return "stable", 0.0
    
    def _calculate_system_health_score(
        self,
        satisfaction: float,
        latency: float,
        precision: float,
        error_rate: float
    ) -> float:
        """Calculate overall system health score"""
        try:
            # Weight different factors
            satisfaction_weight = 0.3
            latency_weight = 0.2
            precision_weight = 0.3
            error_weight = 0.2
            
            # Normalize metrics to 0-1 scale
            satisfaction_score = satisfaction  # Already 0-1
            latency_score = max(0, 1 - (latency / 5.0))  # Assume 5s as max acceptable
            precision_score = precision  # Already 0-1
            error_score = max(0, 1 - error_rate)  # Invert error rate
            
            # Calculate weighted average
            health_score = (
                satisfaction_score * satisfaction_weight +
                latency_score * latency_weight +
                precision_score * precision_weight +
                error_score * error_weight
            )
            
            return health_score
            
        except Exception:
            return 0.0
    
    def _identify_top_issues(
        self,
        satisfaction: float,
        latency: float,
        error_rate: float,
        precision: float
    ) -> List[str]:
        """Identify top system issues"""
        issues = []
        
        if satisfaction < 0.7:
            issues.append("Low user satisfaction")
        
        if latency > 3.0:
            issues.append("High response latency")
        
        if error_rate > 0.1:
            issues.append("High error rate")
        
        if precision < 0.6:
            issues.append("Low recommendation precision")
        
        return issues[:5]  # Return top 5 issues
    
    def _identify_improvement_areas(
        self,
        satisfaction: float,
        ctr: float,
        conversion: float,
        recall: float
    ) -> List[str]:
        """Identify areas for improvement"""
        areas = []
        
        if satisfaction < 0.8:
            areas.append("Improve user satisfaction")
        
        if ctr < 0.3:
            areas.append("Increase click-through rate")
        
        if conversion < 0.1:
            areas.append "Improve conversion rate"
        
        if recall < 0.5:
            areas.append("Increase recommendation recall")
        
        return areas[:5]  # Return top 5 areas
    
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
