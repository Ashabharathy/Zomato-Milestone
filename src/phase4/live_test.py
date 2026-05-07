"""
Live Test for Phase 4: LLM Recommendation and Reasoning Layer
Tests with real user input: Indiranagar, budget 1000, rating 4.0
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


def create_indiranagar_restaurants():
    """Create sample restaurants in Indiranagar area"""
    return [
        Restaurant(
            name="Toit",
            cuisine="Brewery & European",
            location="Indiranagar",
            rating=4.5,
            price_range="$$$",
            avg_cost_for_two=1200,
            address="298, 12th Main Rd, Indiranagar, Bangalore",
            features=["craft beer", "rooftop seating", "live music"],
            description="Popular brewery with European cuisine and great ambiance"
        ),
        Restaurant(
            name="Brahmin's Coffee Bar",
            cuisine="South Indian",
            location="Indiranagar", 
            rating=4.2,
            price_range="$",
            avg_cost_for_two=200,
            address="7th Main Rd, Indiranagar, Bangalore",
            features=["traditional", "breakfast", "quick service"],
            description="Authentic South Indian breakfast and snacks"
        ),
        Restaurant(
            name="The Hole in the Wall",
            cuisine="Continental",
            location="Indiranagar",
            rating=4.6,
            price_range="$$",
            avg_cost_for_two=800,
            address="1st Cross Rd, Indiranagar, Bangalore",
            features=["cafe", "brunch", "pet friendly"],
            description="Cozy cafe with Continental fare and great coffee"
        ),
        Restaurant(
            name="Fenny's Lounge and Kitchen",
            cuisine="Asian Fusion",
            location="Indiranagar",
            rating=4.3,
            price_range="$$$",
            avg_cost_for_two=1500,
            address="100 Feet Rd, Indiranagar, Bangalore",
            features=["bar", "lounge", "live sports"],
            description="Asian fusion cuisine with bar and lounge atmosphere"
        ),
        Restaurant(
            name="Cafe Coffee Day",
            cuisine="Cafe",
            location="Indiranagar",
            rating=3.8,
            price_range="$",
            avg_cost_for_two=300,
            address="CMH Rd, Indiranagar, Bangalore",
            features=["coffee", "wifi", "work friendly"],
            description="Popular coffee chain with light bites"
        ),
        Restaurant(
            name="Truffles",
            cuisine="American",
            location="Indiranagar",
            rating=4.4,
            price_range="$$",
            avg_cost_for_two=600,
            address="38th Cross Rd, Indiranagar, Bangalore",
            features=["burgers", "fast casual", "delivery"],
            description="Famous for burgers and American comfort food"
        ),
        Restaurant(
            name="The Biere Club",
            cuisine="Brewery & Pub",
            location="Indiranagar",
            rating=4.1,
            price_range="$$$",
            avg_cost_for_two=1300,
            address="3rd Floor, 100 Feet Rd, Indiranagar",
            features=["craft beer", "pub", "sports screening"],
            description="Microbrewery with pub food and sports"
        ),
        Restaurant(
            name="Punjab Grill",
            cuisine="North Indian",
            location="Indiranagar",
            rating=4.7,
            price_range="$$$$",
            avg_cost_for_two=1800,
            address="4th Block, Indiranagar, Bangalore",
            features=["fine dining", "bar", "valet parking"],
            description="Upscale North Indian cuisine with modern twist"
        )
    ]


def print_recommendations(result):
    """Print formatted recommendations"""
    print("=" * 80)
    print("PHASE 4 LIVE TEST RESULTS")
    print("=" * 80)
    
    print(f"Success: {result.success}")
    print(f"Fallback Used: {result.fallback_used}")
    print(f"Processing Time: {result.processing_time:.2f} seconds")
    print(f"Model Used: {result.model_used}")
    
    if result.tokens_used:
        print(f"Tokens Used: {result.tokens_used}")
    
    print("\n" + "-" * 80)
    print("TOP 5 RESTAURANT RECOMMENDATIONS")
    print("-" * 80)
    
    # Show top 5 recommendations
    top_recommendations = result.recommendations[:5]
    
    for rec in top_recommendations:
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
    """Main live test function"""
    print("Phase 4 Live Test: Indiranagar Restaurant Recommendations")
    print("User Requirements: Location=Indiranagar, Budget=1000, Rating=4.0+")
    
    # Set up logging
    setup_logging()
    
    # Create Phase 4 integration with real API
    phase4 = create_phase4_integration(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",  # Updated to currently available model
        strict_validation=False,
        use_mock=False,  # Using real API
        temperature=0.3,
        max_tokens=4096
    )
    
    # Get system status
    print("\nChecking system status...")
    status = phase4.get_system_status()
    print(f"Connection Test: {status['connection_test']}")
    print(f"Model: {status['config']['model']}")
    print(f"Mock Mode: {status['config']['use_mock']}")
    
    if not status['connection_test']:
        print("Error: Connection test failed. Check API key and network connection.")
        return
    
    # Create user preferences based on requirements
    preferences = UserPreference(
        location="Indiranagar",
        budget_min=None,  # No minimum specified
        budget_max=1000,  # Budget of 1000
        cuisine=None,     # No specific cuisine preference
        min_rating=4.0,   # Minimum rating of 4.0
        dietary_constraints=None,
        meal_type=None,
        group_size=None
    )
    
    # Create Indiranagar restaurant candidates
    restaurants = create_indiranagar_restaurants()
    
    print(f"\nUser Preferences:")
    print(f"  Location: {preferences.location}")
    print(f"  Budget: Up to ${preferences.budget_max}")
    print(f"  Minimum Rating: {preferences.min_rating}")
    print(f"  Cuisine: Any preference")
    
    print(f"\nCandidate Restaurants: {len(restaurants)}")
    for i, restaurant in enumerate(restaurants, 1):
        print(f"  {i}. {restaurant.name} ({restaurant.cuisine}, {restaurant.rating} stars, {restaurant.price_range}, avg: ${restaurant.avg_cost_for_two})")
    
    # Filter restaurants that meet basic criteria (budget <= 1000, rating >= 4.0)
    eligible_restaurants = [
        r for r in restaurants 
        if r.rating >= preferences.min_rating and 
           (r.avg_cost_for_two is None or r.avg_cost_for_two <= preferences.budget_max)
    ]
    
    print(f"\nEligible Restaurants (after filtering): {len(eligible_restaurants)}")
    for i, restaurant in enumerate(eligible_restaurants, 1):
        print(f"  {i}. {restaurant.name} ({restaurant.cuisine}, {restaurant.rating} stars, avg: ${restaurant.avg_cost_for_two})")
    
    if not eligible_restaurants:
        print("No restaurants meet the specified criteria!")
        return
    
    # Generate recommendations
    print(f"\nGenerating recommendations using Groq LLM...")
    result = phase4.generate_recommendations(preferences, eligible_restaurants)
    
    # Print results
    print_recommendations(result)


if __name__ == "__main__":
    main()
