"""
Example Usage Script for Phase 6: Feedback, Evaluation, and Improvement Loop
Demonstrates all Phase 6 functionality including feedback collection, metrics tracking,
A/B testing, and monitoring capabilities.
"""

import os
import sys
import time
import uuid
import random
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import Phase 6 components
from .phase6_integration import (
    Phase6Integration, Phase6Config, create_phase6_integration
)
from .feedback_collector import (
    FeedbackType, FeedbackSource
)
from .metrics_tracker import (
    MetricType, TimeGranularity
)
from .prompt_version_manager import (
    PromptType, ExperimentStatus
)
from .monitoring_logging import (
    LogLevel, AlertSeverity, MetricCategory
)

# Import from previous phases for testing
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result


def create_sample_phase4_result() -> Phase4Result:
    """Create a sample Phase4Result for testing"""
    return Phase4Result(
        success=True,
        recommendations=[
            {
                "rank": 1,
                "restaurant_name": "The Hole in the Wall",
                "score": 0.92,
                "explanation": "Great cafe with cozy atmosphere and excellent coffee",
                "highlights": ["Highly rated", "Pet friendly", "Cozy atmosphere"],
                "considerations": ["Moderately expensive", "Limited seating"],
                "cuisine": "Continental",
                "rating": 4.6,
                "price_range": "$$",
                "avg_cost_for_two": 800
            },
            {
                "rank": 2,
                "restaurant_name": "Barbeque Nation",
                "score": 0.88,
                "explanation": "Excellent BBQ with great ambiance and service",
                "highlights": ["Great value", "Family friendly", "Wide variety"],
                "considerations": ["Can be crowded", "Long wait times"],
                "cuisine": "Barbecue",
                "rating": 4.4,
                "price_range": "$$$",
                "avg_cost_for_two": 1200
            },
            {
                "rank": 3,
                "restaurant_name": "Truffles & Co.",
                "score": 0.85,
                "explanation": "Fine dining experience with exceptional service",
                "highlights": ["Fine dining", "Excellent service", "Wine selection"],
                "considerations": ["Expensive", "Formal dress code"],
                "cuisine": "Continental",
                "rating": 4.7,
                "price_range": "$$$$",
                "avg_cost_for_two": 2000
            }
        ],
        summary="Top 3 restaurants matching your preferences in Indiranagar",
        alternatives="Consider exploring other areas like Koramangala for more options",
        metadata={
            "processing_time": 1.23,
            "model_used": "llama-3.3-70b-versatile",
            "tokens_used": 1450,
            "request_id": str(uuid.uuid4())
        }
    )


def create_sample_phase5_result() -> Phase5Result:
    """Create a sample Phase5Result for testing"""
    return Phase5Result(
        success=True,
        formatted_result={
            "format_type": "card",
            "recommendations": [
                {
                    "rank": 1,
                    "restaurant_name": "The Hole in the Wall",
                    "score": 0.92,
                    "explanation": "Great cafe with cozy atmosphere",
                    "cuisine": "Continental",
                    "rating": 4.6,
                    "price_range": "$$"
                }
            ]
        },
        rendered_output={
            "content": "<html>...</html>",
            "format_type": "html",
            "content_type": "text/html"
        },
        summary_result={
            "summary_type": "quick_comparison",
            "title": "Quick Comparison",
            "insights": ["Average rating: 4.6 stars"]
        },
        processing_time=0.45
    )


def create_sample_user_interactions() -> List[Dict[str, Any]]:
    """Create sample user interaction data"""
    return [
        {
            "type": "like",
            "restaurant_id": "The Hole in the Wall",
            "rating": 5,
            "helpfulness": 4,
            "comment": "Excellent coffee and atmosphere!",
            "reasons": ["Good coffee", "Nice ambiance", "Friendly staff"],
            "duration": 45.2,
            "scroll_depth": 0.8,
            "device_type": "mobile",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": str(uuid.uuid4()),
            "user_id": "user123"
        },
        {
            "type": "dislike",
            "restaurant_id": "Barbeque Nation",
            "rating": 2,
            "helpfulness": 3,
            "comment": "Too crowded and service was slow",
            "reasons": ["Crowded", "Slow service", "Long wait"],
            "duration": 12.5,
            "scroll_depth": 0.3,
            "device_type": "mobile",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": str(uuid.uuid4()),
            "user_id": "user123"
        },
        {
            "type": "bookmark",
            "restaurant_id": "Truffles & Co.",
            "rating": 4,
            "helpfulness": 5,
            "comment": "Saved for special occasion",
            "reasons": ["Fine dining", "Special occasion"],
            "duration": 28.7,
            "scroll_depth": 0.9,
            "device_type": "desktop",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": str(uuid.uuid4()),
            "user_id": "user123"
        }
    ]


def demonstrate_feedback_collection(phase6: Phase6Integration):
    """Demonstrate feedback collection functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING FEEDBACK COLLECTION")
    print("="*60)
    
    # Collect individual feedback
    feedback = phase6.collect_feedback(
        user_id="user123",
        session_id="session456",
        recommendation_id="rec789",
        restaurant_id="The Hole in the Wall",
        feedback_type=FeedbackType.LIKE,
        feedback_source=FeedbackSource.UI_BUTTON,
        rating=5,
        helpfulness=4,
        comment="Great experience!",
        reasons=["Good food", "Nice ambiance", "Friendly staff"]
    )
    
    print(f"Collected feedback: {feedback.feedback_type.value} for {feedback.restaurant_id}")
    print(f"Rating: {feedback.rating}, Helpfulness: {feedback.helpfulness}")
    print(f"Comment: {feedback.comment}")
    
    # Get feedback insights
    insights = phase6.get_feedback_insights()
    print(f"\nFeedback Insights:")
    print(f"Total feedback: {insights.total_feedback}")
    print(f"Feedback rate: {insights.feedback_rate:.2%}")
    print(f"Average rating: {insights.average_rating:.2f}")
    print(f"Top performing restaurants: {len(insights.top_performing_restaurants)}")
    print(f"Common issues: {insights.common_issues}")
    print(f"Improvement suggestions: {insights.improvement_suggestions}")


def demonstrate_metrics_tracking(phase6: Phase6Integration):
    """Demonstrate metrics tracking functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING METRICS TRACKING")
    print("="*60)
    
    # Get performance metrics
    try:
        precision_metrics = phase6.get_performance_metrics(
            MetricType.PRECISION_AT_K,
            granularity=TimeGranularity.DAILY
        )
        print(f"Precision@K Metrics:")
        print(f"  Mean: {precision_metrics.mean:.4f}")
        print(f"  Median: {precision_metrics.median:.4f}")
        print(f"  Trend: {precision_metrics.trend}")
        print(f"  Sample count: {precision_metrics.sample_count}")
    except Exception as e:
        print(f"Precision metrics not available: {str(e)}")
    
    # Get all metrics
    all_metrics = phase6.get_performance_metrics(granularity=TimeGranularity.DAILY)
    print(f"\nAvailable Metrics: {len(all_metrics)}")
    for metric_name, metric_data in all_metrics.items():
        print(f"  {metric_name}: mean={metric_data.mean:.4f}, samples={metric_data.sample_count}")


def demonstrate_prompt_testing(phase6: Phase6Integration):
    """Demonstrate A/B testing functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING A/B TESTING")
    print("="*60)
    
    # Create prompt templates
    try:
        # Create control template
        control_template = phase6.prompt_manager.create_prompt_template(
            name="Standard Ranking Prompt",
            prompt_type=PromptType.RANKING_PROMPT,
            template="Please rank these restaurants based on user preferences: {preferences}",
            description="Standard prompt for restaurant ranking",
            variables=["preferences"]
        )
        
        # Create treatment template
        treatment_template = phase6.prompt_manager.create_prompt_template(
            name="Enhanced Ranking Prompt",
            prompt_type=PromptType.RANKING_PROMPT,
            template="Please rank these restaurants based on user preferences {preferences}, considering factors like location, price, and cuisine match.",
            description="Enhanced prompt with additional context",
            variables=["preferences"]
        )
        
        print(f"Created templates: {control_template.name} and {treatment_template.name}")
        
        # Create experiment
        experiment = phase6.create_a_b_experiment(
            name="Ranking Prompt Comparison",
            description="Test standard vs enhanced ranking prompts",
            prompt_type=PromptType.RANKING_PROMPT,
            control_template_id=control_template.id,
            treatment_template_ids=[treatment_template.id],
            sample_size=100,
            confidence_level=0.95
        )
        
        print(f"Created experiment: {experiment.name}")
        print(f"Control template: {experiment.control_template_id}")
        print(f"Treatment templates: {experiment.treatment_template_ids}")
        print(f"Traffic split: {experiment.traffic_split}")
        
        # Start experiment
        started_experiment = phase6.start_experiment(experiment.id)
        print(f"Experiment status: {started_experiment.status.value}")
        
        # Get prompt for user
        prompt_variables = {"preferences": "Indiranagar, budget 1000, rating 4.0+"}
        rendered_prompt, template_id = phase6.prompt_manager.get_prompt_for_user(
            PromptType.RANKING_PROMPT, "user123", prompt_variables
        )
        
        print(f"Prompt for user123: {rendered_prompt[:100]}...")
        print(f"Template used: {template_id}")
        
    except Exception as e:
        print(f"Error in A/B testing demo: {str(e)}")


def demonstrate_monitoring(phase6: Phase6Integration):
    """Demonstrate monitoring functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING MONITORING")
    print("="*60)
    
    # Get system health
    health_status = phase6.get_system_health()
    print(f"System Health:")
    print(f"  Overall status: {health_status['overall_status']}")
    print(f"  Active alerts: {health_status['active_alerts']}")
    print(f"  Components checked: {len(health_status['components'])}")
    
    for component, status in health_status['components'].items():
        print(f"    {component}: {status['status']} ({status['message']})")
    
    # Get monitoring report
    try:
        report = phase6.get_monitoring_report()
        print(f"\nMonitoring Report:")
        print(f"  Period: {report['period']['duration_hours']:.1f} hours")
        print(f"  Metrics categories: {len(report['metrics_summary'])}")
        print(f"  Recommendations: {len(report['recommendations'])}")
        
        for category, metrics in report['metrics_summary'].items():
            print(f"    {category}: avg={metrics['average']:.2f}, trend={metrics['trend']}")
        
        if report['recommendations']:
            print(f"  Recommendations:")
            for rec in report['recommendations'][:3]:
                print(f"    - {rec}")
        
    except Exception as e:
        print(f"Error generating monitoring report: {str(e)}")


def demonstrate_comprehensive_dashboard(phase6: Phase6Integration):
    """Demonstrate comprehensive dashboard functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING COMPREHENSIVE DASHBOARD")
    print("="*60)
    
    try:
        # Get comprehensive dashboard data
        dashboard = phase6.get_comprehensive_dashboard()
        
        print(f"Dashboard Overview:")
        print(f"  Period: {dashboard['period']['start']} to {dashboard['period']['end']}")
        
        # Feedback section
        feedback_data = dashboard['feedback']
        print(f"\nFeedback Metrics:")
        print(f"  Total feedback: {feedback_data['total_feedback']}")
        print(f"  Feedback rate: {feedback_data['feedback_rate']:.2%}")
        print(f"  Average rating: {feedback_data['average_rating']:.2f}")
        
        # Metrics section
        metrics_data = dashboard['metrics']
        print(f"\nPerformance Metrics:")
        print(f"  Total recommendations: {metrics_data['total_recommendations']}")
        print(f"  Total users: {metrics_data['total_users']}")
        print(f"  Average satisfaction: {metrics_data['average_satisfaction']:.2f}")
        print(f"  Average response time: {metrics_data['average_response_time']:.2f}s")
        print(f"  Precision@5: {metrics_data['precision_at_5']:.4f}")
        print(f"  Click-through rate: {metrics_data['click_through_rate']:.2%}")
        print(f"  Conversion rate: {metrics_data['conversion_rate']:.2%}")
        print(f"  System health score: {metrics_data['system_health_score']:.2f}")
        
        # Experiments section
        experiments_data = dashboard['experiments']
        print(f"\nA/B Testing:")
        print(f"  Total experiments: {experiments_data['total_experiments']}")
        print(f"  Active experiments: {experiments_data['active_experiments']}")
        print(f"  Completed experiments: {experiments_data['completed_experiments']}")
        
        # Monitoring section
        monitoring_data = dashboard['monitoring']
        print(f"\nSystem Monitoring:")
        print(f"  System health: {monitoring_data['system_health']['overall_status']}")
        print(f"  Active alerts: {monitoring_data['active_alerts']}")
        print(f"  Metrics categories: {len(monitoring_data['metrics_summary'])}")
        
        # Insights
        insights = dashboard['insights']
        if insights:
            print(f"\nKey Insights:")
            for insight in insights[:5]:
                print(f"  - {insight}")
        
    except Exception as e:
        print(f"Error generating dashboard: {str(e)}")


def demonstrate_data_export(phase6: Phase6Integration):
    """Demonstrate data export functionality"""
    print("\n" + "="*60)
    print("DEMONSTRATING DATA EXPORT")
    print("="*60)
    
    try:
        # Export feedback data
        feedback_json = phase6.export_data("feedback", "json")
        print(f"Feedback export (JSON): {len(feedback_json)} characters")
        
        # Export metrics data
        metrics_json = phase6.export_data("metrics", "json")
        print(f"Metrics export (JSON): {len(metrics_json)} characters")
        
        # Export as CSV
        feedback_csv = phase6.export_data("feedback", "csv")
        print(f"Feedback export (CSV): {len(feedback_csv)} characters")
        
        print("Data export completed successfully")
        
    except Exception as e:
        print(f"Error in data export: {str(e)}")


def demonstrate_full_session_processing(phase6: Phase6Integration):
    """Demonstrate complete session processing"""
    print("\n" + "="*60)
    print("DEMONSTRATING FULL SESSION PROCESSING")
    print("="*60)
    
    # Create sample data
    phase4_result = create_sample_phase4_result()
    phase5_result = create_sample_phase5_result()
    user_interactions = create_sample_user_interactions()
    
    context = {
        "preferences": {
            "location": "Indiranagar",
            "budget": 1000,
            "cuisine": "Continental",
            "min_rating": 4.0
        },
        "device_type": "mobile",
        "session_duration": 120.5
    }
    
    # Process the session
    result = phase6.process_recommendation_session(
        user_id="user123",
        session_id="session456",
        phase4_result=phase4_result,
        phase5_result=phase5_result,
        user_interactions=user_interactions,
        context=context
    )
    
    print(f"Session Processing Results:")
    print(f"  Success: {result.success}")
    print(f"  Processing time: {result.processing_time:.3f}s")
    print(f"  Feedback collected: {result.feedback_collected}")
    print(f"  Metrics tracked: {len(result.metrics_tracked)}")
    print(f"  Experiment participated: {result.experiment_participated}")
    print(f"  Template used: {result.template_used}")
    print(f"  Alerts triggered: {len(result.alerts_triggered)}")
    
    if result.feedback_insights:
        print(f"  Feedback insights available: {result.feedback_insights.total_feedback} total feedback")
    
    if result.metrics_tracked:
        print("  Metrics tracked:")
        for metric_name, metric_value in result.metrics_tracked.items():
            print(f"    {metric_name}: {metric_value:.4f}")
    
    if result.alerts_triggered:
        print(f"  Alerts triggered: {result.alerts_triggered}")
    
    if result.health_status:
        print(f"  Health status: {result.health_status.get('overall_status', 'unknown')}")


def main():
    """Main demonstration function"""
    print("Phase 6: Feedback, Evaluation, and Improvement Loop")
    print("=" * 60)
    print("This script demonstrates all Phase 6 functionality including:")
    print("- User feedback collection and analysis")
    print("- Performance metrics tracking and evaluation")
    print("- A/B testing for prompt optimization")
    print("- System monitoring and alerting")
    print("- Comprehensive dashboard and reporting")
    print("- Data export capabilities")
    print("- Full session processing integration")
    
    # Create Phase 6 configuration
    config = Phase6Config(
        enable_feedback_collection=True,
        enable_metrics_tracking=True,
        enable_prompt_testing=True,
        enable_monitoring=True,
        feedback_retention_days=30,
        metrics_retention_days=7,
        monitoring_interval_seconds=60,
        log_level=LogLevel.INFO
    )
    
    # Initialize Phase 6 integration
    print("\nInitializing Phase 6 Integration...")
    phase6 = create_phase6_integration(config)
    
    try:
        # Run demonstrations
        demonstrate_full_session_processing(phase6)
        demonstrate_feedback_collection(phase6)
        demonstrate_metrics_tracking(phase6)
        demonstrate_prompt_testing(phase6)
        demonstrate_monitoring(phase6)
        demonstrate_comprehensive_dashboard(phase6)
        demonstrate_data_export(phase6)
        
        print("\n" + "="*60)
        print("PHASE 6 DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("="*60)
        print("All Phase 6 components have been demonstrated:")
        print("1. Feedback collection and analysis")
        print("2. Metrics tracking and evaluation")
        print("3. A/B testing and prompt optimization")
        print("4. System monitoring and health checks")
        print("5. Comprehensive dashboard and insights")
        print("6. Data export functionality")
        print("7. Full session processing integration")
        
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\nShutting down Phase 6 Integration...")
        phase6.shutdown()
        print("Shutdown completed.")


if __name__ == "__main__":
    main()
