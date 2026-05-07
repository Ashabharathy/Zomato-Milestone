"""
Prompt/Version Manager Module for Phase 6: Feedback, Evaluation, and Improvement Loop
Manages prompt versions and A/B testing for continuous improvement.
"""

import json
import time
import uuid
import hashlib
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime, timezone, timedelta
import random
import statistics

# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from .metrics_tracker import MetricsTracker, MetricType, MetricValue


class ExperimentStatus(Enum):
    """Status of A/B testing experiments"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class PromptType(Enum):
    """Types of prompts to manage"""
    SYSTEM_PROMPT = "system_prompt"
    USER_PROMPT = "user_prompt"
    RANKING_PROMPT = "ranking_prompt"
    EXPLANATION_PROMPT = "explanation_prompt"
    FILTERING_PROMPT = "filtering_prompt"


class VariantType(Enum):
    """Types of experiment variants"""
    CONTROL = "control"
    TREATMENT = "treatment"


@dataclass
class PromptTemplate:
    """Prompt template definition"""
    id: str
    name: str
    type: PromptType
    template: str
    variables: List[str]
    description: str
    version: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = PromptType(self.type)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)
    
    def render(self, variables: Dict[str, Any]) -> str:
        """Render template with variables"""
        try:
            rendered = self.template
            for var_name, var_value in variables.items():
                if var_name in self.variables:
                    rendered = rendered.replace(f"{{{var_name}}}", str(var_value))
            return rendered
        except Exception as e:
            logging.error(f"Error rendering template {self.id}: {str(e)}")
            return self.template
    
    def validate_variables(self, variables: Dict[str, Any]) -> List[str]:
        """Validate required variables"""
        missing_vars = []
        for var in self.variables:
            if var not in variables:
                missing_vars.append(var)
        return missing_vars


@dataclass
class Experiment:
    """A/B testing experiment definition"""
    id: str
    name: str
    description: str
    prompt_type: PromptType
    control_template_id: str
    treatment_template_ids: List[str]
    traffic_split: Dict[str, float]  # template_id -> percentage
    status: ExperimentStatus
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    sample_size: int
    confidence_level: float
    success_criteria: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if isinstance(self.prompt_type, str):
            self.prompt_type = PromptType(self.prompt_type)
        if isinstance(self.status, str):
            self.status = ExperimentStatus(self.status)
        if isinstance(self.start_date, str):
            self.start_date = datetime.fromisoformat(self.start_date)
        if isinstance(self.end_date, str):
            self.end_date = datetime.fromisoformat(self.end_date)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)
    
    def is_active(self) -> bool:
        """Check if experiment is currently active"""
        if self.status != ExperimentStatus.ACTIVE:
            return False
        
        now = datetime.now(timezone.utc)
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    def get_variant_for_user(self, user_id: str) -> str:
        """Assign variant to user based on traffic split"""
        # Use consistent hashing for user assignment
        hash_input = f"{self.id}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        user_percentage = (hash_value % 100) / 100.0
        
        cumulative = 0.0
        for template_id, percentage in self.traffic_split.items():
            cumulative += percentage
            if user_percentage <= cumulative:
                return template_id
        
        # Fallback to control
        return self.control_template_id


@dataclass
class ExperimentResult:
    """Results of an A/B testing experiment"""
    experiment_id: str
    variant_results: Dict[str, Dict[str, Any]]
    statistical_significance: bool
    winner: Optional[str]
    confidence_interval: Optional[Tuple[float, float]]
    effect_size: Optional[float]
    sample_size: int
    duration_days: int
    generated_at: datetime
    
    def __post_init__(self):
        if isinstance(self.generated_at, str):
            self.generated_at = datetime.fromisoformat(self.generated_at)


@dataclass
class PromptPerformance:
    """Performance metrics for a prompt template"""
    template_id: str
    experiment_id: Optional[str]
    variant_type: VariantType
    metrics: Dict[str, float]
    sample_size: int
    conversion_rate: float
    average_rating: float
    response_time: float
    error_rate: float
    user_satisfaction: float
    last_updated: datetime
    
    def __post_init__(self):
        if isinstance(self.variant_type, str):
            self.variant_type = VariantType(self.variant_type)
        if isinstance(self.last_updated, str):
            self.last_updated = datetime.fromisoformat(self.last_updated)


class PromptVersionManager:
    """Manages prompt versions and A/B testing experiments"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_tracker = MetricsTracker()
        
        # Storage
        self.templates: Dict[str, PromptTemplate] = {}
        self.experiments: Dict[str, Experiment] = {}
        self.experiment_results: Dict[str, ExperimentResult] = {}
        self.prompt_performance: Dict[str, PromptPerformance] = {}
        
        # User assignments
        self.user_assignments: Dict[str, Dict[str, str]] = {}  # user_id -> experiment_id -> template_id
    
    def create_prompt_template(
        self,
        name: str,
        prompt_type: PromptType,
        template: str,
        description: str = "",
        variables: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PromptTemplate:
        """
        Create a new prompt template
        
        Args:
            name: Template name
            prompt_type: Type of prompt
            template: Template string with {variable} placeholders
            description: Template description
            variables: List of required variables
            metadata: Additional metadata
            
        Returns:
            Created PromptTemplate
        """
        try:
            # Generate ID
            template_id = str(uuid.uuid4())
            
            # Extract variables from template if not provided
            if variables is None:
                variables = self._extract_variables(template)
            
            # Create template
            prompt_template = PromptTemplate(
                id=template_id,
                name=name,
                type=prompt_type,
                template=template,
                variables=variables,
                description=description,
                version="1.0.0",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                is_active=True,
                metadata=metadata or {}
            )
            
            # Store template
            self.templates[template_id] = prompt_template
            
            self.logger.info(
                "prompt_template_created",
                template_id=template_id,
                name=name,
                type=prompt_type.value
            )
            
            return prompt_template
            
        except Exception as e:
            self.logger.error(f"Error creating prompt template: {str(e)}")
            raise
    
    def update_prompt_template(
        self,
        template_id: str,
        template: Optional[str] = None,
        description: Optional[str] = None,
        variables: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PromptTemplate:
        """
        Update an existing prompt template
        
        Args:
            template_id: Template ID
            template: New template string (optional)
            description: New description (optional)
            variables: New variables list (optional)
            metadata: New metadata (optional)
            
        Returns:
            Updated PromptTemplate
        """
        try:
            if template_id not in self.templates:
                raise ValueError(f"Template {template_id} not found")
            
            template_obj = self.templates[template_id]
            
            # Update fields
            if template is not None:
                template_obj.template = template
                if variables is None:
                    template_obj.variables = self._extract_variables(template)
            
            if description is not None:
                template_obj.description = description
            
            if variables is not None:
                template_obj.variables = variables
            
            if metadata is not None:
                template_obj.metadata.update(metadata)
            
            # Update version and timestamp
            template_obj.version = self._increment_version(template_obj.version)
            template_obj.updated_at = datetime.now(timezone.utc)
            
            self.logger.info(
                "prompt_template_updated",
                template_id=template_id,
                new_version=template_obj.version
            )
            
            return template_obj
            
        except Exception as e:
            self.logger.error(f"Error updating prompt template: {str(e)}")
            raise
    
    def create_experiment(
        self,
        name: str,
        description: str,
        prompt_type: PromptType,
        control_template_id: str,
        treatment_template_ids: List[str],
        traffic_split: Optional[Dict[str, float]] = None,
        sample_size: int = 1000,
        confidence_level: float = 0.95,
        success_criteria: Optional[Dict[str, Any]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Experiment:
        """
        Create an A/B testing experiment
        
        Args:
            name: Experiment name
            description: Experiment description
            prompt_type: Type of prompt being tested
            control_template_id: Control template ID
            treatment_template_ids: List of treatment template IDs
            traffic_split: Traffic split percentages (optional)
            sample_size: Required sample size
            confidence_level: Statistical confidence level
            success_criteria: Success criteria definition
            start_date: Experiment start date (optional)
            end_date: Experiment end date (optional)
            
        Returns:
            Created Experiment
        """
        try:
            # Validate templates exist
            if control_template_id not in self.templates:
                raise ValueError(f"Control template {control_template_id} not found")
            
            for tid in treatment_template_ids:
                if tid not in self.templates:
                    raise ValueError(f"Treatment template {tid} not found")
            
            # Generate ID
            experiment_id = str(uuid.uuid4())
            
            # Set default traffic split
            if traffic_split is None:
                total_variants = len(treatment_template_ids) + 1
                split_percentage = 1.0 / total_variants
                traffic_split = {control_template_id: split_percentage}
                for tid in treatment_template_ids:
                    traffic_split[tid] = split_percentage
            
            # Validate traffic split
            if abs(sum(traffic_split.values()) - 1.0) > 0.01:
                raise ValueError("Traffic split must sum to 1.0")
            
            # Create experiment
            experiment = Experiment(
                id=experiment_id,
                name=name,
                description=description,
                prompt_type=prompt_type,
                control_template_id=control_template_id,
                treatment_template_ids=treatment_template_ids,
                traffic_split=traffic_split,
                status=ExperimentStatus.DRAFT,
                start_date=start_date,
                end_date=end_date,
                sample_size=sample_size,
                confidence_level=confidence_level,
                success_criteria=success_criteria or {},
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                metadata={}
            )
            
            # Store experiment
            self.experiments[experiment_id] = experiment
            
            self.logger.info(
                "experiment_created",
                experiment_id=experiment_id,
                name=name,
                control_template=control_template_id,
                treatment_templates=treatment_template_ids
            )
            
            return experiment
            
        except Exception as e:
            self.logger.error(f"Error creating experiment: {str(e)}")
            raise
    
    def start_experiment(self, experiment_id: str) -> Experiment:
        """Start an A/B testing experiment"""
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            if experiment.status != ExperimentStatus.DRAFT:
                raise ValueError(f"Experiment {experiment_id} is not in draft status")
            
            # Update experiment
            experiment.status = ExperimentStatus.ACTIVE
            experiment.start_date = datetime.now(timezone.utc)
            experiment.updated_at = datetime.now(timezone.utc)
            
            self.logger.info(
                "experiment_started",
                experiment_id=experiment_id,
                start_date=experiment.start_date.isoformat()
            )
            
            return experiment
            
        except Exception as e:
            self.logger.error(f"Error starting experiment: {str(e)}")
            raise
    
    def stop_experiment(self, experiment_id: str) -> Experiment:
        """Stop an A/B testing experiment"""
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            if experiment.status != ExperimentStatus.ACTIVE:
                raise ValueError(f"Experiment {experiment_id} is not active")
            
            # Update experiment
            experiment.status = ExperimentStatus.COMPLETED
            experiment.end_date = datetime.now(timezone.utc)
            experiment.updated_at = datetime.now(timezone.utc)
            
            # Generate results
            results = self.analyze_experiment_results(experiment_id)
            self.experiment_results[experiment_id] = results
            
            self.logger.info(
                "experiment_stopped",
                experiment_id=experiment_id,
                end_date=experiment.end_date.isoformat(),
                winner=results.winner
            )
            
            return experiment
            
        except Exception as e:
            self.logger.error(f"Error stopping experiment: {str(e)}")
            raise
    
    def get_prompt_for_user(
        self,
        prompt_type: PromptType,
        user_id: str,
        variables: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Get appropriate prompt template for user
        
        Args:
            prompt_type: Type of prompt needed
            user_id: User ID
            variables: Variables for template rendering
            
        Returns:
            Tuple of (rendered_prompt, template_id)
        """
        try:
            # Find active experiments for this prompt type
            active_experiments = [
                exp for exp in self.experiments.values()
                if exp.is_active() and exp.prompt_type == prompt_type
            ]
            
            if active_experiments:
                # Use A/B testing
                experiment = active_experiments[0]  # Use first active experiment
                template_id = experiment.get_variant_for_user(user_id)
                
                # Store assignment
                if user_id not in self.user_assignments:
                    self.user_assignments[user_id] = {}
                self.user_assignments[user_id][experiment.id] = template_id
                
            else:
                # Use default active template
                template_id = self._get_default_template(prompt_type)
            
            if template_id not in self.templates:
                raise ValueError(f"Template {template_id} not found")
            
            template = self.templates[template_id]
            rendered_prompt = template.render(variables)
            
            return rendered_prompt, template_id
            
        except Exception as e:
            self.logger.error(f"Error getting prompt for user: {str(e)}")
            # Fallback to basic template
            return self._get_fallback_prompt(prompt_type, variables), "fallback"
    
    def track_prompt_performance(
        self,
        template_id: str,
        user_id: str,
        phase4_result: Phase4Result,
        user_feedback: List[Any],
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Track performance of a prompt template
        
        Args:
            template_id: Template ID
            user_id: User ID
            phase4_result: Phase 4 result
            user_feedback: User feedback
            context: Additional context
        """
        try:
            # Get or create performance record
            if template_id not in self.prompt_performance:
                self.prompt_performance[template_id] = PromptPerformance(
                    template_id=template_id,
                    experiment_id=None,
                    variant_type=VariantType.CONTROL,
                    metrics={},
                    sample_size=0,
                    conversion_rate=0.0,
                    average_rating=0.0,
                    response_time=0.0,
                    error_rate=0.0,
                    user_satisfaction=0.0,
                    last_updated=datetime.now(timezone.utc)
                )
            
            performance = self.prompt_performance[template_id]
            
            # Calculate metrics
            metrics = self.metrics_tracker.track_recommendation_metrics(
                phase4_result, None, user_feedback, context
            )
            
            # Update performance
            performance.sample_size += 1
            
            # Update specific metrics
            if MetricType.CONVERSION_RATE in metrics:
                performance.conversion_rate = (
                    (performance.conversion_rate * (performance.sample_size - 1) + 
                     metrics[MetricType.CONVERSION_RATE].value) / performance.sample_size
                )
            
            if MetricType.SATISFACTION_SCORE in metrics:
                performance.user_satisfaction = (
                    (performance.user_satisfaction * (performance.sample_size - 1) + 
                     metrics[MetricType.SATISFACTION_SCORE].value) / performance.sample_size
                )
            
            if MetricType.RESPONSE_LATENCY in metrics:
                performance.response_time = (
                    (performance.response_time * (performance.sample_size - 1) + 
                     metrics[MetricType.RESPONSE_LATENCY].value) / performance.sample_size
                )
            
            if MetricType.ERROR_RATE in metrics:
                performance.error_rate = (
                    (performance.error_rate * (performance.sample_size - 1) + 
                     metrics[MetricType.ERROR_RATE].value) / performance.sample_size
                )
            
            # Update metrics dictionary
            for metric_type, metric_value in metrics.items():
                performance.metrics[metric_type.value] = metric_value.value
            
            performance.last_updated = datetime.now(timezone.utc)
            
            self.logger.debug(
                "prompt_performance_tracked",
                template_id=template_id,
                sample_size=performance.sample_size,
                conversion_rate=performance.conversion_rate
            )
            
        except Exception as e:
            self.logger.error(f"Error tracking prompt performance: {str(e)}")
    
    def analyze_experiment_results(self, experiment_id: str) -> ExperimentResult:
        """
        Analyze results of an A/B testing experiment
        
        Args:
            experiment_id: Experiment ID
            
        Returns:
            ExperimentResult
        """
        try:
            if experiment_id not in self.experiments:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            experiment = self.experiments[experiment_id]
            
            # Collect results for each variant
            variant_results = {}
            
            # Control group
            control_performance = self.prompt_performance.get(experiment.control_template_id)
            if control_performance:
                variant_results[experiment.control_template_id] = {
                    "sample_size": control_performance.sample_size,
                    "conversion_rate": control_performance.conversion_rate,
                    "user_satisfaction": control_performance.user_satisfaction,
                    "response_time": control_performance.response_time,
                    "error_rate": control_performance.error_rate
                }
            
            # Treatment groups
            for treatment_id in experiment.treatment_template_ids:
                treatment_performance = self.prompt_performance.get(treatment_id)
                if treatment_performance:
                    variant_results[treatment_id] = {
                        "sample_size": treatment_performance.sample_size,
                        "conversion_rate": treatment_performance.conversion_rate,
                        "user_satisfaction": treatment_performance.user_satisfaction,
                        "response_time": treatment_performance.response_time,
                        "error_rate": treatment_performance.error_rate
                    }
            
            # Perform statistical analysis
            statistical_significance, winner, confidence_interval, effect_size = self._perform_statistical_analysis(
                variant_results, experiment.confidence_level
            )
            
            # Calculate duration
            duration_days = 0
            if experiment.start_date and experiment.end_date:
                duration_days = (experiment.end_date - experiment.start_date).days
            elif experiment.start_date:
                duration_days = (datetime.now(timezone.utc) - experiment.start_date).days
            
            # Total sample size
            total_sample_size = sum(
                result["sample_size"] for result in variant_results.values()
            )
            
            return ExperimentResult(
                experiment_id=experiment_id,
                variant_results=variant_results,
                statistical_significance=statistical_significance,
                winner=winner,
                confidence_interval=confidence_interval,
                effect_size=effect_size,
                sample_size=total_sample_size,
                duration_days=duration_days,
                generated_at=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing experiment results: {str(e)}")
            raise
    
    def get_best_template(
        self,
        prompt_type: PromptType,
        metric: str = "conversion_rate"
    ) -> Optional[PromptTemplate]:
        """
        Get best performing template for a prompt type
        
        Args:
            prompt_type: Type of prompt
            metric: Metric to optimize for
            
        Returns:
            Best performing PromptTemplate
        """
        try:
            # Filter templates by type
            type_templates = [
                template for template in self.templates.values()
                if template.type == prompt_type and template.is_active
            ]
            
            if not type_templates:
                return None
            
            # Get performance for each template
            template_scores = {}
            for template in type_templates:
                performance = self.prompt_performance.get(template.id)
                if performance and hasattr(performance, metric):
                    template_scores[template.id] = getattr(performance, metric)
                else:
                    template_scores[template.id] = 0.0
            
            # Return template with highest score
            best_template_id = max(template_scores, key=template_scores.get)
            return self.templates[best_template_id]
            
        except Exception as e:
            self.logger.error(f"Error getting best template: {str(e)}")
            return None
    
    def get_prompt_insights(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get insights about prompt performance
        
        Args:
            time_range: Time range for analysis (optional)
            
        Returns:
            Insights dictionary
        """
        try:
            insights = {
                "total_templates": len(self.templates),
                "active_templates": len([t for t in self.templates.values() if t.is_active]),
                "total_experiments": len(self.experiments),
                "active_experiments": len([e for e in self.experiments.values() if e.is_active()]),
                "completed_experiments": len([e for e in self.experiments.values() if e.status == ExperimentStatus.COMPLETED]),
                "template_performance": {},
                "experiment_results": {},
                "recommendations": []
            }
            
            # Template performance by type
            template_by_type = {}
            for template in self.templates.values():
                if template.type not in template_by_type:
                    template_by_type[template.type] = []
                template_by_type[template.type].append(template.id)
            
            for prompt_type, template_ids in template_by_type.items():
                type_performance = []
                for template_id in template_ids:
                    performance = self.prompt_performance.get(template_id)
                    if performance:
                        type_performance.append({
                            "template_id": template_id,
                            "conversion_rate": performance.conversion_rate,
                            "user_satisfaction": performance.user_satisfaction,
                            "sample_size": performance.sample_size
                        })
                
                # Sort by conversion rate
                type_performance.sort(key=lambda x: x["conversion_rate"], reverse=True)
                insights["template_performance"][prompt_type.value] = type_performance
            
            # Experiment results
            for experiment_id, result in self.experiment_results.items():
                experiment = self.experiments[experiment_id]
                insights["experiment_results"][experiment_id] = {
                    "name": experiment.name,
                    "status": experiment.status.value,
                    "winner": result.winner,
                    "statistical_significance": result.statistical_significance,
                    "sample_size": result.sample_size
                }
            
            # Generate recommendations
            insights["recommendations"] = self._generate_prompt_recommendations()
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting prompt insights: {str(e)}")
            return {}
    
    # Helper methods
    def _extract_variables(self, template: str) -> List[str]:
        """Extract variable names from template"""
        import re
        pattern = r'\{([^}]+)\}'
        matches = re.findall(pattern, template)
        return list(set(matches))
    
    def _increment_version(self, version: str) -> str:
        """Increment version number"""
        try:
            parts = version.split('.')
            parts[-1] = str(int(parts[-1]) + 1)
            return '.'.join(parts)
        except:
            return "2.0.0"
    
    def _get_default_template(self, prompt_type: PromptType) -> str:
        """Get default active template for prompt type"""
        active_templates = [
            template for template in self.templates.values()
            if template.type == prompt_type and template.is_active
        ]
        
        if active_templates:
            return active_templates[0].id
        
        # Create fallback template if none exists
        return self._create_fallback_template(prompt_type)
    
    def _create_fallback_template(self, prompt_type: PromptType) -> str:
        """Create fallback template for prompt type"""
        fallback_templates = {
            PromptType.SYSTEM_PROMPT: "You are a helpful restaurant recommendation assistant.",
            PromptType.USER_PROMPT: "Please recommend restaurants based on the following criteria: {criteria}",
            PromptType.RANKING_PROMPT: "Rank these restaurants: {restaurants}",
            PromptType.EXPLANATION_PROMPT: "Explain why these restaurants are recommended: {restaurants}",
            PromptType.FILTERING_PROMPT: "Filter restaurants based on: {criteria}"
        }
        
        template_text = fallback_templates.get(prompt_type, "Default prompt template")
        
        template = self.create_prompt_template(
            name=f"Fallback {prompt_type.value}",
            prompt_type=prompt_type,
            template=template_text,
            description="Auto-generated fallback template",
            variables=self._extract_variables(template_text)
        )
        
        return template.id
    
    def _get_fallback_prompt(self, prompt_type: PromptType, variables: Dict[str, Any]) -> str:
        """Get fallback prompt text"""
        fallback_prompts = {
            PromptType.SYSTEM_PROMPT: "You are a helpful restaurant recommendation assistant.",
            PromptType.USER_PROMPT: "Please recommend restaurants based on the provided criteria.",
            PromptType.RANKING_PROMPT: "Please rank the given restaurants.",
            PromptType.EXPLANATION_PROMPT: "Please explain the restaurant recommendations.",
            PromptType.FILTERING_PROMPT: "Please filter the restaurants based on criteria."
        }
        
        return fallback_prompts.get(prompt_type, "Please provide restaurant recommendations.")
    
    def _perform_statistical_analysis(
        self,
        variant_results: Dict[str, Dict[str, Any]],
        confidence_level: float
    ) -> Tuple[bool, Optional[str], Optional[Tuple[float, float]], Optional[float]]:
        """Perform statistical analysis on experiment results"""
        try:
            if len(variant_results) < 2:
                return False, None, None, None
            
            # Get conversion rates for comparison
            variants = list(variant_results.keys())
            control_rate = variant_results[variants[0]]["conversion_rate"]
            treatment_rate = variant_results[variants[1]]["conversion_rate"]
            
            # Sample sizes
            control_size = variant_results[variants[0]]["sample_size"]
            treatment_size = variant_results[variants[1]]["sample_size"]
            
            # Perform simple statistical test
            if control_size < 30 or treatment_size < 30:
                return False, None, None, None
            
            # Calculate pooled proportion
            pooled_rate = (control_rate * control_size + treatment_rate * treatment_size) / (control_size + treatment_size)
            
            # Calculate standard error
            se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_size + 1/treatment_size))
            
            # Calculate z-score
            z_score = abs(treatment_rate - control_rate) / se if se > 0 else 0
            
            # Determine statistical significance (simplified)
            z_critical = 1.96  # For 95% confidence
            statistical_significance = z_score > z_critical
            
            # Determine winner
            winner = None
            if statistical_significance:
                winner = variants[0] if control_rate > treatment_rate else variants[1]
            
            # Calculate confidence interval (simplified)
            margin_error = z_critical * se if se > 0 else 0
            confidence_interval = (treatment_rate - margin_error, treatment_rate + margin_error)
            
            # Calculate effect size (Cohen's h)
            effect_size = 2 * math.asin(math.sqrt(treatment_rate)) - 2 * math.asin(math.sqrt(control_rate))
            
            return statistical_significance, winner, confidence_interval, effect_size
            
        except Exception as e:
            self.logger.error(f"Error performing statistical analysis: {str(e)}")
            return False, None, None, None
    
    def _generate_prompt_recommendations(self) -> List[str]:
        """Generate recommendations based on prompt performance"""
        recommendations = []
        
        # Check for underperforming templates
        for template_id, performance in self.prompt_performance.items():
            if performance.sample_size > 100:
                if performance.conversion_rate < 0.1:
                    recommendations.append(f"Template {template_id} has low conversion rate ({performance.conversion_rate:.2%})")
                
                if performance.user_satisfaction < 0.5:
                    recommendations.append(f"Template {template_id} has low user satisfaction ({performance.user_satisfaction:.2%})")
                
                if performance.error_rate > 0.1:
                    recommendations.append(f"Template {template_id} has high error rate ({performance.error_rate:.2%})")
        
        # Check for successful experiments
        for experiment_id, result in self.experiment_results.items():
            if result.statistical_significance and result.winner:
                experiment = self.experiments[experiment_id]
                recommendations.append(f"Experiment {experiment.name} has a clear winner: {result.winner}")
        
        return recommendations[:10]  # Return top 10 recommendations
