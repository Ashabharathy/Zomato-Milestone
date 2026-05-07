"""
Summary Generator Module for Phase 5: Response Assembly and Presentation Layer
Generates quick comparisons and summaries between top restaurant options.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

from .result_formatter import FormattedRecommendation


class SummaryType(Enum):
    """Types of summaries"""
    QUICK_COMPARISON = "quick_comparison"
    DETAILED_ANALYSIS = "detailed_analysis"
    BEST_FOR = "best_for"
    PRICE_COMPARISON = "price_comparison"
    FEATURE_COMPARISON = "feature_comparison"


@dataclass
class ComparisonPoint:
    """Individual comparison point"""
    restaurant: str
    rank: int
    score: float
    value: Any
    description: str


@dataclass
class SummaryResult:
    """Generated summary result"""
    summary_type: SummaryType
    title: str
    content: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]


class SummaryGenerator:
    """Generates summaries and comparisons for restaurant recommendations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_summary(
        self, 
        recommendations: List[FormattedRecommendation],
        summary_type: SummaryType = SummaryType.QUICK_COMPARISON,
        max_items: int = 3
    ) -> SummaryResult:
        """
        Generate summary for recommendations
        
        Args:
            recommendations: List of formatted recommendations
            summary_type: Type of summary to generate
            max_items: Maximum number of items to include in comparison
            
        Returns:
            SummaryResult with generated summary
        """
        try:
            if not recommendations:
                return self._create_empty_summary(summary_type)
            
            # Limit recommendations for analysis
            top_recommendations = recommendations[:max_items]
            
            # Route to appropriate generator
            if summary_type == SummaryType.QUICK_COMPARISON:
                return self._generate_quick_comparison(top_recommendations)
            elif summary_type == SummaryType.DETAILED_ANALYSIS:
                return self._generate_detailed_analysis(top_recommendations)
            elif summary_type == SummaryType.BEST_FOR:
                return self._generate_best_for_summary(top_recommendations)
            elif summary_type == SummaryType.PRICE_COMPARISON:
                return self._generate_price_comparison(top_recommendations)
            elif summary_type == SummaryType.FEATURE_COMPARISON:
                return self._generate_feature_comparison(top_recommendations)
            else:
                return self._generate_quick_comparison(top_recommendations)
                
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return self._create_error_summary(str(e), summary_type)
    
    def _generate_quick_comparison(self, recommendations: List[FormattedRecommendation]) -> SummaryResult:
        """Generate quick comparison between top recommendations"""
        content = {
            "comparison_type": "quick_comparison",
            "restaurants": [],
            "key_metrics": ["rating", "price", "score", "highlights"],
            "winner": None
        }
        
        # Build comparison data
        for rec in recommendations:
            restaurant_data = {
                "name": rec.restaurant_name,
                "rank": rec.rank,
                "score": rec.score,
                "rating": rec.rating or 0,
                "price_range": rec.price_range or "Unknown",
                "cuisine": rec.cuisine or "Unknown",
                "highlights": rec.highlights[:3],
                "key_strength": self._determine_key_strength(rec)
            }
            content["restaurants"].append(restaurant_data)
        
        # Determine winner
        if content["restaurants"]:
            content["winner"] = max(content["restaurants"], key=lambda x: x["score"])
        
        # Generate insights
        insights = self._generate_comparison_insights(content["restaurants"])
        
        # Generate recommendations
        recommendations_text = self._generate_recommendation_text(content["restaurants"])
        
        return SummaryResult(
            summary_type=SummaryType.QUICK_COMPARISON,
            title="Quick Comparison of Top Restaurants",
            content=content,
            insights=insights,
            recommendations=recommendations_text,
            metadata={
                "items_compared": len(recommendations),
                "generated_at": self._get_timestamp()
            }
        )
    
    def _generate_detailed_analysis(self, recommendations: List[FormattedRecommendation]) -> SummaryResult:
        """Generate detailed analysis of recommendations"""
        content = {
            "analysis_type": "detailed_analysis",
            "restaurants": [],
            "comparative_analysis": {},
            "pros_cons": {},
            "decision_factors": {}
        }
        
        # Build detailed analysis
        for rec in recommendations:
            restaurant_data = {
                "name": rec.restaurant_name,
                "rank": rec.rank,
                "score": rec.score,
                "rating": rec.rating or 0,
                "price_range": rec.price_range or "Unknown",
                "cuisine": rec.cuisine or "Unknown",
                "avg_cost": rec.avg_cost_for_two or 0,
                "highlights": rec.highlights,
                "considerations": rec.considerations,
                "explanation": rec.explanation,
                "features": rec.features or []
            }
            content["restaurants"].append(restaurant_data)
        
        # Comparative analysis
        content["comparative_analysis"] = self._perform_comparative_analysis(content["restaurants"])
        
        # Pros and cons
        content["pros_cons"] = self._generate_pros_cons(content["restaurants"])
        
        # Decision factors
        content["decision_factors"] = self._analyze_decision_factors(content["restaurants"])
        
        # Generate insights
        insights = self._generate_detailed_insights(content)
        
        # Generate recommendations
        recommendations_text = self._generate_detailed_recommendations(content)
        
        return SummaryResult(
            summary_type=SummaryType.DETAILED_ANALYSIS,
            title="Detailed Analysis of Restaurant Options",
            content=content,
            insights=insights,
            recommendations=recommendations_text,
            metadata={
                "items_analyzed": len(recommendations),
                "analysis_depth": "comprehensive",
                "generated_at": self._get_timestamp()
            }
        )
    
    def _generate_best_for_summary(self, recommendations: List[FormattedRecommendation]) -> SummaryResult:
        """Generate 'best for' recommendations"""
        content = {
            "best_for_categories": {},
            "category_winners": {},
            "overall_winner": None
        }
        
        # Define categories
        categories = {
            "best_quality": lambda r: r.rating or 0,
            "best_value": lambda r: self._calculate_value_score(r),
            "best_match": lambda r: r.score,
            "most_features": lambda r: len(r.highlights) if r.highlights else 0,
            "most_budget_friendly": lambda r: self._price_to_number(r.price_range or "$$$$")
        }
        
        # Find winners for each category
        for category, scorer in categories.items():
            if recommendations:
                winner = max(recommendations, key=scorer)
                content["category_winners"][category] = {
                    "restaurant": winner.restaurant_name,
                    "value": scorer(winner),
                    "reason": self._get_category_reason(category, winner)
                }
        
        # Overall winner (highest score)
        if recommendations:
            overall_winner = max(recommendations, key=lambda r: r.score)
            content["overall_winner"] = {
                "restaurant": overall_winner.restaurant_name,
                "score": overall_winner.score,
                "reason": "Highest overall match score"
            }
        
        # Generate insights
        insights = self._generate_best_for_insights(content)
        
        # Generate recommendations
        recommendations_text = self._generate_best_for_recommendations(content)
        
        return SummaryResult(
            summary_type=SummaryType.BEST_FOR,
            title="Best Restaurant for Different Needs",
            content=content,
            insights=insights,
            recommendations=recommendations_text,
            metadata={
                "categories_analyzed": len(categories),
                "items_considered": len(recommendations),
                "generated_at": self._get_timestamp()
            }
        )
    
    def _generate_price_comparison(self, recommendations: List[FormattedRecommendation]) -> SummaryResult:
        """Generate price-focused comparison"""
        content = {
            "price_comparison": {},
            "value_analysis": {},
            "budget_recommendations": {}
        }
        
        # Sort by price
        price_order = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
        sorted_by_price = sorted(
            recommendations, 
            key=lambda r: price_order.get(r.price_range or "$$$$", 5)
        )
        
        content["price_comparison"] = {
            "most_affordable": {
                "restaurant": sorted_by_price[0].restaurant_name if sorted_by_price else None,
                "price_range": sorted_by_price[0].price_range if sorted_by_price else None,
                "avg_cost": sorted_by_price[0].avg_cost_for_two if sorted_by_price else 0
            },
            "most_expensive": {
                "restaurant": sorted_by_price[-1].restaurant_name if sorted_by_price else None,
                "price_range": sorted_by_price[-1].price_range if sorted_by_price else None,
                "avg_cost": sorted_by_price[-1].avg_cost_for_two if sorted_by_price else 0
            },
            "price_range_list": [
                {
                    "restaurant": rec.restaurant_name,
                    "price_range": rec.price_range,
                    "avg_cost": rec.avg_cost_for_two,
                    "value_score": self._calculate_value_score(rec)
                }
                for rec in recommendations
            ]
        }
        
        # Value analysis
        content["value_analysis"] = self._analyze_value_for_money(recommendations)
        
        # Budget recommendations
        content["budget_recommendations"] = self._generate_budget_recommendations(recommendations)
        
        # Generate insights
        insights = self._generate_price_insights(content)
        
        # Generate recommendations
        recommendations_text = self._generate_price_recommendations_text(content)
        
        return SummaryResult(
            summary_type=SummaryType.PRICE_COMPARISON,
            title="Price and Value Comparison",
            content=content,
            insights=insights,
            recommendations=recommendations_text,
            metadata={
                "price_ranges_analyzed": len(set(r.price_range for r in recommendations if r.price_range)),
                "items_compared": len(recommendations),
                "generated_at": self._get_timestamp()
            }
        )
    
    def _generate_feature_comparison(self, recommendations: List[FormattedRecommendation]) -> SummaryResult:
        """Generate feature-focused comparison"""
        content = {
            "feature_analysis": {},
            "unique_features": {},
            "common_features": [],
            "feature_matrix": {}
        }
        
        # Collect all features
        all_features = set()
        restaurant_features = {}
        
        for rec in recommendations:
            features = set(rec.highlights + (rec.features or []))
            restaurant_features[rec.restaurant_name] = features
            all_features.update(features)
        
        # Build feature matrix
        for feature in all_features:
            content["feature_matrix"][feature] = {
                "restaurants": [
                    rec.restaurant_name 
                    for rec in recommendations 
                    if feature in (rec.highlights + (rec.features or []))
                ],
                "count": sum(
                    1 for rec in recommendations 
                    if feature in (rec.highlights + (rec.features or []))
                )
            }
        
        # Find unique and common features
        for rec in recommendations:
            features = restaurant_features[rec.restaurant_name]
            unique = features - set().union(*[restaurant_features[r] for r in restaurant_features if r != rec.restaurant_name])
            if unique:
                content["unique_features"][rec.restaurant_name] = list(unique)
        
        # Common features (present in all restaurants)
        if restaurant_features:
            common_features = set.intersection(*[set(f) for f in restaurant_features.values()])
            content["common_features"] = list(common_features)
        
        # Feature analysis
        content["feature_analysis"] = self._analyze_features(content["feature_matrix"])
        
        # Generate insights
        insights = self._generate_feature_insights(content)
        
        # Generate recommendations
        recommendations_text = self._generate_feature_recommendations(content)
        
        return SummaryResult(
            summary_type=SummaryType.FEATURE_COMPARISON,
            title="Feature Comparison Analysis",
            content=content,
            insights=insights,
            recommendations=recommendations_text,
            metadata={
                "total_features": len(all_features),
                "restaurants_analyzed": len(recommendations),
                "common_features": len(content["common_features"]),
                "generated_at": self._get_timestamp()
            }
        )
    
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
    
    def _calculate_value_score(self, rec: FormattedRecommendation) -> float:
        """Calculate value for money score"""
        rating = rec.rating or 0
        price_factor = self._price_to_number(rec.price_range or "$$$$")
        return rating / price_factor if price_factor > 0 else 0
    
    def _price_to_number(self, price_range: str) -> int:
        """Convert price range to number"""
        price_map = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}
        return price_map.get(price_range, 4)
    
    def _generate_comparison_insights(self, restaurants: List[Dict[str, Any]]) -> List[str]:
        """Generate insights for quick comparison"""
        insights = []
        
        if not restaurants:
            return insights
        
        # Rating insights
        ratings = [r["rating"] for r in restaurants if r["rating"] > 0]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            insights.append(f"Average rating: {avg_rating:.1f} stars")
            best_rating = max(ratings)
            insights.append(f"Highest rated: {best_rating:.1f} stars")
        
        # Price insights
        price_ranges = [r["price_range"] for r in restaurants if r["price_range"] != "Unknown"]
        if price_ranges:
            insights.append(f"Price range: {min(price_ranges)} - {max(price_ranges)}")
        
        # Score insights
        scores = [r["score"] for r in restaurants]
        if scores:
            avg_score = sum(scores) / len(scores)
            insights.append(f"Average match score: {avg_score:.2f}")
        
        # Cuisine diversity
        cuisines = [r["cuisine"] for r in restaurants if r["cuisine"] != "Unknown"]
        if len(set(cuisines)) > 1:
            insights.append(f"Diverse cuisine options: {', '.join(set(cuisines))}")
        
        return insights
    
    def _generate_recommendation_text(self, restaurants: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendation text"""
        recommendations = []
        
        if not restaurants:
            return recommendations
        
        # Top recommendation
        winner = max(restaurants, key=lambda x: x["score"])
        recommendations.append(f"Best overall match: {winner['name']} (Score: {winner['score']:.2f})")
        
        # Budget recommendation
        budget_friendly = min(restaurants, key=lambda x: self._price_to_number(x["price_range"]))
        recommendations.append(f"Most budget-friendly: {budget_friendly['name']} ({budget_friendly['price_range']})")
        
        # Quality recommendation
        best_quality = max(restaurants, key=lambda x: x["rating"])
        recommendations.append(f"Highest quality: {best_quality['name']} ({best_quality['rating']} stars)")
        
        return recommendations
    
    def _perform_comparative_analysis(self, restaurants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comparative analysis"""
        analysis = {}
        
        # Rating comparison
        ratings = [r["rating"] for r in restaurants if r["rating"] > 0]
        if ratings:
            analysis["rating_analysis"] = {
                "highest": max(ratings),
                "lowest": min(ratings),
                "average": sum(ratings) / len(ratings),
                "spread": max(ratings) - min(ratings)
            }
        
        # Price comparison
        avg_costs = [r["avg_cost"] for r in restaurants if r["avg_cost"] > 0]
        if avg_costs:
            analysis["price_analysis"] = {
                "highest": max(avg_costs),
                "lowest": min(avg_costs),
                "average": sum(avg_costs) / len(avg_costs),
                "spread": max(avg_costs) - min(avg_costs)
            }
        
        # Score comparison
        scores = [r["score"] for r in restaurants]
        analysis["score_analysis"] = {
            "highest": max(scores),
            "lowest": min(scores),
            "average": sum(scores) / len(scores),
            "spread": max(scores) - min(scores)
        }
        
        return analysis
    
    def _generate_pros_cons(self, restaurants: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[str]]]:
        """Generate pros and cons for each restaurant"""
        pros_cons = {}
        
        for restaurant in restaurants:
            pros = []
            cons = []
            
            # Pros based on attributes
            if restaurant["rating"] >= 4.5:
                pros.append("Excellent rating")
            elif restaurant["rating"] >= 4.0:
                pros.append("Good rating")
            
            if restaurant["price_range"] in ["$", "$$"]:
                pros.append("Affordable")
            
            if len(restaurant["highlights"]) >= 3:
                pros.append("Many features/highlights")
            
            if restaurant["score"] >= 0.8:
                pros.append("High match score")
            
            # Cons based on attributes
            if restaurant["rating"] < 4.0:
                cons.append("Lower rating")
            
            if restaurant["price_range"] in ["$$$", "$$$$"]:
                cons.append("Expensive")
            
            if restaurant["considerations"]:
                cons.extend(restaurant["considerations"])
            
            pros_cons[restaurant["name"]] = {
                "pros": pros,
                "cons": cons
            }
        
        return pros_cons
    
    def _analyze_decision_factors(self, restaurants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze decision factors"""
        factors = {}
        
        # Rating importance
        ratings = [r["rating"] for r in restaurants if r["rating"] > 0]
        if ratings and max(ratings) - min(ratings) > 0.5:
            factors["rating_importance"] = "high"
        else:
            factors["rating_importance"] = "low"
        
        # Price importance
        avg_costs = [r["avg_cost"] for r in restaurants if r["avg_cost"] > 0]
        if avg_costs and max(avg_costs) / min(avg_costs) > 2:
            factors["price_importance"] = "high"
        else:
            factors["price_importance"] = "low"
        
        # Score spread
        scores = [r["score"] for r in restaurants]
        if max(scores) - min(scores) > 0.2:
            factors["score_discrimination"] = "high"
        else:
            factors["score_discrimination"] = "low"
        
        return factors
    
    def _generate_detailed_insights(self, content: Dict[str, Any]) -> List[str]:
        """Generate detailed insights"""
        insights = []
        
        if "comparative_analysis" in content:
            analysis = content["comparative_analysis"]
            
            if "rating_analysis" in analysis:
                rating_analysis = analysis["rating_analysis"]
                insights.append(f"Rating spread: {rating_analysis['spread']:.1f} stars")
            
            if "price_analysis" in analysis:
                price_analysis = analysis["price_analysis"]
                insights.append(f"Price range: ${price_analysis['lowest']:.0f} - ${price_analysis['highest']:.0f}")
        
        if "decision_factors" in content:
            factors = content["decision_factors"]
            if factors.get("rating_importance") == "high":
                insights.append("Rating is a key differentiator")
            if factors.get("price_importance") == "high":
                insights.append("Price varies significantly between options")
        
        return insights
    
    def _generate_detailed_recommendations(self, content: Dict[str, Any]) -> List[str]:
        """Generate detailed recommendations"""
        recommendations = []
        
        restaurants = content.get("restaurants", [])
        if not restaurants:
            return recommendations
        
        # Overall best
        best_restaurant = max(restaurants, key=lambda x: x["score"])
        recommendations.append(
            f"Best overall: {best_restaurant['name']} - "
            f"Score: {best_restaurant['score']:.2f}, Rating: {best_restaurant['rating']}"
        )
        
        # Best value
        best_value = max(restaurants, key=lambda x: self._calculate_value_score(
            type('obj', (object,), {
                'rating': x['rating'], 
                'price_range': x['price_range']
            })()
        ))
        recommendations.append(f"Best value: {best_value['name']}")
        
        return recommendations
    
    def _get_category_reason(self, category: str, restaurant: FormattedRecommendation) -> str:
        """Get reason for category win"""
        reasons = {
            "best_quality": f"Excellent rating of {restaurant.rating} stars",
            "best_value": f"Great combination of quality and price",
            "best_match": f"Highest match score of {restaurant.score:.2f}",
            "most_features": f"Most features/highlights ({len(restaurant.highlights) if restaurant.highlights else 0})",
            "most_budget_friendly": f"Most affordable at {restaurant.price_range}"
        }
        return reasons.get(category, "Top performer in this category")
    
    def _generate_best_for_insights(self, content: Dict[str, Any]) -> List[str]:
        """Generate insights for best-for summary"""
        insights = []
        
        category_winners = content.get("category_winners", {})
        if category_winners:
            winners = list(category_winners.values())
            winner_names = [w["restaurant"] for w in winners]
            
            # Count wins per restaurant
            win_counts = {}
            for winner_name in winner_names:
                win_counts[winner_name] = win_counts.get(winner_name, 0) + 1
            
            # Find most versatile
            if win_counts:
                most_versatile = max(win_counts, key=win_counts.get)
                insights.append(f"Most versatile: {most_versatile} ({win_counts[most_versatile]} categories)")
        
        return insights
    
    def _generate_best_for_recommendations(self, content: Dict[str, Any]) -> List[str]:
        """Generate recommendations for best-for summary"""
        recommendations = []
        
        overall_winner = content.get("overall_winner")
        if overall_winner:
            recommendations.append(f"Overall best: {overall_winner['restaurant']}")
        
        category_winners = content.get("category_winners", {})
        if "best_quality" in category_winners:
            recommendations.append(f"For quality: {category_winners['best_quality']['restaurant']}")
        if "best_value" in category_winners:
            recommendations.append(f"For value: {category_winners['best_value']['restaurant']}")
        
        return recommendations
    
    def _analyze_value_for_money(self, recommendations: List[FormattedRecommendation]) -> Dict[str, Any]:
        """Analyze value for money"""
        value_scores = []
        
        for rec in recommendations:
            value_score = self._calculate_value_score(rec)
            value_scores.append({
                "restaurant": rec.restaurant_name,
                "value_score": value_score,
                "rating": rec.rating or 0,
                "price_range": rec.price_range or "Unknown"
            })
        
        # Sort by value score
        value_scores.sort(key=lambda x: x["value_score"], reverse=True)
        
        return {
            "rankings": value_scores,
            "best_value": value_scores[0] if value_scores else None,
            "average_value": sum(v["value_score"] for v in value_scores) / len(value_scores) if value_scores else 0
        }
    
    def _generate_budget_recommendations(self, recommendations: List[FormattedRecommendation]) -> Dict[str, Any]:
        """Generate budget-based recommendations"""
        budget_recs = {}
        
        # By price range
        for price_range in ["$", "$$", "$$$", "$$$$"]:
            in_range = [r for r in recommendations if r.price_range == price_range]
            if in_range:
                budget_recs[price_range] = {
                    "best_option": max(in_range, key=lambda x: x.score).restaurant_name,
                    "count": len(in_range)
                }
        
        return budget_recs
    
    def _generate_price_insights(self, content: Dict[str, Any]) -> List[str]:
        """Generate price-related insights"""
        insights = []
        
        price_comparison = content.get("price_comparison", {})
        if "most_affordable" in price_comparison and "most_expensive" in price_comparison:
            most_affordable = price_comparison["most_affordable"]
            most_expensive = price_comparison["most_expensive"]
            
            if most_affordable["restaurant"] and most_expensive["restaurant"]:
                insights.append(f"Price range: {most_affordable['price_range']} - {most_expensive['price_range']}")
                
                if most_affordable["avg_cost"] and most_expensive["avg_cost"]:
                    price_diff = most_expensive["avg_cost"] - most_affordable["avg_cost"]
                    insights.append(f"Price difference: ${price_diff:.0f}")
        
        value_analysis = content.get("value_analysis", {})
        if "best_value" in value_analysis and value_analysis["best_value"]:
            best_value = value_analysis["best_value"]
            insights.append(f"Best value: {best_value['restaurant']}")
        
        return insights
    
    def _generate_price_recommendations_text(self, content: Dict[str, Any]) -> List[str]:
        """Generate price-focused recommendations"""
        recommendations = []
        
        price_comparison = content.get("price_comparison", {})
        if "most_affordable" in price_comparison:
            affordable = price_comparison["most_affordable"]
            if affordable["restaurant"]:
                recommendations.append(f"Most budget-friendly: {affordable['restaurant']}")
        
        value_analysis = content.get("value_analysis", {})
        if "best_value" in value_analysis and value_analysis["best_value"]:
            best_value = value_analysis["best_value"]
            recommendations.append(f"Best value for money: {best_value['restaurant']}")
        
        return recommendations
    
    def _analyze_features(self, feature_matrix: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature distribution"""
        analysis = {
            "most_common": [],
            "least_common": [],
            "unique_features": []
        }
        
        # Sort features by frequency
        feature_counts = [(feature, data["count"]) for feature, data in feature_matrix.items()]
        feature_counts.sort(key=lambda x: x[1], reverse=True)
        
        # Most common (present in multiple restaurants)
        analysis["most_common"] = [
            {"feature": feature, "count": count}
            for feature, count in feature_counts[:5] if count > 1
        ]
        
        # Least common (present in only one restaurant)
        analysis["least_common"] = [
            {"feature": feature, "count": count}
            for feature, count in feature_counts if count == 1
        ]
        
        return analysis
    
    def _generate_feature_insights(self, content: Dict[str, Any]) -> List[str]:
        """Generate feature-related insights"""
        insights = []
        
        feature_analysis = content.get("feature_analysis", {})
        most_common = feature_analysis.get("most_common", [])
        
        if most_common:
            top_feature = most_common[0]
            insights.append(f"Most common feature: {top_feature['feature']} ({top_feature['count']} restaurants)")
        
        unique_features = content.get("unique_features", {})
        if unique_features:
            total_unique = sum(len(features) for features in unique_features.values())
            insights.append(f"Total unique features: {total_unique}")
        
        common_features = content.get("common_features", [])
        if common_features:
            insights.append(f"Common to all: {', '.join(common_features)}")
        
        return insights
    
    def _generate_feature_recommendations(self, content: Dict[str, Any]) -> List[str]:
        """Generate feature-based recommendations"""
        recommendations = []
        
        feature_analysis = content.get("feature_analysis", {})
        most_common = feature_analysis.get("most_common", [])
        
        if most_common:
            top_feature = most_common[0]
            restaurants_with_feature = content["feature_matrix"][top_feature["feature"]]["restaurants"]
            recommendations.append(f"For {top_feature['feature']}: {', '.join(restaurants_with_feature)}")
        
        unique_features = content.get("unique_features", {})
        for restaurant, features in unique_features.items():
            if features:
                recommendations.append(f"Unique to {restaurant}: {', '.join(features)}")
        
        return recommendations
    
    def _create_empty_summary(self, summary_type: SummaryType) -> SummaryResult:
        """Create empty summary result"""
        return SummaryResult(
            summary_type=summary_type,
            title="No Data Available",
            content={},
            insights=["No recommendations available for analysis"],
            recommendations=["Please provide restaurant recommendations to generate summary"],
            metadata={"error": "no_data", "generated_at": self._get_timestamp()}
        )
    
    def _create_error_summary(self, error_message: str, summary_type: SummaryType) -> SummaryResult:
        """Create error summary result"""
        return SummaryResult(
            summary_type=summary_type,
            title="Error Generating Summary",
            content={},
            insights=[f"Error: {error_message}"],
            recommendations=["Please try again with valid recommendation data"],
            metadata={"error": error_message, "generated_at": self._get_timestamp()}
        )
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
