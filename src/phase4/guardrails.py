"""
Guardrails Module for Phase 4: LLM Recommendation and Reasoning Layer
Implements format checks, validation, and fallback behavior for invalid outputs.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

from prompt_builder import UserPreference, Restaurant
from response_parser import ParsedResponse, Recommendation


class ValidationLevel(Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationResult:
    """Result of validation check"""
    level: ValidationLevel
    message: str
    field: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class GuardrailResult:
    """Result of guardrail processing"""
    is_valid: bool
    validation_results: List[ValidationResult]
    fallback_triggered: bool
    processed_response: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class Guardrails:
    """Implements validation and fallback mechanisms for LLM responses"""
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize guardrails
        
        Args:
            strict_mode: If True, more validation errors will cause fallback
        """
        self.strict_mode = strict_mode
        self.logger = logging.getLogger(__name__)
        
        # Validation rules configuration
        self.validation_rules = {
            "min_recommendations": 1,
            "max_recommendations": 10,
            "min_score": 0.0,
            "max_score": 1.0,
            "required_fields": ["rank", "restaurant_name", "score", "explanation"],
            "max_explanation_length": 1000,
            "min_explanation_length": 20
        }
    
    def validate_and_process_response(
        self, 
        parsed_response: ParsedResponse,
        user_preferences: UserPreference,
        available_restaurants: List[Restaurant]
    ) -> GuardrailResult:
        """
        Validate parsed response and apply fallbacks if needed
        
        Args:
            parsed_response: Parsed response from LLM
            user_preferences: Original user preferences
            available_restaurants: Restaurants provided to LLM
            
        Returns:
            GuardrailResult with validation and any fallback processing
        """
        validation_results = []
        
        # Perform comprehensive validation
        validation_results.extend(self._validate_response_structure(parsed_response))
        validation_results.extend(self._validate_recommendations(parsed_response.recommendations))
        validation_results.extend(self._validate_against_preferences(parsed_response.recommendations, user_preferences))
        validation_results.extend(self._validate_against_candidates(parsed_response.recommendations, available_restaurants))
        
        # Determine if fallback is needed
        error_count = sum(1 for v in validation_results if v.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL])
        critical_count = sum(1 for v in validation_results if v.level == ValidationLevel.CRITICAL)
        
        needs_fallback = (
            critical_count > 0 or 
            (self.strict_mode and error_count > 0) or
            not parsed_response.is_valid
        )
        
        if needs_fallback:
            self.logger.warning(f"Triggering fallback due to {error_count} errors, {critical_count} critical")
            fallback_response = self._create_fallback_response(
                parsed_response, user_preferences, available_restaurants, validation_results
            )
            
            return GuardrailResult(
                is_valid=False,
                validation_results=validation_results,
                fallback_triggered=True,
                processed_response=fallback_response,
                error_message="Response failed validation, fallback generated"
            )
        else:
            # Process valid response
            processed_response = self._process_valid_response(parsed_response, validation_results)
            
            return GuardrailResult(
                is_valid=True,
                validation_results=validation_results,
                fallback_triggered=False,
                processed_response=processed_response
            )
    
    def _validate_response_structure(self, parsed_response: ParsedResponse) -> List[ValidationResult]:
        """Validate basic response structure"""
        results = []
        
        # Check if response exists
        if not parsed_response:
            results.append(ValidationResult(
                level=ValidationLevel.CRITICAL,
                message="No response data provided"
            ))
            return results
        
        # Check for fallback usage
        if parsed_response.fallback_used:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                message="Response was generated using fallback parsing",
                suggestion="Consider improving prompt or LLM parameters"
            ))
        
        # Check parsing errors
        if parsed_response.parsing_errors:
            for error in parsed_response.parsing_errors:
                results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    message=f"Parsing error: {error}"
                ))
        
        # Check summary and alternatives
        if not parsed_response.summary or len(parsed_response.summary.strip()) < 10:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                message="Summary is too short or missing",
                field="summary"
            ))
        
        return results
    
    def _validate_recommendations(self, recommendations: List[Recommendation]) -> List[ValidationResult]:
        """Validate individual recommendations"""
        results = []
        
        # Check recommendation count
        count = len(recommendations)
        if count < self.validation_rules["min_recommendations"]:
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message=f"Too few recommendations: {count} (minimum: {self.validation_rules['min_recommendations']})",
                field="recommendations"
            ))
        
        if count > self.validation_rules["max_recommendations"]:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                message=f"Too many recommendations: {count} (maximum: {self.validation_rules['max_recommendations']})",
                field="recommendations"
            ))
        
        # Validate each recommendation
        for i, rec in enumerate(recommendations):
            # Check required fields
            for field in self.validation_rules["required_fields"]:
                if not hasattr(rec, field) or getattr(rec, field) is None:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        message=f"Missing required field '{field}' in recommendation {i+1}",
                        field=f"recommendations[{i}].{field}"
                    ))
            
            # Validate score range
            if hasattr(rec, 'score') and rec.score is not None:
                if not (self.validation_rules["min_score"] <= rec.score <= self.validation_rules["max_score"]):
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        message=f"Score {rec.score} out of range [{self.validation_rules['min_score']}, {self.validation_rules['max_score']}]",
                        field=f"recommendations[{i}].score"
                    ))
            
            # Validate explanation length
            if hasattr(rec, 'explanation') and rec.explanation:
                exp_len = len(rec.explanation)
                if exp_len < self.validation_rules["min_explanation_length"]:
                    results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        message=f"Explanation too short: {exp_len} chars (minimum: {self.validation_rules['min_explanation_length']})",
                        field=f"recommendations[{i}].explanation"
                    ))
                
                if exp_len > self.validation_rules["max_explanation_length"]:
                    results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        message=f"Explanation too long: {exp_len} chars (maximum: {self.validation_rules['max_explanation_length']})",
                        field=f"recommendations[{i}].explanation"
                    ))
        
        # Check for duplicate ranks
        ranks = [rec.rank for rec in recommendations]
        if len(set(ranks)) != len(ranks):
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                message="Duplicate ranks found in recommendations",
                field="recommendations"
            ))
        
        # Check rank sequence
        sorted_ranks = sorted(ranks)
        expected_ranks = list(range(1, len(recommendations) + 1))
        if sorted_ranks != expected_ranks:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                message=f"Ranks not sequential: {sorted_ranks} (expected: {expected_ranks})",
                field="recommendations"
            ))
        
        return results
    
    def _validate_against_preferences(
        self, 
        recommendations: List[Recommendation], 
        preferences: UserPreference
    ) -> List[ValidationResult]:
        """Validate recommendations against user preferences"""
        results = []
        
        # This is a basic validation - in practice, you might want more sophisticated checks
        # For now, we'll just check that explanations mention relevant preferences
        
        pref_keywords = []
        if preferences.cuisine:
            pref_keywords.append(preferences.cuisine.lower())
        if preferences.location:
            pref_keywords.append(preferences.location.lower())
        
        if pref_keywords:
            for i, rec in enumerate(recommendations):
                explanation_lower = rec.explanation.lower()
                keyword_matches = sum(1 for keyword in pref_keywords if keyword in explanation_lower)
                
                if keyword_matches == 0:
                    results.append(ValidationResult(
                        level=ValidationLevel.INFO,
                        message=f"Recommendation {i+1} explanation doesn't mention user preferences",
                        field=f"recommendations[{i}].explanation",
                        suggestion="Consider making explanation more personalized"
                    ))
        
        return results
    
    def _validate_against_candidates(
        self, 
        recommendations: List[Recommendation], 
        available_restaurants: List[Restaurant]
    ) -> List[ValidationResult]:
        """Validate that recommended restaurants were in the candidate list"""
        results = []
        
        available_names = {r.name.lower() for r in available_restaurants}
        
        for i, rec in enumerate(recommendations):
            if rec.restaurant_name.lower() not in available_names:
                results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    message=f"Recommended restaurant '{rec.restaurant_name}' not in candidate list",
                    field=f"recommendations[{i}].restaurant_name"
                ))
        
        return results
    
    def _create_fallback_response(
        self, 
        parsed_response: ParsedResponse,
        preferences: UserPreference,
        available_restaurants: List[Restaurant],
        validation_results: List[ValidationResult]
    ) -> Dict[str, Any]:
        """Create fallback response when validation fails"""
        
        # Sort restaurants by rating as basic fallback
        sorted_restaurants = sorted(available_restaurants, key=lambda x: x.rating, reverse=True)
        
        fallback_recommendations = []
        
        for i, restaurant in enumerate(sorted_restaurants[:5], 1):
            # Create basic explanation
            explanation_parts = []
            explanation_parts.append(f"{restaurant.name} offers {restaurant.cuisine} cuisine")
            explanation_parts.append(f"It has a rating of {restaurant.rating}/5")
            explanation_parts.append(f"Located in {restaurant.location}")
            
            if preferences.cuisine and preferences.cuisine.lower() in restaurant.cuisine.lower():
                explanation_parts.append("Matches your cuisine preference")
            
            if restaurant.price_range:
                explanation_parts.append(f"Price range: {restaurant.price_range}")
            
            fallback_rec = {
                "rank": i,
                "restaurant_name": restaurant.name,
                "score": max(0.5, restaurant.rating / 5.0 - (i * 0.1)),  # Basic scoring
                "explanation": ". ".join(explanation_parts) + ".",
                "highlights": [
                    f"{restaurant.cuisine} cuisine",
                    f"Rating: {restaurant.rating}/5",
                    f"Location: {restaurant.location}"
                ],
                "considerations": [
                    "Fallback recommendation - generated due to validation failure",
                    "Please verify details independently"
                ]
            }
            fallback_recommendations.append(fallback_rec)
        
        return {
            "success": False,
            "fallback_used": True,
            "validation_errors": [v.message for v in validation_results if v.level in [ValidationLevel.ERROR, ValidationLevel.CRITICAL]],
            "validation_warnings": [v.message for v in validation_results if v.level == ValidationLevel.WARNING],
            "summary": f"Fallback recommendations generated due to validation failures. Found {len(sorted_restaurants)} restaurants, showing top {len(fallback_recommendations)}.",
            "alternatives": "Consider re-running with different parameters or improving input data quality.",
            "recommendations": fallback_recommendations
        }
    
    def _process_valid_response(self, parsed_response: ParsedResponse, validation_results: List[ValidationResult]) -> Dict[str, Any]:
        """Process valid response and add validation metadata"""
        
        processed = {
            "success": True,
            "fallback_used": False,
            "validation_warnings": [v.message for v in validation_results if v.level == ValidationLevel.WARNING],
            "validation_info": [v.message for v in validation_results if v.level == ValidationLevel.INFO],
            "summary": parsed_response.summary,
            "alternatives": parsed_response.alternatives,
            "recommendations": []
        }
        
        for rec in parsed_response.recommendations:
            rec_data = {
                "rank": rec.rank,
                "restaurant_name": rec.restaurant_name,
                "score": rec.score,
                "explanation": rec.explanation,
                "highlights": rec.highlights,
                "considerations": rec.considerations
            }
            processed["recommendations"].append(rec_data)
        
        return processed
    
    def get_validation_summary(self, guardrail_result: GuardrailResult) -> Dict[str, Any]:
        """Get summary of validation results"""
        level_counts = {}
        for level in ValidationLevel:
            level_counts[level.value] = sum(1 for v in guardrail_result.validation_results if v.level == level)
        
        return {
            "total_validations": len(guardrail_result.validation_results),
            "level_counts": level_counts,
            "is_valid": guardrail_result.is_valid,
            "fallback_triggered": guardrail_result.fallback_triggered,
            "has_warnings": level_counts.get("warning", 0) > 0,
            "has_errors": level_counts.get("error", 0) > 0,
            "has_critical": level_counts.get("critical", 0) > 0
        }
