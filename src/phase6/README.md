# Phase 6: Feedback, Evaluation, and Improvement Loop

## Overview

Phase 6 implements the feedback, evaluation, and improvement loop for the AI-Powered Restaurant Recommendation System. This phase is responsible for collecting user feedback, tracking performance metrics, conducting A/B testing for prompt optimization, and providing comprehensive monitoring and logging capabilities.

## Architecture

### Core Components

1. **Feedback Collector** (`feedback_collector.py`)
   - Collects and processes user feedback from multiple sources
   - Aggregates feedback by restaurant and generates insights
   - Supports various feedback types (like, dislike, bookmark, visit, etc.)
   - Provides feedback analytics and improvement suggestions

2. **Metrics Tracker** (`metrics_tracker.py`)
   - Tracks comprehensive performance metrics for the recommendation system
   - Calculates precision@k, recall@k, satisfaction scores, and other key metrics
   - Aggregates metrics over time periods and identifies trends
   - Generates performance reports and system health assessments

3. **Prompt/Version Manager** (`prompt_version_manager.py`)
   - Manages prompt templates and versions for A/B testing
   - Creates and manages experiments with statistical analysis
   - Handles traffic splitting and user assignment
   - Provides prompt performance insights and recommendations

4. **Monitoring and Logging Layer** (`monitoring_logging.py`)
   - Provides structured logging with monitoring capabilities
   - Tracks system metrics (CPU, memory, disk usage)
   - Implements health checks and alerting system
   - Generates comprehensive monitoring reports

5. **Integration Module** (`phase6_integration.py`)
   - Main integration point for all Phase 6 components
   - Orchestrates feedback collection, metrics tracking, and monitoring
   - Provides unified API for the feedback loop
   - Handles background processing and periodic tasks

## Key Features

### Feedback Collection
- **Multi-source feedback**: UI buttons, surveys, interviews, automatic tracking
- **Rich feedback data**: Ratings, comments, reasons, context information
- **Real-time aggregation**: Automatic feedback aggregation and analysis
- **Insight generation**: Identifies common issues and improvement opportunities

### Performance Metrics
- **Recommendation quality**: Precision@k, recall@k, diversity, novelty
- **User satisfaction**: Satisfaction scores, engagement metrics
- **System performance**: Response times, error rates, token efficiency
- **Business metrics**: Click-through rates, conversion rates

### A/B Testing
- **Prompt optimization**: Test different prompt versions and templates
- **Statistical analysis**: Proper statistical testing with confidence intervals
- **Traffic management**: Automatic user assignment and traffic splitting
- **Performance tracking**: Track prompt performance over time

### Monitoring & Alerting
- **System health**: CPU, memory, disk usage monitoring
- **Application metrics**: Response times, error rates, throughput
- **Health checks**: Database, API, and service health monitoring
- **Alert management**: Configurable alerts with severity levels

## Installation

### Dependencies

Install the required dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

### Key Dependencies

- **psutil**: System monitoring and metrics collection
- **scipy/numpy**: Statistical analysis for metrics and A/B testing
- **structlog**: Structured logging with monitoring capabilities
- **prometheus-client**: Metrics export for external monitoring systems

## Usage

### Basic Usage

```python
from phase6.phase6_integration import Phase6Integration, Phase6Config

# Create configuration
config = Phase6Config(
    enable_feedback_collection=True,
    enable_metrics_tracking=True,
    enable_prompt_testing=True,
    enable_monitoring=True
)

# Initialize Phase 6
phase6 = Phase6Integration(config)

# Process a recommendation session
result = phase6.process_recommendation_session(
    user_id="user123",
    session_id="session456",
    phase4_result=phase4_result,
    phase5_result=phase5_result,
    user_interactions=user_interactions,
    context={"preferences": {...}}
)

# Get insights
feedback_insights = phase6.get_feedback_insights()
performance_metrics = phase6.get_performance_metrics()
system_health = phase6.get_system_health()
```

### Feedback Collection

```python
# Collect individual feedback
feedback = phase6.collect_feedback(
    user_id="user123",
    session_id="session456",
    recommendation_id="rec789",
    restaurant_id="Restaurant Name",
    feedback_type=FeedbackType.LIKE,
    rating=5,
    comment="Great experience!",
    reasons=["Good food", "Nice ambiance"]
)

# Get feedback insights
insights = phase6.get_feedback_insights()
print(f"Total feedback: {insights.total_feedback}")
print(f"Average rating: {insights.average_rating}")
print(f"Common issues: {insights.common_issues}")
```

### Metrics Tracking

```python
# Get specific metrics
precision_metrics = phase6.get_performance_metrics(
    MetricType.PRECISION_AT_K,
    granularity=TimeGranularity.DAILY
)

# Get all metrics
all_metrics = phase6.get_performance_metrics(
    granularity=TimeGranularity.HOURLY
)

# Generate performance report
report = phase6.metrics_tracker.generate_performance_report()
print(f"System health score: {report.system_health_score}")
```

### A/B Testing

```python
# Create prompt templates
control_template = phase6.prompt_manager.create_prompt_template(
    name="Standard Prompt",
    prompt_type=PromptType.RANKING_PROMPT,
    template="Rank these restaurants: {restaurants}"
)

treatment_template = phase6.prompt_manager.create_prompt_template(
    name="Enhanced Prompt",
    prompt_type=PromptType.RANKING_PROMPT,
    template="Rank these restaurants based on {preferences}: {restaurants}"
)

# Create experiment
experiment = phase6.create_a_b_experiment(
    name="Prompt Comparison",
    prompt_type=PromptType.RANKING_PROMPT,
    control_template_id=control_template.id,
    treatment_template_ids=[treatment_template.id],
    sample_size=1000
)

# Start experiment
phase6.start_experiment(experiment.id)

# Get results
results = phase6.get_experiment_results(experiment.id)
print(f"Winner: {results.winner}")
print(f"Statistical significance: {results.statistical_significance}")
```

### Monitoring

```python
# Get system health
health = phase6.get_system_health()
print(f"Overall status: {health['overall_status']}")
print(f"Active alerts: {health['active_alerts']}")

# Get monitoring report
report = phase6.get_monitoring_report()
print(f"Recommendations: {report['recommendations']}")

# Get comprehensive dashboard
dashboard = phase6.get_comprehensive_dashboard()
print(f"Feedback metrics: {dashboard['feedback']}")
print(f"Performance metrics: {dashboard['metrics']}")
print(f"Experiment results: {dashboard['experiments']}")
```

## Configuration

### Phase6Config Options

```python
@dataclass
class Phase6Config:
    # Enable/disable components
    enable_feedback_collection: bool = True
    enable_metrics_tracking: bool = True
    enable_prompt_testing: bool = True
    enable_monitoring: bool = True
    
    # Feedback settings
    feedback_retention_days: int = 90
    auto_aggregate_feedback: bool = True
    feedback_aggregation_interval_hours: int = 24
    
    # Metrics settings
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
```

## API Reference

### FeedbackCollector

#### Methods

- `collect_feedback()`: Collect individual user feedback
- `collect_batch_feedback()`: Collect multiple feedback items
- `collect_recommendation_feedback()`: Collect feedback from session interactions
- `aggregate_feedback()`: Aggregate feedback by restaurant
- `generate_insights()`: Generate feedback insights and analytics
- `export_feedback()`: Export feedback data in various formats

### MetricsTracker

#### Methods

- `track_recommendation_metrics()`: Track metrics for recommendation session
- `track_system_metrics()`: Track system-level metrics
- `get_metric_history()`: Get historical metric values
- `aggregate_metrics()`: Aggregate metrics over time period
- `generate_performance_report()`: Generate comprehensive performance report

### PromptVersionManager

#### Methods

- `create_prompt_template()`: Create new prompt template
- `update_prompt_template()`: Update existing template
- `create_experiment()`: Create A/B testing experiment
- `start_experiment()`: Start experiment
- `stop_experiment()`: Stop experiment and analyze results
- `get_prompt_for_user()`: Get appropriate prompt for user

### SystemMonitor

#### Methods

- `record_metric()`: Record system metric
- `create_alert()`: Create alert definition
- `perform_health_check()`: Perform component health check
- `get_system_health()`: Get overall system health
- `generate_monitoring_report()`: Generate monitoring report

## Data Models

### UserFeedback

```python
@dataclass
class UserFeedback:
    user_id: str
    session_id: str
    recommendation_id: str
    restaurant_id: str
    feedback_type: FeedbackType
    feedback_source: FeedbackSource
    rating: Optional[int] = None
    helpfulness: Optional[int] = None
    comment: Optional[str] = None
    reasons: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    processed: bool = False
```

### MetricValue

```python
@dataclass
class MetricValue:
    metric_type: MetricType
    value: float
    timestamp: datetime
    context: Dict[str, Any]
    granularity: TimeGranularity
    sample_size: int
    confidence_interval: Optional[Tuple[float, float]] = None
```

### Experiment

```python
@dataclass
class Experiment:
    id: str
    name: str
    description: str
    prompt_type: PromptType
    control_template_id: str
    treatment_template_ids: List[str]
    traffic_split: Dict[str, float]
    status: ExperimentStatus
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    sample_size: int
    confidence_level: float
    success_criteria: Dict[str, Any]
```

## Integration with Other Phases

Phase 6 integrates with all previous phases to create a complete feedback loop:

- **Phase 1-3**: Data ingestion and processing metrics
- **Phase 4**: Recommendation quality metrics and feedback collection
- **Phase 5**: User interaction tracking and presentation metrics
- **Phase 6**: Comprehensive analysis, monitoring, and improvement

## Example Usage

See `example_usage.py` for a comprehensive demonstration of all Phase 6 functionality:

```bash
python example_usage.py
```

This script demonstrates:
- Full session processing
- Feedback collection and analysis
- Metrics tracking and evaluation
- A/B testing setup and execution
- System monitoring and health checks
- Comprehensive dashboard generation
- Data export functionality

## Monitoring and Alerting

### System Metrics

- **CPU Usage**: Monitors system CPU utilization
- **Memory Usage**: Tracks memory consumption
- **Disk Usage**: Monitors disk space usage
- **Process Metrics**: Tracks application-specific metrics

### Health Checks

- **Database**: Connectivity and response time
- **LLM API**: API availability and response time
- **Redis**: Cache system health
- **Disk Space**: Storage availability

### Alerts

- **Threshold-based**: Configurable thresholds for metrics
- **Severity levels**: Low, Medium, High, Critical
- **Auto-resolution**: Automatic alert resolution
- **Callback support**: Custom alert notification handlers

## Data Export

Phase 6 supports data export in multiple formats:

```python
# Export feedback data
feedback_json = phase6.export_data("feedback", "json")
feedback_csv = phase6.export_data("feedback", "csv")

# Export metrics data
metrics_json = phase6.export_data("metrics", "json")
```

## Performance Considerations

### Memory Management

- **Circular buffers**: Limited storage for logs and metrics
- **Data retention**: Configurable retention periods
- **Background cleanup**: Automatic cleanup of old data

### Processing Efficiency

- **Async operations**: Non-blocking metric collection
- **Batch processing**: Efficient batch operations
- **Caching**: Intelligent caching for frequently accessed data

### Scalability

- **Horizontal scaling**: Support for multiple instances
- **Distributed metrics**: Metrics aggregation across instances
- **Load balancing**: Efficient load distribution

## Troubleshooting

### Common Issues

1. **High memory usage**: Reduce retention periods or increase cleanup frequency
2. **Missing metrics**: Check metric configuration and data flow
3. **Alert fatigue**: Adjust alert thresholds and severity levels
4. **Slow performance**: Optimize aggregation intervals and background tasks

### Debug Mode

Enable debug logging for troubleshooting:

```python
config = Phase6Config(
    log_level=LogLevel.DEBUG,
    structured_logging=True
)
```

### Health Monitoring

Regular health checks can identify issues early:

```python
health = phase6.get_system_health()
if health['overall_status'] != 'healthy':
    # Handle unhealthy state
    pass
```

## Best Practices

### Feedback Collection

1. **Collect diverse feedback**: Multiple sources and types
2. **Provide context**: Rich context information with feedback
3. **Real-time processing**: Process feedback as it arrives
4. **Regular analysis**: Periodic insight generation

### Metrics Tracking

1. **Track relevant metrics**: Focus on business-critical metrics
2. **Proper aggregation**: Use appropriate time granularities
3. **Trend analysis**: Monitor trends over time
4. **Alert thresholds**: Set appropriate alert thresholds

### A/B Testing

1. **Statistical validity**: Ensure proper sample sizes
2. **Clear hypotheses**: Define success criteria clearly
3. **Proper controls**: Use appropriate control groups
4. **Continuous monitoring**: Monitor experiments continuously

### Monitoring

1. **Comprehensive coverage**: Monitor all critical components
2. **Actionable alerts**: Create actionable alert definitions
3. **Regular health checks**: Perform periodic health checks
4. **Performance optimization**: Continuously optimize performance

## Future Enhancements

### Planned Features

1. **Machine Learning**: ML-based improvement suggestions
2. **Advanced Analytics**: More sophisticated analytics capabilities
3. **Real-time Dashboard**: Real-time dashboard updates
4. **Integration Hub**: Centralized integration with external systems

### Extensions

1. **Multi-tenant Support**: Support for multiple tenants
2. **Advanced A/B Testing**: More sophisticated testing frameworks
3. **Predictive Analytics**: Predictive capabilities for system performance
4. **Custom Metrics**: Support for custom metric definitions

## Contributing

When contributing to Phase 6:

1. **Follow coding standards**: Maintain consistent code style
2. **Add tests**: Include comprehensive tests for new features
3. **Update documentation**: Keep documentation up-to-date
4. **Performance testing**: Test performance impact of changes

## License

This phase is part of the AI-Powered Restaurant Recommendation System project and follows the same licensing terms.

## Support

For support and questions regarding Phase 6:

1. Check the documentation and examples
2. Review the troubleshooting section
3. Enable debug logging for detailed information
4. Contact the development team for complex issues
