"""
Prompt Builder Module for Phase 4: LLM Recommendation and Reasoning Layer
Builds structured prompts with context and instruction templates for Groq LLM.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class UserPreference:
    """Structured user preference object"""
    location: str
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    cuisine: Optional[str] = None
    min_rating: Optional[float] = None
    dietary_constraints: Optional[List[str]] = None
    meal_type: Optional[str] = None
    group_size: Optional[int] = None


@dataclass
class Restaurant:
    """Restaurant data structure"""
    name: str
    cuisine: str
    location: str
    rating: float
    price_range: str
    avg_cost_for_two: Optional[float] = None
    address: Optional[str] = None
    features: Optional[List[str]] = None
    description: Optional[str] = None


class PromptBuilder:
    """Builds structured prompts for LLM recommendation generation"""
    
    def __init__(self):
        self.system_prompt = self._get_system_prompt()
        self.user_instruction_template = self._get_user_instruction_template()
    
    def _get_system_prompt(self) -> str:
        """System prompt for the LLM"""
        return """You are an expert restaurant recommendation assistant with deep knowledge of cuisines, dining experiences, and local food scenes. Your task is to provide personalized restaurant recommendations with detailed, helpful explanations.

Key responsibilities:
1. Analyze user preferences and restaurant options carefully
2. Rank restaurants based on how well they match user needs
3. Provide clear, specific explanations for each recommendation
4. Consider factors like cuisine preferences, budget, ratings, location, and special requirements
5. Be honest about limitations or trade-offs
6. Maintain a helpful, professional tone

Always structure your response as valid JSON with the following format:
{
    "recommendations": [
        {
            "rank": 1,
            "restaurant_name": "Restaurant Name",
            "score": 0.95,
            "explanation": "Detailed explanation of why this restaurant is recommended...",
            "highlights": ["Key highlight 1", "Key highlight 2"],
            "considerations": ["Any considerations or warnings"]
        }
    ],
    "summary": "Brief summary of the recommendations",
    "alternatives": "Suggestion for alternatives if none are perfect matches"
}"""
    
    def _get_user_instruction_template(self) -> str:
        """Template for user-specific instructions"""
        return """Based on the following user preferences and restaurant candidates, please provide personalized recommendations with detailed explanations.

USER PREFERENCES:
{user_preferences}

CANDIDATE RESTAURANTS:
{restaurant_candidates}

Please analyze these options and provide your recommendations in the specified JSON format. Focus on:
1. How well each restaurant matches the user's specific preferences
2. The quality and uniqueness of the dining experience
3. Value for money and suitability for the occasion
4. Any special features or considerations

Rank the restaurants from most to least suitable for this user."""
    
    def format_user_preferences(self, preferences: UserPreference) -> str:
        """Format user preferences for the prompt"""
        pref_dict = {
            "location": preferences.location,
            "budget_range": f"${preferences.budget_min or 'any'} - ${preferences.budget_max or 'any'}",
            "cuisine_preference": preferences.cuisine or "No specific preference",
            "minimum_rating": preferences.min_rating or "No minimum",
            "dietary_constraints": preferences.dietary_constraints or [],
            "meal_type": preferences.meal_type or "Not specified",
            "group_size": preferences.group_size or "Not specified"
        }
        
        return json.dumps(pref_dict, indent=2)
    
    def format_restaurant_candidates(self, restaurants: List[Restaurant]) -> str:
        """Format restaurant candidates for the prompt"""
        candidates = []
        
        for i, restaurant in enumerate(restaurants, 1):
            candidate = {
                "id": i,
                "name": restaurant.name,
                "cuisine": restaurant.cuisine,
                "location": restaurant.location,
                "rating": restaurant.rating,
                "price_range": restaurant.price_range,
                "avg_cost_for_two": restaurant.avg_cost_for_two,
                "address": restaurant.address,
                "features": restaurant.features or [],
                "description": restaurant.description or "No description available"
            }
            candidates.append(candidate)
        
        return json.dumps(candidates, indent=2)
    
    def build_prompt(self, preferences: UserPreference, restaurants: List[Restaurant]) -> str:
        """Build the complete prompt for LLM inference"""
        
        # Format components
        formatted_preferences = self.format_user_preferences(preferences)
        formatted_restaurants = self.format_restaurant_candidates(restaurants)
        
        # Build user instruction
        user_instruction = self.user_instruction_template.format(
            user_preferences=formatted_preferences,
            restaurant_candidates=formatted_restaurants
        )
        
        # Combine system prompt and user instruction
        full_prompt = f"{self.system_prompt}\n\n{user_instruction}"
        
        return full_prompt
    
    def build_fallback_prompt(self, preferences: UserPreference, restaurants: List[Restaurant]) -> str:
        """Build a simplified prompt for fallback scenarios"""
        return f"""You are a restaurant recommendation assistant. 

User preferences:
- Location: {preferences.location}
- Budget: ${preferences.budget_min or 'any'} - ${preferences.budget_max or 'any'}
- Cuisine: {preferences.cuisine or 'any'}
- Min rating: {preferences.min_rating or 'any'}

Available restaurants:
{[f"{r.name} ({r.cuisine}, {r.rating} stars, {r.price_range})" for r in restaurants[:5]]}

Please rank these restaurants 1-5 and briefly explain why each is suitable for the user. Return as JSON with rankings and explanations."""
    
    def validate_prompt_components(self, preferences: UserPreference, restaurants: List[Restaurant]) -> Dict[str, Any]:
        """Validate prompt components before building"""
        validation_result = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check preferences
        if not preferences.location:
            validation_result["issues"].append("Location is required")
            validation_result["valid"] = False
        
        # Check restaurants
        if not restaurants:
            validation_result["issues"].append("No restaurant candidates provided")
            validation_result["valid"] = False
        
        if len(restaurants) > 20:
            validation_result["warnings"].append("Too many restaurants may affect LLM performance")
        
        if len(restaurants) < 3:
            validation_result["warnings"].append("Fewer than 3 restaurants may limit recommendation quality")
        
        return validation_result
