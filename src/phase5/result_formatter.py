"""
Result Formatter Module for Phase 5: Response Assembly and Presentation Layer
Formats LLM recommendations into card/list/table JSON structures for different output formats.
"""

import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging


class OutputFormat(Enum):
    """Supported output formats"""
    CARD = "card"
    LIST = "list"
    TABLE = "table"
    COMPACT = "compact"
    DETAILED = "detailed"


@dataclass
class FormattedRecommendation:
    """Formatted recommendation data"""
    rank: int
    restaurant_name: str
    score: float
    explanation: str
    highlights: List[str]
    considerations: List[str]
    cuisine: Optional[str] = None
    rating: Optional[float] = None
    price_range: Optional[str] = None
    avg_cost_for_two: Optional[float] = None
    location: Optional[str] = None
    address: Optional[str] = None
    features: Optional[List[str]] = None


@dataclass
class FormattedResult:
    """Complete formatted result package"""
    format_type: OutputFormat
    recommendations: List[FormattedRecommendation]
    summary: str
    alternatives: str
    metadata: Dict[str, Any]
    success: bool
    total_count: int


class ResultFormatter:
    """Formats LLM recommendations into various output structures"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def format_recommendations(
        self, 
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        max_recommendations: Optional[int] = None
    ) -> FormattedResult:
        """
        Format Phase 4 LLM results into specified output format
        
        Args:
            phase4_result: Raw result from Phase 4 LLM processing
            output_format: Desired output format (card, list, table, etc.)
            max_recommendations: Maximum number of recommendations to include
            
        Returns:
            FormattedResult with structured data
        """
        try:
            # Extract basic information
            success = phase4_result.get("success", False)
            recommendations_data = phase4_result.get("recommendations", [])
            summary = phase4_result.get("summary", "")
            alternatives = phase4_result.get("alternatives", "")
            
            # Limit recommendations if specified
            if max_recommendations:
                recommendations_data = recommendations_data[:max_recommendations]
            
            # Convert to formatted recommendations
            formatted_recommendations = []
            for rec_data in recommendations_data:
                formatted_rec = self._create_formatted_recommendation(rec_data)
                formatted_recommendations.append(formatted_rec)
            
            # Apply format-specific transformations
            if output_format == OutputFormat.CARD:
                formatted_recommendations = self._format_as_cards(formatted_recommendations)
            elif output_format == OutputFormat.LIST:
                formatted_recommendations = self._format_as_list(formatted_recommendations)
            elif output_format == OutputFormat.TABLE:
                formatted_recommendations = self._format_as_table(formatted_recommendations)
            elif output_format == OutputFormat.COMPACT:
                formatted_recommendations = self._format_as_compact(formatted_recommendations)
            elif output_format == OutputFormat.DETAILED:
                formatted_recommendations = self._format_as_detailed(formatted_recommendations)
            
            # Create metadata
            metadata = self._create_metadata(phase4_result, output_format)
            
            return FormattedResult(
                format_type=output_format,
                recommendations=formatted_recommendations,
                summary=summary,
                alternatives=alternatives,
                metadata=metadata,
                success=success,
                total_count=len(formatted_recommendations)
            )
            
        except Exception as e:
            self.logger.error(f"Error formatting recommendations: {str(e)}")
            return self._create_error_result(str(e))
    
    def _create_formatted_recommendation(self, rec_data: Dict[str, Any]) -> FormattedRecommendation:
        """Create FormattedRecommendation from raw data"""
        return FormattedRecommendation(
            rank=rec_data.get("rank", 0),
            restaurant_name=rec_data.get("restaurant_name", ""),
            score=rec_data.get("score", 0.0),
            explanation=rec_data.get("explanation", ""),
            highlights=rec_data.get("highlights", []),
            considerations=rec_data.get("considerations", []),
            cuisine=rec_data.get("cuisine"),
            rating=rec_data.get("rating"),
            price_range=rec_data.get("price_range"),
            avg_cost_for_two=rec_data.get("avg_cost_for_two"),
            location=rec_data.get("location"),
            address=rec_data.get("address"),
            features=rec_data.get("features")
        )
    
    def _format_as_cards(self, recommendations: List[FormattedRecommendation]) -> List[FormattedRecommendation]:
        """Format recommendations as interactive cards"""
        formatted = []
        
        for rec in recommendations:
            # Add card-specific formatting
            card_rec = FormattedRecommendation(
                rank=rec.rank,
                restaurant_name=rec.restaurant_name,
                score=rec.score,
                explanation=self._truncate_text(rec.explanation, 200),  # Shorter for cards
                highlights=rec.highlights[:3],  # Limit highlights
                considerations=rec.considerations[:2],  # Limit considerations
                cuisine=rec.cuisine,
                rating=rec.rating,
                price_range=rec.price_range,
                avg_cost_for_two=rec.avg_cost_for_two,
                location=rec.location,
                address=rec.address,
                features=rec.features[:5] if rec.features else None  # Limit features
            )
            formatted.append(card_rec)
        
        return formatted
    
    def _format_as_list(self, recommendations: List[FormattedRecommendation]) -> List[FormattedRecommendation]:
        """Format recommendations as simple list items"""
        formatted = []
        
        for rec in recommendations:
            # Add list-specific formatting
            list_rec = FormattedRecommendation(
                rank=rec.rank,
                restaurant_name=rec.restaurant_name,
                score=rec.score,
                explanation=self._truncate_text(rec.explanation, 150),
                highlights=rec.highlights[:2],
                considerations=[],  # No considerations in list view
                cuisine=rec.cuisine,
                rating=rec.rating,
                price_range=rec.price_range,
                avg_cost_for_two=rec.avg_cost_for_two,
                location=rec.location,
                address=None,  # No address in list view
                features=None
            )
            formatted.append(list_rec)
        
        return formatted
    
    def _format_as_table(self, recommendations: List[FormattedRecommendation]) -> List[FormattedRecommendation]:
        """Format recommendations as table rows"""
        formatted = []
        
        for rec in recommendations:
            # Add table-specific formatting
            table_rec = FormattedRecommendation(
                rank=rec.rank,
                restaurant_name=rec.restaurant_name,
                score=rec.score,
                explanation="",  # No explanation in table
                highlights=[],
                considerations=[],
                cuisine=rec.cuisine,
                rating=rec.rating,
                price_range=rec.price_range,
                avg_cost_for_two=rec.avg_cost_for_two,
                location=rec.location,
                address=None,
                features=None
            )
            formatted.append(table_rec)
        
        return formatted
    
    def _format_as_compact(self, recommendations: List[FormattedRecommendation]) -> List[FormattedRecommendation]:
        """Format recommendations as compact items"""
        formatted = []
        
        for rec in recommendations:
            # Add compact-specific formatting
            compact_rec = FormattedRecommendation(
                rank=rec.rank,
                restaurant_name=rec.restaurant_name,
                score=rec.score,
                explanation=self._truncate_text(rec.explanation, 100),
                highlights=rec.highlights[:1],
                considerations=[],
                cuisine=rec.cuisine,
                rating=rec.rating,
                price_range=rec.price_range,
                avg_cost_for_two=rec.avg_cost_for_two,
                location=rec.location,
                address=None,
                features=None
            )
            formatted.append(compact_rec)
        
        return formatted
    
    def _format_as_detailed(self, recommendations: List[FormattedRecommendation]) -> List[FormattedRecommendation]:
        """Format recommendations with full details"""
        return recommendations  # Return as-is for detailed view
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length].rstrip() + "..."
    
    def _create_metadata(self, phase4_result: Dict[str, Any], output_format: OutputFormat) -> Dict[str, Any]:
        """Create metadata for the formatted result"""
        metadata = {
            "format_type": output_format.value,
            "processing_time": phase4_result.get("processing_time"),
            "model_used": phase4_result.get("model_used"),
            "tokens_used": phase4_result.get("tokens_used"),
            "fallback_used": phase4_result.get("fallback_used", False),
            "validation_summary": phase4_result.get("validation_summary", {}),
            "generated_at": self._get_timestamp(),
            "version": "1.0.0"
        }
        
        # Add format-specific metadata
        if output_format == OutputFormat.TABLE:
            metadata["table_columns"] = ["rank", "restaurant_name", "cuisine", "rating", "price_range", "score"]
        elif output_format == OutputFormat.CARD:
            metadata["card_fields"] = ["name", "cuisine", "rating", "price_range", "highlights", "score"]
        
        return metadata
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _create_error_result(self, error_message: str) -> FormattedResult:
        """Create error result"""
        return FormattedResult(
            format_type=OutputFormat.CARD,
            recommendations=[],
            summary="Error occurred during formatting",
            alternatives="Please try again or contact support",
            metadata={"error": error_message},
            success=False,
            total_count=0
        )
    
    def to_json(self, formatted_result: FormattedResult, indent: Optional[int] = 2) -> str:
        """Convert formatted result to JSON string"""
        try:
            # Convert to serializable format
            result_dict = {
                "format_type": formatted_result.format_type.value,
                "success": formatted_result.success,
                "total_count": formatted_result.total_count,
                "summary": formatted_result.summary,
                "alternatives": formatted_result.alternatives,
                "metadata": formatted_result.metadata,
                "recommendations": []
            }
            
            for rec in formatted_result.recommendations:
                rec_dict = {
                    "rank": rec.rank,
                    "restaurant_name": rec.restaurant_name,
                    "score": rec.score,
                    "explanation": rec.explanation,
                    "highlights": rec.highlights,
                    "considerations": rec.considerations,
                    "cuisine": rec.cuisine,
                    "rating": rec.rating,
                    "price_range": rec.price_range,
                    "avg_cost_for_two": rec.avg_cost_for_two,
                    "location": rec.location,
                    "address": rec.address,
                    "features": rec.features
                }
                result_dict["recommendations"].append(rec_dict)
            
            return json.dumps(result_dict, indent=indent, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Error converting to JSON: {str(e)}")
            return json.dumps({"error": str(e)}, indent=indent)
    
    def create_comparison_table(self, recommendations: List[FormattedRecommendation]) -> Dict[str, Any]:
        """Create comparison table for top recommendations"""
        if not recommendations:
            return {"error": "No recommendations available"}
        
        # Take top 3 for comparison
        top_recommendations = recommendations[:3]
        
        comparison = {
            "comparison_type": "top_3_comparison",
            "restaurants": [],
            "comparison_criteria": ["rating", "price", "cuisine", "highlights"],
            "best_for": {}
        }
        
        for rec in top_recommendations:
            restaurant_data = {
                "name": rec.restaurant_name,
                "rank": rec.rank,
                "score": rec.score,
                "rating": rec.rating or 0,
                "price_range": rec.price_range or "Unknown",
                "cuisine": rec.cuisine or "Unknown",
                "avg_cost": rec.avg_cost_for_two or 0,
                "highlights": rec.highlights[:3],
                "key_strength": self._determine_key_strength(rec)
            }
            comparison["restaurants"].append(restaurant_data)
        
        # Add best for recommendations
        comparison["best_for"] = self._determine_best_for(top_recommendations)
        
        return comparison
    
    def _determine_key_strength(self, rec: FormattedRecommendation) -> str:
        """Determine key strength of a restaurant"""
        if rec.rating and rec.rating >= 4.5:
            return "Highest Quality"
        elif rec.price_range == "$":
            return "Most Budget-Friendly"
        elif rec.score >= 0.9:
            return "Best Match"
        elif rec.highlights and len(rec.highlights) >= 3:
            return "Most Features"
        else:
            return "Well-Rounded"
    
    def _determine_best_for(self, recommendations: List[FormattedRecommendation]) -> Dict[str, str]:
        """Determine which restaurant is best for different criteria"""
        best_for = {}
        
        if not recommendations:
            return best_for
        
        # Best rating
        best_rating = max(recommendations, key=lambda x: x.rating or 0)
        best_for["best_rating"] = best_rating.restaurant_name
        
        # Most budget-friendly
        budget_order = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
        most_budget = min(recommendations, key=lambda x: budget_order.get(x.price_range, 5))
        best_for["most_budget_friendly"] = most_budget.restaurant_name
        
        # Highest score
        best_score = max(recommendations, key=lambda x: x.score)
        best_for["best_match"] = best_score.restaurant_name
        
        # Most features
        most_features = max(recommendations, key=lambda x: len(x.highlights) if x.highlights else 0)
        best_for["most_features"] = most_features.restaurant_name
        
        return best_for
