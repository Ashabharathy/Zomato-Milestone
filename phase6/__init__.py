"""
Phase 6: Feedback, Evaluation, and Improvement Loop
Complete feedback, evaluation, and improvement system for the AI-Powered Restaurant Recommendation System.
"""

from .phase6_integration import (
    Phase6Integration,
    Phase6Config,
    Phase6Result,
    create_phase6_integration
)

from .feedback_collector import (
    FeedbackCollector,
    UserFeedback,
    FeedbackType,
    FeedbackSource,
    FeedbackInsights,
    FeedbackAggregation
)

from .metrics_tracker import (
    MetricsTracker,
    MetricType,
    MetricValue,
    SystemPerformance,
    MetricAggregation,
    TimeGranularity
)

from .prompt_version_manager import (
    PromptVersionManager,
    PromptTemplate,
    Experiment,
    ExperimentResult,
    PromptType,
    ExperimentStatus,
    VariantType
)

from .monitoring_logging import (
    MonitoringAndLogging,
    MonitoringLogger,
    LogLevel,
    AlertSeverity,
    MetricCategory,
    SystemMetric,
    Alert
)

__version__ = "1.0.0"
__author__ = "AI Restaurant Recommendation Team"
__description__ = "Phase 6: Feedback, Evaluation, and Improvement Loop"

# Main exports
__all__ = [
    # Main integration
    "Phase6Integration",
    "Phase6Config", 
    "Phase6Result",
    "create_phase6_integration",
    
    # Feedback collection
    "FeedbackCollector",
    "UserFeedback",
    "FeedbackType",
    "FeedbackSource",
    "FeedbackInsights",
    "FeedbackAggregation",
    
    # Metrics tracking
    "MetricsTracker",
    "MetricType",
    "MetricValue",
    "SystemPerformance",
    "MetricAggregation",
    "TimeGranularity",
    
    # A/B testing
    "PromptVersionManager",
    "PromptTemplate",
    "Experiment",
    "ExperimentResult",
    "PromptType",
    "ExperimentStatus",
    "VariantType",
    
    # Monitoring and logging
    "MonitoringAndLogging",
    "MonitoringLogger",
    "LogLevel",
    "AlertSeverity",
    "MetricCategory",
    "SystemMetric",
    "Alert"
]

# Convenience function for quick setup
def create_feedback_loop(config=None):
    """
    Create a complete feedback, evaluation, and improvement loop
    
    Args:
        config: Optional Phase6Config for customization
        
    Returns:
        Configured Phase6Integration instance
    """
    return create_phase6_integration(config)

# Version info
def get_version():
    """Get Phase 6 version information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "components": [
            "Feedback Collection",
            "Metrics Tracking", 
            "A/B Testing",
            "Monitoring & Logging",
            "Integration Layer"
        ]
    }
