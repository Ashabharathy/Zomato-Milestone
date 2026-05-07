"""
Example Usage Script for Phase 4: LLM Recommendation and Reasoning Layer
Demonstrates how to use the Phase 4 integration with Groq API.
"""

import os
import logging
from dotenv import load_dotenv

from phase4_integration import create_phase4_integration
from prompt_builder import UserPreference, Restaurant

# Load environment variables from .env file in the same directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_sample_user_preferences() -> UserPreference:
    """Create sample user preferences for demonstration"""
    return UserPreference(
        location="New York",
        budget_min=30,
        budget_max=150,
        cuisine="Italian",
        min_rating=4.0,
        dietary_constraints=["vegetarian"],
        meal_type="dinner",
        group_size=2
    )


def create_sample_restaurants() -> list[Restaurant]:
    """Create sample restaurant candidates for demonstration"""
    return [
        Restaurant(
            name="Bella Italia",
            cuisine="Italian",
            location="New York",
            rating=4.5,
            price_range="$$",
            avg_cost_for_two=60,
            address="123 Main St, New York, NY",
            features=["vegetarian options", "outdoor seating", "wine bar"],
            description="Authentic Italian cuisine with modern twist and farm-to-table ingredients"
        ),
        Restaurant(
            name="Pizza Paradise",
            cuisine="Italian", 
            location="New York",
            rating=4.2,
            price_range="$",
            avg_cost_for_two=35,
            address="456 Oak Ave, New York, NY",
            features=["delivery", "takeout", "family-friendly"],
            description="Traditional pizza and pasta dishes with casual atmosphere"
        ),
        Restaurant(
            name="Garden Bistro",
            cuisine="American",
            location="New York", 
            rating=4.7,
            price_range="$$$",
            avg_cost_for_two=80,
            address="789 Park Rd, New York, NY",
            features=["vegetarian-friendly", "wine bar", "reservations recommended"],
            description="Farm-to-table American cuisine with seasonal menu"
        ),
        Restaurant(
            name="Sushi Master",
            cuisine="Japanese",
            location="New York",
            rating=4.8,
            price_range="$$$$",
            avg_cost_for_two=120,
            address="321 Broadway, New York, NY",
            features=["omakase", "sushi bar", "intimate setting"],
            description="Authentic Japanese sushi and omakase experience"
        ),
        Restaurant(
            name="The Green Fork",
            cuisine="Vegetarian",
            location="New York",
            rating=4.4,
            price_range="$$",
            avg_cost_for_two=50,
            address="555 Elm St, New York, NY",
            features=["vegan options", "organic", "gluten-free options"],
            description="Plant-based cuisine with creative vegetarian and vegan dishes"
        )
    ]


def print_recommendations(result):
    """Print formatted recommendations"""
    print("=" * 80)
    print("RESTAURANT RECOMMENDATIONS")
    print("=" * 80)
    
    print(f"Success: {result.success}")
    print(f"Fallback Used: {result.fallback_used}")
    print(f"Processing Time: {result.processing_time:.2f} seconds")
    print(f"Model Used: {result.model_used}")
    
    if result.tokens_used:
        print(f"Tokens Used: {result.tokens_used}")
    
    print("\n" + "-" * 80)
    print("RECOMMENDATIONS")
    print("-" * 80)
    
    for rec in result.recommendations:
        print(f"\n{rec['rank']}. {rec['restaurant_name']} (Score: {rec['score']:.2f})")
        print(f"   Explanation: {rec['explanation']}")
        
        if rec['highlights']:
            print(f"   Highlights: {', '.join(rec['highlights'])}")
        
        if rec['considerations']:
            print(f"   Considerations: {', '.join(rec['considerations'])}")
    
    print("\n" + "-" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(result.summary)
    
    print("\n" + "-" * 80)
    print("ALTERNATIVES")
    print("-" * 80)
    print(result.alternatives)
    
    if result.validation_summary:
        print("\n" + "-" * 80)
        print("VALIDATION SUMMARY")
        print("-" * 80)
        for key, value in result.validation_summary.items():
            print(f"{key}: {value}")
    
    if result.error_message:
        print("\n" + "-" * 80)
        print("ERROR MESSAGE")
        print("-" * 80)
        print(result.error_message)
    
    print("=" * 80)


def main():
    """Main demonstration function"""
    print("Phase 4: LLM Recommendation and Reasoning Layer Demo")
    print("Using Groq API for restaurant recommendations")
    
    # Environment variables already loaded at module level
    
    # Set up logging
    setup_logging()
    
    # Create Phase 4 integration
    # Using real API key from .env file
    # Set use_mock=True for testing without API key
    # Set use_mock=False for real API calls
    phase4 = create_phase4_integration(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192",
        strict_validation=False,
        use_mock=False,  # Using real API with .env key
        temperature=0.3,
        max_tokens=4096
    )
    
    # Get system status
    print("\nChecking system status...")
    status = phase4.get_system_status()
    print(f"Connection Test: {status['connection_test']}")
    print(f"Model: {status['config']['model']}")
    print(f"Mock Mode: {status['config']['use_mock']}")
    
    if not status['connection_test'] and not status['config']['use_mock']:
        print("Warning: Connection test failed. Check API key and network connection.")
        return
    
    # Create sample data
    preferences = create_sample_user_preferences()
    restaurants = create_sample_restaurants()
    
    print(f"\nUser Preferences:")
    print(f"  Location: {preferences.location}")
    print(f"  Budget: ${preferences.budget_min} - ${preferences.budget_max}")
    print(f"  Cuisine: {preferences.cuisine}")
    print(f"  Min Rating: {preferences.min_rating}")
    print(f"  Dietary Constraints: {preferences.dietary_constraints}")
    print(f"  Meal Type: {preferences.meal_type}")
    print(f"  Group Size: {preferences.group_size}")
    
    print(f"\nCandidate Restaurants: {len(restaurants)}")
    for i, restaurant in enumerate(restaurants, 1):
        print(f"  {i}. {restaurant.name} ({restaurant.cuisine}, {restaurant.rating} stars, {restaurant.price_range})")
    
    # Generate recommendations
    print(f"\nGenerating recommendations...")
    result = phase4.generate_recommendations(preferences, restaurants)
    
    # Print results
    print_recommendations(result)


def test_different_scenarios():
    """Test different user preference scenarios"""
    print("\n" + "=" * 80)
    print("TESTING DIFFERENT SCENARIOS")
    print("=" * 80)
    
    # Create integration
    phase4 = create_phase4_integration(use_mock=True)
    
    # Test scenarios
    scenarios = [
        {
            "name": "Budget-Conscious Student",
            "preferences": UserPreference(
                location="New York",
                budget_min=10,
                budget_max=30,
                cuisine="Any",
                min_rating=3.5,
                dietary_constraints=None,
                meal_type="lunch",
                group_size=1
            )
        },
        {
            "name": "Romantic Dinner",
            "preferences": UserPreference(
                location="New York",
                budget_min=100,
                budget_max=200,
                cuisine="French",
                min_rating=4.5,
                dietary_constraints=None,
                meal_type="dinner",
                group_size=2
            )
        },
        {
            "name": "Family with Kids",
            "preferences": UserPreference(
                location="New York",
                budget_min=50,
                budget_max=100,
                cuisine="American",
                min_rating=4.0,
                dietary_constraints=["kid-friendly"],
                meal_type="dinner",
                group_size=4
            )
        }
    ]
    
    restaurants = create_sample_restaurants()
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        result = phase4.generate_recommendations(scenario['preferences'], restaurants)
        
        print(f"Success: {result.success}")
        print(f"Top Recommendation: {result.recommendations[0]['restaurant_name'] if result.recommendations else 'None'}")
        print(f"Processing Time: {result.processing_time:.2f}s")


if __name__ == "__main__":
    # Run main demonstration
    main()
    
    # Uncomment to run additional scenarios
    # test_different_scenarios()
