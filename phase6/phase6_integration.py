"""
Phase 6 Integration Module for Feedback, Evaluation, and Improvement Loop
Main integration point for all Phase 6 components.
"""

import time
import uuid
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
import logging

# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result

# Import Phase 6 components
from phase6.feedback_collector import (
    FeedbackCollector, UserFeedback, FeedbackType, FeedbackSource,
    FeedbackInsights, FeedbackAggregation
)
from phase6.metrics_tracker import (
    MetricsTracker, MetricType, MetricValue, SystemPerformance,
    MetricAggregation, TimeGranularity
)
from phase6.prompt_version_manager import (
    PromptVersionManager, PromptTemplate, Experiment, ExperimentResult,
    PromptType, ExperimentStatus, VariantType
)
from phase6.monitoring_logging import (
    MonitoringAndLogging, MonitoringLogger, LogLevel, AlertSeverity,
    MetricCategory, SystemMetric, Alert
)


@dataclass
class Phase6Config:
    """Configuration for Phase 6 operations"""
    enable_feedback_collection: bool = True
    enable_metrics_tracking: bool = True
    enable_prompt_testing: bool = True
    enable_monitoring: bool = True
    
    # Feedback collection settings
    feedback_retention_days: int = 90
    auto_aggregate_feedback: bool = True
    feedback_aggregation_interval_hours: int = 24
    
    # Metrics tracking settings
    metrics_retention_days: int = 30
    metrics_aggregation_interval_hours: int = 1
    performance_report_interval_hours: int = 24
    
    # A/B testing settings
    default_sample_size: int = 1000
    default_confidence_level: float = 0.95
    experiment_auto_stop_enabled: bool = True
    
    # Monitoring settings
    monitoring_interval_seconds: int = 30
    health_check_interval_seconds: int = 60
    alert_threshold_cpu: float = 80.0
    alert_threshold_memory: float = 85.0
    alert_threshold_disk: float = 90.0
    
    # Logging settings
    log_retention_days: int = 7
    log_level: LogLevel = LogLevel.INFO
    structured_logging: bool = True


@dataclass
class Phase6Result:
    """Result of Phase 6 processing"""
    success: bool
    session_id: str
    user_id: str
    processing_time: float
    
    # Feedback results
    feedback_collected: int
    feedback_insights: Optional[FeedbackInsights]
    
    # Metrics results
    metrics_tracked: Dict[str, float]
    system_performance: Optional[SystemPerformance]
    
    # A/B testing results
    experiment_participated: Optional[str]
    template_used: Optional[str]
    
    # Monitoring results
    alerts_triggered: List[str]
    health_status: Dict[str, Any]
    
    # Metadata
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
        if isinstance(self.log_level, str):
            self.log_level = LogLevel(self.log_level)


class Phase6Integration:
    """Main integration class for Phase 6: Feedback, Evaluation, and Improvement Loop"""
    
    def __init__(self, config: Optional[Phase6Config] = None):
        self.config = config or Phase6Config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.feedback_collector = FeedbackCollector()
        self.metrics_tracker = MetricsTracker()
        self.prompt_manager = PromptVersionManager()
        self.monitoring = MonitoringAndLogging()
        
        # Component logger
        self.component_logger = self.monitoring.get_logger("phase6_integration")
        
        # Background processing
        self._background_tasks_enabled = False
        self._last_aggregation_time = {}
        self._last_report_time = {}
        
        # Start background tasks if enabled
        if self.config.enable_monitoring:
            self._start_background_tasks()
        
        self.component_logger.info(
            "Phase 6 Integration initialized",
            config=asdict(self.config)
        )
    
    def process_recommendation_session(
        self,
        user_id: str,
        session_id: str,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_interactions: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> Phase6Result:
        """
        Process a complete recommendation session through Phase 6
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            phase4_result: Phase 4 recommendation result
            phase5_result: Phase 5 presentation result
            user_interactions: List of user interaction events
            context: Additional context
            
        Returns:
            Phase6Result with all processing outcomes
        """
        start_time = time.time()
        timestamp = datetime.now(timezone.utc)
        context = context or {}
        
        try:
            self.component_logger.info(
                "Phase 6 processing started",
                user_id=user_id,
                session_id=session_id
            )
            
            # Initialize result
            result = Phase6Result(
                success=True,
                session_id=session_id,
                user_id=user_id,
                processing_time=0.0,
                feedback_collected=0,
                feedback_insights=None,
                metrics_tracked={},
                system_performance=None,
                experiment_participated=None,
                template_used=None,
                alerts_triggered=[],
                health_status={},
                timestamp=timestamp,
                metadata={}
            )
            
            # 1. Collect user feedback
            if self.config.enable_feedback_collection and user_interactions:
                feedback_data = self._collect_user_feedback(
                    user_id, session_id, phase4_result, phase5_result, user_interactions, context
                )
                result.feedback_collected = len(feedback_data)
                
                # Generate feedback insights
                if self.config.auto_aggregate_feedback:
                    result.feedback_insights = self.feedback_collector.generate_insights()
            
            # 2. Track metrics
            if self.config.enable_metrics_tracking:
                metrics_data = self._track_session_metrics(
                    phase4_result, phase5_result, user_interactions, context
                )
                result.metrics_tracked = {k.value: v.value for k, v in metrics_data.items()}
            
            # 3. Handle A/B testing
            if self.config.enable_prompt_testing:
                experiment_data = self._handle_prompt_testing(
                    user_id, session_id, phase4_result, user_interactions, context
                )
                result.experiment_participated = experiment_data.get("experiment_id")
                result.template_used = experiment_data.get("template_id")
            
            # 4. System monitoring
            if self.config.enable_monitoring:
                monitoring_data = self._perform_monitoring_checks(context)
                result.alerts_triggered = monitoring_data["alerts"]
                result.health_status = monitoring_data["health"]
            
            # Calculate processing time
            result.processing_time = time.time() - start_time
            
            # Log completion
            self.component_logger.info(
                "Phase 6 processing completed",
                user_id=user_id,
                session_id=session_id,
                processing_time_ms=result.processing_time * 1000,
                feedback_collected=result.feedback_collected,
                metrics_tracked=len(result.metrics_tracked)
            )
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            self.component_logger.error(
                "Phase 6 processing failed",
                user_id=user_id,
                session_id=session_id,
                error=str(e),
                processing_time_ms=processing_time * 1000
            )
            
            # Return error result
            return Phase6Result(
                success=False,
                session_id=session_id,
                user_id=user_id,
                processing_time=processing_time,
                feedback_collected=0,
                feedback_insights=None,
                metrics_tracked={},
                system_performance=None,
                experiment_participated=None,
                template_used=None,
                alerts_triggered=[],
                health_status={},
                timestamp=timestamp,
                metadata={"error": str(e)}
            )
    
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
        Collect individual user feedback
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            recommendation_id: Recommendation identifier
            restaurant_id: Restaurant identifier
            feedback_type: Type of feedback
            feedback_source: Source of feedback
            rating: User rating (1-5)
            helpfulness: Helpfulness rating (1-5)
            comment: User comment
            reasons: Reasons for feedback
            context: Additional context
            
        Returns:
            Collected UserFeedback object
        """
        try:
            feedback = self.feedback_collector.collect_feedback(
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
            
            self.component_logger.info(
                "Feedback collected",
                user_id=user_id,
                restaurant_id=restaurant_id,
                feedback_type=feedback_type.value if isinstance(feedback_type, FeedbackType) else feedback_type,
                rating=rating
            )
            
            return feedback
            
        except Exception as e:
            self.component_logger.error(
                "Error collecting feedback",
                user_id=user_id,
                restaurant_id=restaurant_id,
                error=str(e)
            )
            raise
    
    def get_feedback_insights(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> FeedbackInsights:
        """Get feedback insights and analytics"""
        try:
            insights = self.feedback_collector.generate_insights(time_range)
            
            self.component_logger.info(
                "Feedback insights generated",
                time_range=time_range,
                total_feedback=insights.total_feedback
            )
            
            return insights
            
        except Exception as e:
            self.component_logger.error(
                "Error generating feedback insights",
                error=str(e)
            )
            raise
    
    def get_performance_metrics(
        self,
        metric_type: Optional[MetricType] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        granularity: Optional[TimeGranularity] = None
    ) -> Union[MetricAggregation, Dict[str, MetricAggregation]]:
        """Get performance metrics and aggregations"""
        try:
            if metric_type:
                # Get specific metric aggregation
                aggregation = self.metrics_tracker.aggregate_metrics(
                    metric_type, granularity or TimeGranularity.DAILY, time_range
                )
                
                self.component_logger.info(
                    "Performance metrics retrieved",
                    metric_type=metric_type.value,
                    granularity=(granularity or TimeGranularity.DAILY).value
                )
                
                return aggregation
            else:
                # Get all metric aggregations
                all_metrics = {}
                for mtype in MetricType:
                    try:
                        aggregation = self.metrics_tracker.aggregate_metrics(
                            mtype, granularity or TimeGranularity.DAILY, time_range
                        )
                        all_metrics[mtype.value] = aggregation
                    except Exception:
                        continue  # Skip metrics that don't have data
                
                self.component_logger.info(
                    "All performance metrics retrieved",
                    metrics_count=len(all_metrics),
                    granularity=(granularity or TimeGranularity.DAILY).value
                )
                
                return all_metrics
                
        except Exception as e:
            self.component_logger.error(
                "Error retrieving performance metrics",
                error=str(e)
            )
            raise
    
    def create_a_b_experiment(
        self,
        name: str,
        description: str,
        prompt_type: PromptType,
        control_template_id: str,
        treatment_template_ids: List[str],
        traffic_split: Optional[Dict[str, float]] = None,
        sample_size: int = 1000,
        confidence_level: float = 0.95
    ) -> Experiment:
        """Create a new A/B testing experiment"""
        try:
            experiment = self.prompt_manager.create_experiment(
                name=name,
                description=description,
                prompt_type=prompt_type,
                control_template_id=control_template_id,
                treatment_template_ids=treatment_template_ids,
                traffic_split=traffic_split,
                sample_size=sample_size,
                confidence_level=confidence_level
            )
            
            self.component_logger.info(
                "A/B experiment created",
                experiment_id=experiment.id,
                name=name,
                control_template=control_template_id,
                treatment_templates=treatment_template_ids
            )
            
            return experiment
            
        except Exception as e:
            self.component_logger.error(
                "Error creating A/B experiment",
                name=name,
                error=str(e)
            )
            raise
    
    def start_experiment(self, experiment_id: str) -> Experiment:
        """Start an A/B testing experiment"""
        try:
            experiment = self.prompt_manager.start_experiment(experiment_id)
            
            self.component_logger.info(
                "A/B experiment started",
                experiment_id=experiment_id,
                name=experiment.name
            )
            
            return experiment
            
        except Exception as e:
            self.component_logger.error(
                "Error starting A/B experiment",
                experiment_id=experiment_id,
                error=str(e)
            )
            raise
    
    def get_experiment_results(self, experiment_id: str) -> ExperimentResult:
        """Get results of an A/B testing experiment"""
        try:
            results = self.prompt_manager.analyze_experiment_results(experiment_id)
            
            self.component_logger.info(
                "Experiment results retrieved",
                experiment_id=experiment_id,
                winner=results.winner,
                statistical_significance=results.statistical_significance
            )
            
            return results
            
        except Exception as e:
            self.component_logger.error(
                "Error retrieving experiment results",
                experiment_id=experiment_id,
                error=str(e)
            )
            raise
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        try:
            health_status = self.monitoring.system_monitor.get_system_health()
            
            self.component_logger.info(
                "System health retrieved",
                overall_status=health_status["overall_status"],
                active_alerts=health_status["active_alerts"]
            )
            
            return health_status
            
        except Exception as e:
            self.component_logger.error(
                "Error retrieving system health",
                error=str(e)
            )
            raise
    
    def get_monitoring_report(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Get comprehensive monitoring report"""
        try:
            report = self.monitoring.system_monitor.generate_monitoring_report(time_range)
            
            self.component_logger.info(
                "Monitoring report generated",
                time_range=time_range,
                recommendations_count=len(report.get("recommendations", []))
            )
            
            return report
            
        except Exception as e:
            self.component_logger.error(
                "Error generating monitoring report",
                error=str(e)
            )
            raise
    
    def get_comprehensive_dashboard(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        try:
            # Set default time range (last 7 days)
            if time_range is None:
                end_time = datetime.now(timezone.utc)
                start_time = end_time - timedelta(days=7)
                time_range = (start_time, end_time)
            
            dashboard = {
                "period": {
                    "start": time_range[0].isoformat(),
                    "end": time_range[1].isoformat()
                },
                "feedback": self._get_feedback_dashboard_data(time_range),
                "metrics": self._get_metrics_dashboard_data(time_range),
                "experiments": self._get_experiments_dashboard_data(),
                "monitoring": self._get_monitoring_dashboard_data(time_range),
                "insights": self._generate_dashboard_insights(time_range)
            }
            
            self.component_logger.info(
                "Comprehensive dashboard generated",
                time_range=time_range
            )
            
            return dashboard
            
        except Exception as e:
            self.component_logger.error(
                "Error generating comprehensive dashboard",
                error=str(e)
            )
            raise
    
    def export_data(
        self,
        data_type: str,
        format: str = "json",
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> str:
        """Export data in specified format"""
        try:
            if data_type == "feedback":
                data = self.feedback_collector.export_feedback(format, None, time_range)
            elif data_type == "metrics":
                data = self.metrics_tracker.export_metrics(format, time_range)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
            
            self.component_logger.info(
                "Data exported",
                data_type=data_type,
                format=format,
                time_range=time_range
            )
            
            return data
            
        except Exception as e:
            self.component_logger.error(
                "Error exporting data",
                data_type=data_type,
                format=format,
                error=str(e)
            )
            raise
    
    def shutdown(self):
        """Shutdown Phase 6 integration and cleanup resources"""
        try:
            self._background_tasks_enabled = False
            
            # Shutdown monitoring
            self.monitoring.shutdown()
            
            self.component_logger.info("Phase 6 Integration shutdown completed")
            
        except Exception as e:
            self.component_logger.error(
                "Error during Phase 6 shutdown",
                error=str(e)
            )
    
    # Private helper methods
    def _collect_user_feedback(
        self,
        user_id: str,
        session_id: str,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_interactions: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[UserFeedback]:
        """Collect user feedback from interactions"""
        return self.feedback_collector.collect_recommendation_feedback(
            phase4_result, phase5_result, user_interactions
        )
    
    def _track_session_metrics(
        self,
        phase4_result: Phase4Result,
        phase5_result: Phase5Result,
        user_interactions: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[MetricType, MetricValue]:
        """Track metrics for the session"""
        # Convert interactions to feedback objects
        feedback_list = []
        for interaction in user_interactions:
            # Create minimal feedback objects for metrics calculation
            pass  # Simplified for this example
        
        return self.metrics_tracker.track_recommendation_metrics(
            phase4_result, phase5_result, feedback_list, context
        )
    
    def _handle_prompt_testing(
        self,
        user_id: str,
        session_id: str,
        phase4_result: Phase4Result,
        user_interactions: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle A/B testing for prompts"""
        try:
            # Get appropriate prompt for user
            prompt_variables = {
                "user_preferences": context.get("preferences", {}),
                "location": context.get("location", ""),
                "budget": context.get("budget", ""),
                "cuisine": context.get("cuisine", "")
            }
            
            rendered_prompt, template_id = self.prompt_manager.get_prompt_for_user(
                PromptType.RANKING_PROMPT, user_id, prompt_variables
            )
            
            return {
                "experiment_id": None,  # Would be populated if user is in experiment
                "template_id": template_id,
                "prompt": rendered_prompt
            }
            
        except Exception as e:
            self.component_logger.warning(
                "Error handling prompt testing",
                error=str(e)
            )
            return {}
    
    def _perform_monitoring_checks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform monitoring and health checks"""
        try:
            # Get system health
            health_status = self.monitoring.system_monitor.get_system_health()
            
            # Get active alerts
            active_alerts = self.monitoring.system_monitor.get_active_alerts()
            
            return {
                "health": health_status,
                "alerts": [alert.name for alert in active_alerts]
            }
            
        except Exception as e:
            self.component_logger.warning(
                "Error performing monitoring checks",
                error=str(e)
            )
            return {"health": {}, "alerts": []}
    
    def _start_background_tasks(self):
        """Start background processing tasks"""
        self._background_tasks_enabled = True
        
        # Start background thread for periodic tasks
        import threading
        
        def background_worker():
            while self._background_tasks_enabled:
                try:
                    self._perform_background_tasks()
                    time.sleep(3600)  # Run every hour
                except Exception as e:
                    self.component_logger.error(
                        "Error in background worker",
                        error=str(e)
                    )
                    time.sleep(300)  # Wait 5 minutes on error
        
        background_thread = threading.Thread(target=background_worker, daemon=True)
        background_thread.start()
    
    def _perform_background_tasks(self):
        """Perform periodic background tasks"""
        current_time = datetime.now(timezone.utc)
        
        # Auto-aggregate feedback
        if self.config.auto_aggregate_feedback:
            last_feedback_agg = self._last_aggregation_time.get("feedback")
            if (not last_feedback_agg or 
                (current_time - last_feedback_agg).total_seconds() >= 
                self.config.feedback_aggregation_interval_hours * 3600):
                
                self.feedback_collector.aggregate_feedback()
                self._last_aggregation_time["feedback"] = current_time
        
        # Generate performance reports
        last_report = self._last_report_time.get("performance")
        if (not last_report or 
            (current_time - last_report).total_seconds() >= 
            self.config.performance_report_interval_hours * 3600):
            
            self.metrics_tracker.generate_performance_report()
            self._last_report_time["performance"] = current_time
    
    def _get_feedback_dashboard_data(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Get feedback data for dashboard"""
        insights = self.feedback_collector.generate_insights(time_range)
        stats = self.feedback_collector.get_feedback_statistics()
        
        return {
            "total_feedback": insights.total_feedback,
            "feedback_rate": insights.feedback_rate,
            "average_rating": insights.average_rating,
            "top_performing": insights.top_performing_restaurants[:5],
            "underperforming": insights.underperforming_restaurants[:5],
            "common_issues": insights.common_issues,
            "statistics": stats
        }
    
    def _get_metrics_dashboard_data(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Get metrics data for dashboard"""
        performance = self.metrics_tracker.generate_performance_report(time_range)
        
        return {
            "total_recommendations": performance.total_recommendations,
            "total_users": performance.total_users,
            "average_satisfaction": performance.average_satisfaction,
            "average_response_time": performance.average_response_time,
            "precision_at_5": performance.precision_at_5,
            "recall_at_5": performance.recall_at_5,
            "click_through_rate": performance.click_through_rate,
            "conversion_rate": performance.conversion_rate,
            "error_rate": performance.error_rate,
            "system_health_score": performance.system_health_score
        }
    
    def _get_experiments_dashboard_data(self) -> Dict[str, Any]:
        """Get experiments data for dashboard"""
        experiments = self.prompt_manager.experiments
        results = self.prompt_manager.experiment_results
        
        active_experiments = [exp for exp in experiments.values() if exp.is_active()]
        completed_experiments = [exp for exp in experiments.values() if exp.status == ExperimentStatus.COMPLETED]
        
        return {
            "total_experiments": len(experiments),
            "active_experiments": len(active_experiments),
            "completed_experiments": len(completed_experiments),
            "recent_results": [
                {
                    "experiment_id": result.experiment_id,
                    "winner": result.winner,
                    "statistical_significance": result.statistical_significance,
                    "sample_size": result.sample_size
                }
                for result in results.values()
            ][:10]
        }
    
    def _get_monitoring_dashboard_data(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Get monitoring data for dashboard"""
        report = self.monitoring.system_monitor.generate_monitoring_report(time_range)
        health = self.monitoring.system_monitor.get_system_health()
        
        return {
            "system_health": health,
            "active_alerts": len(self.monitoring.system_monitor.get_active_alerts()),
            "metrics_summary": report.get("metrics_summary", {}),
            "alerts_summary": report.get("alerts_summary", {}),
            "recommendations": report.get("recommendations", [])
        }
    
    def _generate_dashboard_insights(self, time_range: Tuple[datetime, datetime]) -> List[str]:
        """Generate insights for dashboard"""
        insights = []
        
        try:
            # Feedback insights
            feedback_insights = self.feedback_collector.generate_insights(time_range)
            if feedback_insights.average_rating < 3.5:
                insights.append("User satisfaction is below target - consider improving recommendation quality")
            
            # Performance insights
            performance = self.metrics_tracker.generate_performance_report(time_range)
            if performance.error_rate > 0.1:
                insights.append("High error rate detected - investigate system issues")
            
            if performance.average_response_time > 2.0:
                insights.append("Response times are slow - consider optimization")
            
            # Monitoring insights
            health = self.monitoring.system_monitor.get_system_health()
            if health["active_alerts"] > 0:
                insights.append(f"{health['active_alerts']} active alerts require attention")
            
            # Experiment insights
            if len(self.prompt_manager.experiment_results) > 0:
                insights.append("A/B testing experiments are providing valuable insights")
            
        except Exception as e:
            self.component_logger.warning(
                "Error generating dashboard insights",
                error=str(e)
            )
        
        return insights[:10]  # Return top 10 insights


# Factory function for easy instantiation
def create_phase6_integration(config: Optional[Phase6Config] = None) -> Phase6Integration:
    """Create and return a Phase6Integration instance"""
    return Phase6Integration(config)
