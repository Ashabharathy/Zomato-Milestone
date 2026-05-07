"""
Phase 4 Integration Module: LLM Recommendation and Reasoning Layer
Main integration point for Phase 4 components using Groq LLM.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from prompt_builder import PromptBuilder, UserPreference, Restaurant
from llm_inference import GroqInference, MockGroqInference, create_inference_client
from response_parser import ResponseParser, ParsedResponse
from guardrails import Guardrails, GuardrailResult


@dataclass
class Phase4Config:
    """Configuration for Phase 4 integration"""
    groq_api_key: Optional[str] = None
    groq_model: str = "llama3-70b-8192"
    temperature: float = 0.3
    max_tokens: int = 4096
    top_p: float = 0.9
    timeout: int = 30
    max_retries: int = 3
    strict_validation: bool = False
    use_mock: bool = False


@dataclass
class Phase4Result:
    """Result from Phase 4 processing"""
    success: bool
    recommendations: List[Dict[str, Any]]
    summary: str
    alternatives: str
    processing_time: float
    tokens_used: Optional[int]
    model_used: str
    validation_summary: Dict[str, Any]
    fallback_used: bool
    error_message: Optional[str] = None


class Phase4Integration:
    """Main integration class for Phase 4: LLM Recommendation and Reasoning Layer"""
    
    def __init__(self, config: Phase4Config):
        """
        Initialize Phase 4 integration
        
        Args:
            config: Configuration for Phase 4 components
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.response_parser = ResponseParser()
        self.guardrails = Guardrails(strict_mode=config.strict_validation)
        
        # Initialize LLM inference client
        self.llm_client = create_inference_client(
            api_key=config.groq_api_key,
            model=config.groq_model,
            use_mock=config.use_mock
        )
        
        self.logger.info(f"Phase 4 initialized with model: {config.groq_model}")
    
    def generate_recommendations(
        self, 
        user_preferences: UserPreference, 
        candidate_restaurants: List[Restaurant]
    ) -> Phase4Result:
        """
        Generate personalized restaurant recommendations using LLM
        
        Args:
            user_preferences: User's dining preferences
            candidate_restaurants: Pre-filtered restaurant candidates from Phase 3
            
        Returns:
            Phase4Result with recommendations and metadata
        """
        start_time = time.time()
        
        try:
            # Step 1: Validate inputs
            validation_result = self.prompt_builder.validate_prompt_components(
                user_preferences, candidate_restaurants
            )
            
            if not validation_result["valid"]:
                return Phase4Result(
                    success=False,
                    recommendations=[],
                    summary="Input validation failed",
                    alternatives="Please check your preferences and try again",
                    processing_time=time.time() - start_time,
                    tokens_used=None,
                    model_used=self.config.groq_model,
                    validation_summary={"errors": validation_result["issues"]},
                    fallback_used=True,
                    error_message="Input validation failed: " + "; ".join(validation_result["issues"])
                )
            
            # Step 2: Build prompt
            prompt = self.prompt_builder.build_prompt(user_preferences, candidate_restaurants)
            
            # Step 3: Generate LLM response
            llm_response = self.llm_client.generate_with_retry(
                prompt=prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries
            )
            
            if not llm_response.success:
                return Phase4Result(
                    success=False,
                    recommendations=[],
                    summary="LLM inference failed",
                    alternatives="Please try again later or use fallback recommendations",
                    processing_time=llm_response.response_time or time.time() - start_time,
                    tokens_used=llm_response.tokens_used,
                    model_used=llm_response.model_used,
                    validation_summary={"llm_error": llm_response.error_message},
                    fallback_used=True,
                    error_message=llm_response.error_message
                )
            
            # Step 4: Parse response
            parsed_response = self.response_parser.parse_response(
                llm_response.content, candidate_restaurants
            )
            
            # Step 5: Apply guardrails
            guardrail_result = self.guardrails.validate_and_process_response(
                parsed_response, user_preferences, candidate_restaurants
            )
            
            # Step 6: Format final result
            processing_time = time.time() - start_time
            
            if guardrail_result.is_valid:
                return Phase4Result(
                    success=True,
                    recommendations=guardrail_result.processed_response["recommendations"],
                    summary=guardrail_result.processed_response["summary"],
                    alternatives=guardrail_result.processed_response["alternatives"],
                    processing_time=processing_time,
                    tokens_used=llm_response.tokens_used,
                    model_used=llm_response.model_used,
                    validation_summary=self.guardrails.get_validation_summary(guardrail_result),
                    fallback_used=guardrail_result.fallback_triggered
                )
            else:
                # Fallback response
                return Phase4Result(
                    success=False,
                    recommendations=guardrail_result.processed_response["recommendations"],
                    summary=guardrail_result.processed_response["summary"],
                    alternatives=guardrail_result.processed_response["alternatives"],
                    processing_time=processing_time,
                    tokens_used=llm_response.tokens_used,
                    model_used=llm_response.model_used,
                    validation_summary=self.guardrails.get_validation_summary(guardrail_result),
                    fallback_used=True,
                    error_message="Validation failed, fallback generated"
                )
        
        except Exception as e:
            self.logger.error(f"Unexpected error in Phase 4: {str(e)}")
            return Phase4Result(
                success=False,
                recommendations=[],
                summary="System error occurred",
                alternatives="Please try again or contact support",
                processing_time=time.time() - start_time,
                tokens_used=None,
                model_used=self.config.groq_model,
                validation_summary={"system_error": str(e)},
                fallback_used=True,
                error_message=f"System error: {str(e)}"
            )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all Phase 4 components"""
        try:
            llm_status = self.llm_client.get_model_info()
            connection_test = self.llm_client.test_connection()
        except Exception as e:
            llm_status = {"error": str(e)}
            connection_test = False
        
        return {
            "components": {
                "prompt_builder": "initialized",
                "response_parser": "initialized", 
                "guardrails": f"initialized (strict_mode={self.config.strict_validation})",
                "llm_client": llm_status
            },
            "connection_test": connection_test,
            "config": {
                "model": self.config.groq_model,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "max_retries": self.config.max_retries,
                "use_mock": self.config.use_mock
            }
        }
    
    def update_config(self, **kwargs) -> None:
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config parameter: {key}")
    
    def create_sample_preferences(self) -> UserPreference:
        """Create sample user preferences for testing"""
        return UserPreference(
            location="New York",
            budget_min=20,
            budget_max=100,
            cuisine="Italian",
            min_rating=4.0,
            dietary_constraints=["vegetarian"],
            meal_type="dinner",
            group_size=2
        )
    
    def create_sample_restaurants(self) -> List[Restaurant]:
        """Create sample restaurant data for testing"""
        return [
            Restaurant(
                name="Bella Italia",
                cuisine="Italian",
                location="New York",
                rating=4.5,
                price_range="$$",
                avg_cost_for_two=60,
                address="123 Main St, New York, NY",
                features=["vegetarian options", "outdoor seating"],
                description="Authentic Italian cuisine with modern twist"
            ),
            Restaurant(
                name="Pizza Paradise",
                cuisine="Italian", 
                location="New York",
                rating=4.2,
                price_range="$",
                avg_cost_for_two=35,
                address="456 Oak Ave, New York, NY",
                features=["delivery", "takeout"],
                description="Traditional pizza and pasta dishes"
            ),
            Restaurant(
                name="Garden Bistro",
                cuisine="American",
                location="New York", 
                rating=4.7,
                price_range="$$$",
                avg_cost_for_two=80,
                address="789 Park Rd, New York, NY",
                features=["vegetarian-friendly", "wine bar"],
                description="Farm-to-table American cuisine"
            )
        ]


def create_phase4_integration(
    groq_api_key: Optional[str] = None,
    model: str = "llama3-70b-8192",
    strict_validation: bool = False,
    use_mock: bool = False,
    **kwargs
) -> Phase4Integration:
    """
    Factory function to create Phase 4 integration
    
    Args:
        groq_api_key: Groq API key (if None, will use environment variable)
        model: Groq model to use
        strict_validation: Whether to use strict validation mode
        use_mock: Whether to use mock client for testing
        **kwargs: Additional configuration parameters
        
    Returns:
        Configured Phase4Integration instance
    """
    config = Phase4Config(
        groq_api_key=groq_api_key,
        groq_model=model,
        strict_validation=strict_validation,
        use_mock=use_mock,
        **kwargs
    )
    
    return Phase4Integration(config)


# Example usage function
def example_usage():
    """Example of how to use Phase 4 integration"""
    import os
    
    # Create integration (use mock for example)
    phase4 = create_phase4_integration(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192",
        use_mock=True  # Set to False to use real Groq API
    )
    
    # Get system status
    status = phase4.get_system_status()
    print("System Status:", status)
    
    # Create sample data
    preferences = phase4.create_sample_preferences()
    restaurants = phase4.create_sample_restaurants()
    
    # Generate recommendations
    result = phase4.generate_recommendations(preferences, restaurants)
    
    print(f"Success: {result.success}")
    print(f"Fallback used: {result.fallback_used}")
    print(f"Processing time: {result.processing_time:.2f}s")
    print(f"Model used: {result.model_used}")
    
    if result.success:
        print("\nRecommendations:")
        for rec in result.recommendations:
            print(f"{rec['rank']}. {rec['restaurant_name']} (Score: {rec['score']:.2f})")
            print(f"   {rec['explanation']}")
        
        print(f"\nSummary: {result.summary}")
        print(f"Alternatives: {result.alternatives}")
    else:
        print(f"Error: {result.error_message}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run example
    example_usage()
