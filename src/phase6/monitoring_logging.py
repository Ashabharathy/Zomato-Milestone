"""
Monitoring and Logging Layer Module for Phase 6: Feedback, Evaluation, and Improvement Loop
Provides comprehensive monitoring, logging, and alerting capabilities.
"""

import json
import time
import logging
import traceback
import psutil
import threading
import uuid
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
import queue
import statistics
import math

# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result
from .feedback_collector import UserFeedback
from .metrics_tracker import MetricsTracker, MetricType


class LogLevel(Enum):
    """Log levels for monitoring"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MetricCategory(Enum):
    """Categories of metrics"""
    SYSTEM = "system"
    APPLICATION = "application"
    BUSINESS = "business"
    USER = "user"
    API = "api"
    DATABASE = "database"
    LLM = "llm"


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: LogLevel
    message: str
    context: Dict[str, Any]
    component: str
    user_id: Optional[str]
    session_id: Optional[str]
    request_id: Optional[str]
    duration_ms: Optional[float]
    error: Optional[str]
    stack_trace: Optional[str]
    
    def __post_init__(self):
        if isinstance(self.level, str):
            self.level = LogLevel(self.level)
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "context": self.context,
            "component": self.component,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "stack_trace": self.stack_trace
        }


@dataclass
class SystemMetric:
    """System performance metric"""
    name: str
    category: MetricCategory
    value: float
    unit: str
    timestamp: datetime
    tags: Dict[str, str]
    threshold: Optional[float]
    
    def __post_init__(self):
        if isinstance(self.category, str):
            self.category = MetricCategory(self.category)
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
    
    def is_alert_threshold_exceeded(self) -> bool:
        """Check if metric exceeds alert threshold"""
        if self.threshold is None:
            return False
        return self.value > self.threshold


@dataclass
class Alert:
    """System alert definition"""
    id: str
    name: str
    description: str
    severity: AlertSeverity
    condition: str  # Metric condition expression
    threshold: float
    duration_seconds: int
    is_active: bool
    triggered_at: Optional[datetime]
    resolved_at: Optional[datetime]
    count: int
    last_triggered: Optional[datetime]
    
    def __post_init__(self):
        if isinstance(self.severity, str):
            self.severity = AlertSeverity(self.severity)
        if isinstance(self.triggered_at, str):
            self.triggered_at = datetime.fromisoformat(self.triggered_at)
        if isinstance(self.resolved_at, str):
            self.resolved_at = datetime.fromisoformat(self.resolved_at)
        if isinstance(self.last_triggered, str):
            self.last_triggered = datetime.fromisoformat(self.last_triggered)


@dataclass
class HealthCheck:
    """Health check result"""
    component: str
    status: str  # healthy, unhealthy, degraded
    message: str
    response_time_ms: float
    timestamp: datetime
    details: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class MonitoringLogger:
    """Enhanced logging with structured monitoring capabilities"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.logger = logging.getLogger(component_name)
        self.log_storage: deque = deque(maxlen=10000)  # Store last 10k logs
        self.metrics_tracker = MetricsTracker()
        
    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        error: Optional[str] = None,
        include_stack_trace: bool = False
    ):
        """Log structured message"""
        try:
            # Create log entry
            stack_trace = traceback.format_exc() if include_stack_trace and error else None
            
            log_entry = LogEntry(
                timestamp=datetime.now(timezone.utc),
                level=level,
                message=message,
                context=context or {},
                component=self.component_name,
                user_id=user_id,
                session_id=session_id,
                request_id=request_id,
                duration_ms=duration_ms,
                error=error,
                stack_trace=stack_trace
            )
            
            # Store log entry
            self.log_storage.append(log_entry)
            
            # Log to standard logger
            log_method = getattr(self.logger, level.value)
            log_data = {
                "component": self.component_name,
                "user_id": user_id,
                "session_id": session_id,
                "request_id": request_id,
                "duration_ms": duration_ms,
                "context": context or {}
            }
            
            if error:
                log_data["error"] = error
            
            if stack_trace:
                log_data["stack_trace"] = stack_trace
            
            log_method(message, extra=log_data)
            
        except Exception as e:
            # Fallback logging
            self.logger.error(f"Error in structured logging: {str(e)}")
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, error: Optional[str] = None, **kwargs):
        """Log error message"""
        self.log(LogLevel.ERROR, message, error=error, include_stack_trace=True, **kwargs)
    
    def critical(self, message: str, error: Optional[str] = None, **kwargs):
        """Log critical message"""
        self.log(LogLevel.CRITICAL, message, error=error, include_stack_trace=True, **kwargs)
    
    def log_request(
        self,
        method: str,
        endpoint: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        start_time: Optional[float] = None,
        status_code: Optional[int] = None,
        error: Optional[str] = None
    ):
        """Log HTTP request"""
        duration_ms = None
        if start_time:
            duration_ms = (time.time() - start_time) * 1000
        
        level = LogLevel.INFO
        if error or (status_code and status_code >= 400):
            level = LogLevel.ERROR
        
        message = f"{method} {endpoint}"
        if status_code:
            message += f" - {status_code}"
        
        self.log(
            level=level,
            message=message,
            context={
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code
            },
            user_id=user_id,
            session_id=session_id,
            request_id=request_id,
            duration_ms=duration_ms,
            error=error
        )
    
    def get_logs(
        self,
        level: Optional[LogLevel] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        user_id: Optional[str] = None,
        component: Optional[str] = None,
        limit: int = 1000
    ) -> List[LogEntry]:
        """Get filtered logs"""
        filtered_logs = []
        
        for log_entry in self.log_storage:
            # Apply filters
            if level and log_entry.level != level:
                continue
            
            if time_range:
                start_time, end_time = time_range
                if not (start_time <= log_entry.timestamp <= end_time):
                    continue
            
            if user_id and log_entry.user_id != user_id:
                continue
            
            if component and log_entry.component != component:
                continue
            
            filtered_logs.append(log_entry)
            
            if len(filtered_logs) >= limit:
                break
        
        return filtered_logs


class SystemMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_storage: deque = deque(maxlen=10000)
        self.alerts: Dict[str, Alert] = {}
        self.health_checks: Dict[str, HealthCheck] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Default alert definitions
        self._create_default_alerts()
    
    def start_monitoring(self, interval_seconds: int = 30):
        """Start system monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval_seconds,),
            daemon=True
        )
        self.monitoring_thread.start()
        
        self.logger.info("System monitoring started", interval=interval_seconds)
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        self.logger.info("System monitoring stopped")
    
    def record_metric(
        self,
        name: str,
        value: float,
        category: MetricCategory,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None,
        threshold: Optional[float] = None
    ):
        """Record a system metric"""
        try:
            metric = SystemMetric(
                name=name,
                category=category,
                value=value,
                unit=unit,
                timestamp=datetime.now(timezone.utc),
                tags=tags or {},
                threshold=threshold
            )
            
            self.metrics_storage.append(metric)
            
            # Check for alerts
            self._check_metric_alerts(metric)
            
        except Exception as e:
            self.logger.error(f"Error recording metric {name}: {str(e)}")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add callback for alert notifications"""
        self.alert_callbacks.append(callback)
    
    def create_alert(
        self,
        name: str,
        description: str,
        severity: AlertSeverity,
        condition: str,
        threshold: float,
        duration_seconds: int = 300
    ) -> Alert:
        """Create a new alert"""
        alert = Alert(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            severity=severity,
            condition=condition,
            threshold=threshold,
            duration_seconds=duration_seconds,
            is_active=False,
            triggered_at=None,
            resolved_at=None,
            count=0,
            last_triggered=None
        )
        
        self.alerts[alert.id] = alert
        return alert
    
    def perform_health_check(self, component: str) -> HealthCheck:
        """Perform health check for a component"""
        start_time = time.time()
        
        try:
            if component == "database":
                result = self._check_database_health()
            elif component == "llm_api":
                result = self._check_llm_api_health()
            elif component == "redis":
                result = self._check_redis_health()
            elif component == "disk_space":
                result = self._check_disk_space_health()
            else:
                result = HealthCheck(
                    component=component,
                    status="healthy",
                    message="Component not monitored",
                    response_time_ms=(time.time() - start_time) * 1000,
                    timestamp=datetime.now(timezone.utc),
                    details={}
                )
            
            self.health_checks[component] = result
            return result
            
        except Exception as e:
            error_result = HealthCheck(
                component=component,
                status="unhealthy",
                message=f"Health check failed: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
            
            self.health_checks[component] = error_result
            return error_result
    
    def get_system_metrics(
        self,
        category: Optional[MetricCategory] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        limit: int = 1000
    ) -> List[SystemMetric]:
        """Get system metrics"""
        filtered_metrics = []
        
        for metric in self.metrics_storage:
            # Apply filters
            if category and metric.category != category:
                continue
            
            if time_range:
                start_time, end_time = time_range
                if not (start_time <= metric.timestamp <= end_time):
                    continue
            
            filtered_metrics.append(metric)
            
            if len(filtered_metrics) >= limit:
                break
        
        return filtered_metrics
    
    def get_active_alerts(self) -> List[Alert]:
        """Get currently active alerts"""
        return [alert for alert in self.alerts.values() if alert.is_active]
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        health_status = {
            "overall_status": "healthy",
            "components": {},
            "active_alerts": len(self.get_active_alerts()),
            "last_check": datetime.now(timezone.utc).isoformat()
        }
        
        # Check all components
        for component_name, health_check in self.health_checks.items():
            health_status["components"][component_name] = {
                "status": health_check.status,
                "message": health_check.message,
                "response_time_ms": health_check.response_time_ms,
                "timestamp": health_check.timestamp.isoformat()
            }
            
            # Update overall status
            if health_check.status == "unhealthy":
                health_status["overall_status"] = "unhealthy"
            elif health_check.status == "degraded" and health_status["overall_status"] == "healthy":
                health_status["overall_status"] = "degraded"
        
        return health_status
    
    def generate_monitoring_report(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive monitoring report"""
        try:
            # Set default time range (last 24 hours)
            if time_range is None:
                end_time = datetime.now(timezone.utc)
                start_time = end_time - timedelta(hours=24)
                time_range = (start_time, end_time)
            
            start_time, end_time = time_range
            
            # Get metrics by category
            metrics_by_category = defaultdict(list)
            for metric in self.get_system_metrics(time_range=time_range):
                metrics_by_category[metric.category].append(metric)
            
            # Calculate statistics
            report = {
                "period": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "duration_hours": (end_time - start_time).total_seconds() / 3600
                },
                "metrics_summary": {},
                "alerts_summary": {
                    "total_alerts": len(self.alerts),
                    "active_alerts": len(self.get_active_alerts()),
                    "resolved_alerts": len([a for a in self.alerts.values() if not a.is_active])
                },
                "health_summary": self.get_system_health(),
                "recommendations": []
            }
            
            # Analyze metrics by category
            for category, category_metrics in metrics_by_category.items():
                if not category_metrics:
                    continue
                
                values = [m.value for m in category_metrics]
                report["metrics_summary"][category.value] = {
                    "count": len(category_metrics),
                    "average": statistics.mean(values),
                    "min": min(values),
                    "max": max(values),
                    "latest": category_metrics[-1].value,
                    "trend": self._calculate_metric_trend(values)
                }
            
            # Generate recommendations
            report["recommendations"] = self._generate_monitoring_recommendations(
                metrics_by_category, self.get_active_alerts()
            )
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating monitoring report: {str(e)}")
            return {"error": str(e)}
    
    # Private methods
    def _monitoring_loop(self, interval_seconds: int):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._collect_system_metrics()
                self._perform_health_checks()
                time.sleep(interval_seconds)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(interval_seconds)
    
    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.record_metric(
                name="cpu_usage",
                value=cpu_percent,
                category=MetricCategory.SYSTEM,
                unit="percent",
                threshold=80.0
            )
            
            # Memory metrics
            memory = psutil.virtual_memory()
            self.record_metric(
                name="memory_usage",
                value=memory.percent,
                category=MetricCategory.SYSTEM,
                unit="percent",
                threshold=85.0
            )
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.record_metric(
                name="disk_usage",
                value=disk_percent,
                category=MetricCategory.SYSTEM,
                unit="percent",
                threshold=90.0
            )
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            self.record_metric(
                name="process_memory",
                value=process_memory,
                category=MetricCategory.APPLICATION,
                unit="MB",
                threshold=1000.0
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting system metrics: {str(e)}")
    
    def _perform_health_checks(self):
        """Perform all health checks"""
        components = ["database", "llm_api", "redis", "disk_space"]
        
        for component in components:
            try:
                self.perform_health_check(component)
            except Exception as e:
                self.logger.error(f"Health check failed for {component}: {str(e)}")
    
    def _check_metric_alerts(self, metric: SystemMetric):
        """Check if metric triggers any alerts"""
        for alert in self.alerts.values():
            if alert.is_active and metric.name in alert.condition:
                # Check if alert should be resolved
                if not metric.is_alert_threshold_exceeded():
                    self._resolve_alert(alert)
            elif not alert.is_active and metric.name in alert.condition:
                # Check if alert should be triggered
                if metric.is_alert_threshold_exceeded():
                    self._trigger_alert(alert, metric)
    
    def _trigger_alert(self, alert: Alert, metric: SystemMetric):
        """Trigger an alert"""
        alert.is_active = True
        alert.triggered_at = datetime.now(timezone.utc)
        alert.last_triggered = datetime.now(timezone.utc)
        alert.count += 1
        
        self.logger.warning(
            f"Alert triggered: {alert.name}",
            alert_id=alert.id,
            metric=metric.name,
            value=metric.value,
            threshold=alert.threshold
        )
        
        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {str(e)}")
    
    def _resolve_alert(self, alert: Alert):
        """Resolve an alert"""
        alert.is_active = False
        alert.resolved_at = datetime.now(timezone.utc)
        
        self.logger.info(
            f"Alert resolved: {alert.name}",
            alert_id=alert.id,
            duration_seconds=(
                alert.resolved_at - alert.triggered_at
            ).total_seconds() if alert.triggered_at else 0
        )
    
    def _create_default_alerts(self):
        """Create default system alerts"""
        self.create_alert(
            name="High CPU Usage",
            description="CPU usage is above threshold",
            severity=AlertSeverity.HIGH,
            condition="cpu_usage > threshold",
            threshold=80.0,
            duration_seconds=300
        )
        
        self.create_alert(
            name="High Memory Usage",
            description="Memory usage is above threshold",
            severity=AlertSeverity.HIGH,
            condition="memory_usage > threshold",
            threshold=85.0,
            duration_seconds=300
        )
        
        self.create_alert(
            name="High Disk Usage",
            description="Disk usage is above threshold",
            severity=AlertSeverity.CRITICAL,
            condition="disk_usage > threshold",
            threshold=90.0,
            duration_seconds=300
        )
    
    def _check_database_health(self) -> HealthCheck:
        """Check database health"""
        start_time = time.time()
        
        try:
            # Placeholder for actual database health check
            # In practice, you would check database connectivity, response time, etc.
            
            response_time_ms = (time.time() - start_time) * 1000
            
            return HealthCheck(
                component="database",
                status="healthy",
                message="Database is responding normally",
                response_time_ms=response_time_ms,
                timestamp=datetime.now(timezone.utc),
                details={
                    "connection_pool": "healthy",
                    "query_time": f"{response_time_ms:.2f}ms"
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="database",
                status="unhealthy",
                message=f"Database health check failed: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
    
    def _check_llm_api_health(self) -> HealthCheck:
        """Check LLM API health"""
        start_time = time.time()
        
        try:
            # Placeholder for actual LLM API health check
            # In practice, you would make a test API call
            
            response_time_ms = (time.time() - start_time) * 1000
            
            return HealthCheck(
                component="llm_api",
                status="healthy",
                message="LLM API is responding normally",
                response_time_ms=response_time_ms,
                timestamp=datetime.now(timezone.utc),
                details={
                    "api_response_time": f"{response_time_ms:.2f}ms"
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="llm_api",
                status="unhealthy",
                message=f"LLM API health check failed: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
    
    def _check_redis_health(self) -> HealthCheck:
        """Check Redis health"""
        start_time = time.time()
        
        try:
            # Placeholder for actual Redis health check
            
            response_time_ms = (time.time() - start_time) * 1000
            
            return HealthCheck(
                component="redis",
                status="healthy",
                message="Redis is responding normally",
                response_time_ms=response_time_ms,
                timestamp=datetime.now(timezone.utc),
                details={
                    "memory_usage": "normal",
                    "connection_count": "healthy"
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="redis",
                status="unhealthy",
                message=f"Redis health check failed: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
    
    def _check_disk_space_health(self) -> HealthCheck:
        """Check disk space health"""
        start_time = time.time()
        
        try:
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            response_time_ms = (time.time() - start_time) * 1000
            
            status = "healthy"
            if disk_percent > 90:
                status = "unhealthy"
            elif disk_percent > 80:
                status = "degraded"
            
            return HealthCheck(
                component="disk_space",
                status=status,
                message=f"Disk usage: {disk_percent:.1f}%",
                response_time_ms=response_time_ms,
                timestamp=datetime.now(timezone.utc),
                details={
                    "total_gb": disk.total / 1024 / 1024 / 1024,
                    "used_gb": disk.used / 1024 / 1024 / 1024,
                    "free_gb": disk.free / 1024 / 1024 / 1024,
                    "usage_percent": disk_percent
                }
            )
            
        except Exception as e:
            return HealthCheck(
                component="disk_space",
                status="unhealthy",
                message=f"Disk space check failed: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
    
    def _calculate_metric_trend(self, values: List[float]) -> str:
        """Calculate trend direction for metric values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression
        n = len(values)
        x = list(range(n))
        y = values
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if abs(slope) < 0.01:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _generate_monitoring_recommendations(
        self,
        metrics_by_category: Dict[MetricCategory, List[SystemMetric]],
        active_alerts: List[Alert]
    ) -> List[str]:
        """Generate monitoring recommendations"""
        recommendations = []
        
        # Check for active alerts
        if active_alerts:
            critical_alerts = [a for a in active_alerts if a.severity == AlertSeverity.CRITICAL]
            if critical_alerts:
                recommendations.append("Address critical alerts immediately")
            
            high_alerts = [a for a in active_alerts if a.severity == AlertSeverity.HIGH]
            if high_alerts:
                recommendations.append("Investigate high-priority alerts")
        
        # Check system metrics
        system_metrics = metrics_by_category.get(MetricCategory.SYSTEM, [])
        if system_metrics:
            cpu_values = [m.value for m in system_metrics if m.name == "cpu_usage"]
            if cpu_values and statistics.mean(cpu_values) > 70:
                recommendations.append("Consider scaling up resources due to high CPU usage")
            
            memory_values = [m.value for m in system_metrics if m.name == "memory_usage"]
            if memory_values and statistics.mean(memory_values) > 75:
                recommendations.append("Monitor memory usage and consider optimization")
        
        # Check application metrics
        app_metrics = metrics_by_category.get(MetricCategory.APPLICATION, [])
        if app_metrics:
            response_times = [m.value for m in app_metrics if "response_time" in m.name]
            if response_times and statistics.mean(response_times) > 2000:
                recommendations.append("Optimize application response times")
        
        return recommendations[:10]  # Return top 10 recommendations


class MonitoringAndLogging:
    """Main monitoring and logging interface"""
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.loggers: Dict[str, MonitoringLogger] = {}
        
        # Start system monitoring
        self.system_monitor.start_monitoring()
    
    def get_logger(self, component_name: str) -> MonitoringLogger:
        """Get logger for a component"""
        if component_name not in self.loggers:
            self.loggers[component_name] = MonitoringLogger(component_name)
        return self.loggers[component_name]
    
    def log_phase_execution(
        self,
        phase_name: str,
        phase4_result: Optional[Phase4Result] = None,
        phase5_result: Optional[Phase5Result] = None,
        user_feedback: Optional[List[UserFeedback]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log phase execution with metrics"""
        logger = self.get_logger(phase_name)
        
        try:
            # Log phase start
            start_time = time.time()
            logger.info(
                f"Phase {phase_name} started",
                context=context or {}
            )
            
            # Track metrics if results are available
            if phase4_result and user_feedback:
                metrics = self.system_monitor.metrics_tracker.track_recommendation_metrics(
                    phase4_result, phase5_result, user_feedback, context
                )
                
                # Log key metrics
                for metric_type, metric_value in metrics.items():
                    self.system_monitor.record_metric(
                        name=f"phase_{phase_name}_{metric_type.value}",
                        value=metric_value.value,
                        category=MetricCategory.APPLICATION,
                        unit="score"
                    )
            
            # Log phase completion
            duration_ms = (time.time() - start_time) * 1000
            logger.info(
                f"Phase {phase_name} completed",
                duration_ms=duration_ms,
                context=context or {}
            )
            
        except Exception as e:
            logger.error(
                f"Error logging phase {phase_name} execution",
                error=str(e)
            )
    
    def shutdown(self):
        """Shutdown monitoring and logging"""
        self.system_monitor.stop_monitoring()
