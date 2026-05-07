"""
Response Parser Module for Phase 4: LLM Recommendation and Reasoning Layer
Extracts and validates rankings and explanations from LLM responses.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

from prompt_builder import Restaurant


@dataclass
class Recommendation:
    """Structured recommendation data"""
    rank: int
    restaurant_name: str
    score: float
    explanation: str
    highlights: List[str]
    considerations: List[str]


@dataclass
class ParsedResponse:
    """Parsed and validated response from LLM"""
    recommendations: List[Recommendation]
    summary: str
    alternatives: str
    is_valid: bool
    parsing_errors: List[str]
    fallback_used: bool = False


class ResponseParser:
    """Parses and validates LLM responses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_response(self, llm_content: str, available_restaurants: List[Restaurant]) -> ParsedResponse:
        """
        Parse LLM response and extract structured recommendations
        
        Args:
            llm_content: Raw content from LLM
            available_restaurants: List of restaurants that were provided to LLM
            
        Returns:
            ParsedResponse with structured data and validation info
        """
        parsing_errors = []
        
        try:
            # Try to extract JSON from the response
            json_content = self._extract_json(llm_content)
            
            if json_content:
                parsed_data = json.loads(json_content)
                return self._parse_structured_response(parsed_data, available_restaurants)
            else:
                parsing_errors.append("No valid JSON found in response")
                return self._create_fallback_response(llm_content, available_restaurants, parsing_errors)
                
        except json.JSONDecodeError as e:
            parsing_errors.append(f"JSON parsing error: {str(e)}")
            return self._create_fallback_response(llm_content, available_restaurants, parsing_errors)
        
        except Exception as e:
            parsing_errors.append(f"Unexpected parsing error: {str(e)}")
            return self._create_fallback_response(llm_content, available_restaurants, parsing_errors)
    
    def _extract_json(self, content: str) -> Optional[str]:
        """Extract JSON content from LLM response"""
        # Try to find JSON blocks with code fences
        json_patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'\{.*\}'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                for match in matches:
                    try:
                        # Validate if it's valid JSON
                        json.loads(match.strip())
                        return match.strip()
                    except json.JSONDecodeError:
                        continue
        
        # If no JSON blocks found, try to find JSON-like structure
        content_stripped = content.strip()
        if content_stripped.startswith('{') and content_stripped.endswith('}'):
            try:
                json.loads(content_stripped)
                return content_stripped
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _parse_structured_response(self, data: Dict[str, Any], available_restaurants: List[Restaurant]) -> ParsedResponse:
        """Parse structured JSON response"""
        recommendations = []
        parsing_errors = []
        
        # Extract recommendations
        if 'recommendations' in data and isinstance(data['recommendations'], list):
            for rec_data in data['recommendations']:
                try:
                    recommendation = self._parse_recommendation(rec_data, available_restaurants)
                    if recommendation:
                        recommendations.append(recommendation)
                except Exception as e:
                    parsing_errors.append(f"Error parsing recommendation: {str(e)}")
        else:
            parsing_errors.append("No recommendations array found in response")
        
        # Validate recommendations
        validated_recommendations, validation_errors = self._validate_recommendations(
            recommendations, available_restaurants
        )
        parsing_errors.extend(validation_errors)
        
        # Extract other fields
        summary = data.get('summary', 'No summary provided')
        alternatives = data.get('alternatives', 'No alternatives suggested')
        
        return ParsedResponse(
            recommendations=validated_recommendations,
            summary=summary,
            alternatives=alternatives,
            is_valid=len(validated_recommendations) > 0,
            parsing_errors=parsing_errors,
            fallback_used=False
        )
    
    def _parse_recommendation(self, rec_data: Dict[str, Any], available_restaurants: List[Restaurant]) -> Optional[Recommendation]:
        """Parse individual recommendation data"""
        required_fields = ['rank', 'restaurant_name', 'score', 'explanation']
        
        # Check required fields
        for field in required_fields:
            if field not in rec_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Extract and validate data
        rank = int(rec_data['rank'])
        restaurant_name = str(rec_data['restaurant_name'])
        score = float(rec_data['score'])
        explanation = str(rec_data['explanation'])
        
        highlights = rec_data.get('highlights', [])
        if not isinstance(highlights, list):
            highlights = [str(highlights)]
        
        considerations = rec_data.get('considerations', [])
        if not isinstance(considerations, list):
            considerations = [str(considerations)]
        
        # Validate score range
        if not 0 <= score <= 1:
            self.logger.warning(f"Score {score} not in [0,1] range for {restaurant_name}")
        
        return Recommendation(
            rank=rank,
            restaurant_name=restaurant_name,
            score=score,
            explanation=explanation,
            highlights=highlights,
            considerations=considerations
        )
    
    def _validate_recommendations(self, recommendations: List[Recommendation], available_restaurants: List[Restaurant]) -> Tuple[List[Recommendation], List[str]]:
        """Validate recommendations against available restaurants"""
        validated = []
        errors = []
        
        available_names = {r.name.lower() for r in available_restaurants}
        
        for rec in recommendations:
            # Check if restaurant exists in available list
            if rec.restaurant_name.lower() not in available_names:
                errors.append(f"Restaurant '{rec.restaurant_name}' not found in candidate list")
                continue
            
            # Check for duplicate ranks
            if any(r.rank == rec.rank for r in validated):
                errors.append(f"Duplicate rank {rec.rank} for restaurant '{rec.restaurant_name}'")
                continue
            
            validated.append(rec)
        
        # Sort by rank
        validated.sort(key=lambda x: x.rank)
        
        return validated, errors
    
    def _create_fallback_response(self, content: str, available_restaurants: List[Restaurant], errors: List[str]) -> ParsedResponse:
        """Create fallback response when structured parsing fails"""
        fallback_recommendations = []
        
        try:
            # Try to extract restaurant names and create simple recommendations
            mentioned_restaurants = self._extract_mentioned_restaurants(content, available_restaurants)
            
            for i, restaurant in enumerate(mentioned_restaurants[:5], 1):
                fallback_recommendations.append(Recommendation(
                    rank=i,
                    restaurant_name=restaurant.name,
                    score=0.8 - (i * 0.1),  # Decreasing scores
                    explanation=f"Extracted from LLM response: {restaurant.name} appears to be recommended",
                    highlights=[f"{restaurant.cuisine} cuisine", f"Rating: {restaurant.rating}"],
                    considerations=["Fallback parsing - verify manually"]
                ))
        except Exception as e:
            errors.append(f"Fallback parsing failed: {str(e)}")
        
        return ParsedResponse(
            recommendations=fallback_recommendations,
            summary="Fallback parsing - structured response was not available",
            alternatives="Consider re-running with different parameters",
            is_valid=len(fallback_recommendations) > 0,
            parsing_errors=errors,
            fallback_used=True
        )
    
    def _extract_mentioned_restaurants(self, content: str, available_restaurants: List[Restaurant]) -> List[Restaurant]:
        """Extract restaurant names mentioned in text content"""
        mentioned = []
        content_lower = content.lower()
        
        for restaurant in available_restaurants:
            if restaurant.name.lower() in content_lower:
                mentioned.append(restaurant)
        
        return mentioned
    
    def format_response_for_output(self, parsed_response: ParsedResponse) -> Dict[str, Any]:
        """Format parsed response for downstream consumption"""
        output = {
            "success": parsed_response.is_valid,
            "fallback_used": parsed_response.fallback_used,
            "parsing_errors": parsed_response.parsing_errors,
            "summary": parsed_response.summary,
            "alternatives": parsed_response.alternatives,
            "recommendations": []
        }
        
        for rec in parsed_response.recommendations:
            rec_output = {
                "rank": rec.rank,
                "restaurant_name": rec.restaurant_name,
                "score": rec.score,
                "explanation": rec.explanation,
                "highlights": rec.highlights,
                "considerations": rec.considerations
            }
            output["recommendations"].append(rec_output)
        
        return output
    
    def validate_response_quality(self, parsed_response: ParsedResponse) -> Dict[str, Any]:
        """Validate the quality of parsed response"""
        quality_metrics = {
            "has_recommendations": len(parsed_response.recommendations) > 0,
            "recommendation_count": len(parsed_response.recommendations),
            "has_summary": bool(parsed_response.summary.strip()),
            "has_alternatives": bool(parsed_response.alternatives.strip()),
            "all_scores_valid": all(0 <= rec.score <= 1 for rec in parsed_response.recommendations),
            "ranks_sequential": self._check_sequential_ranks(parsed_response.recommendations),
            "parsing_errors_count": len(parsed_response.parsing_errors),
            "fallback_used": parsed_response.fallback_used
        }
        
        # Overall quality score
        quality_score = 0
        if quality_metrics["has_recommendations"]:
            quality_score += 0.3
        if quality_metrics["has_summary"]:
            quality_score += 0.2
        if quality_metrics["has_alternatives"]:
            quality_score += 0.1
        if quality_metrics["all_scores_valid"]:
            quality_score += 0.2
        if quality_metrics["ranks_sequential"]:
            quality_score += 0.1
        if not quality_metrics["fallback_used"]:
            quality_score += 0.1
        
        quality_metrics["overall_quality_score"] = quality_score
        
        return quality_metrics
    
    def _check_sequential_ranks(self, recommendations: List[Recommendation]) -> bool:
        """Check if ranks are sequential starting from 1"""
        if not recommendations:
            return True
        
        expected_ranks = set(range(1, len(recommendations) + 1))
        actual_ranks = {rec.rank for rec in recommendations}
        
        return expected_ranks == actual_ranks
