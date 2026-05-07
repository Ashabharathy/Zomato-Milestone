"""
Example Usage Script for Phase 5: Response Assembly and Presentation Layer
Demonstrates how to use Phase 5 to format and render restaurant recommendations.
"""

import logging
import json
from datetime import datetime

from phase5_integration import create_phase5_integration
from result_formatter import OutputFormat
from output_renderer import RenderTarget, ResponseFormat
from summary_generator import SummaryType


def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_sample_phase4_result():
    """Create sample Phase 4 result for demonstration"""
    return {
        "success": True,
        "recommendations": [
            {
                "rank": 1,
                "restaurant_name": "The Hole in the Wall",
                "score": 0.92,
                "explanation": "This Continental cafe stands out for its high rating of 4.6 and cozy atmosphere. The pet-friendly policy and great coffee make it perfect for casual dining.",
                "highlights": ["Highly rated (4.6/5)", "Cozy atmosphere", "Pet friendly", "Great coffee", "Brunch menu"],
                "considerations": ["Moderately expensive", "Limited seating during peak hours"],
                "cuisine": "Continental",
                "rating": 4.6,
                "price_range": "$$",
                "avg_cost_for_two": 800,
                "location": "Indiranagar",
                "address": "1st Cross Rd, Indiranagar, Bangalore",
                "features": ["cafe", "brunch", "pet friendly", "outdoor seating"]
            },
            {
                "rank": 2,
                "restaurant_name": "Truffles",
                "score": 0.88,
                "explanation": "Famous for burgers and American comfort food with fast-casual service. Great for quick meals and delivery options.",
                "highlights": ["Famous for burgers", "Fast casual", "Delivery available", "Consistent quality"],
                "considerations": ["Less cozy atmosphere", "Can get crowded during weekends"],
                "cuisine": "American",
                "rating": 4.4,
                "price_range": "$$",
                "avg_cost_for_two": 600,
                "location": "Indiranagar",
                "address": "38th Cross Rd, Indiranagar, Bangalore",
                "features": ["burgers", "fast casual", "delivery", "takeout"]
            },
            {
                "rank": 3,
                "restaurant_name": "Brahmin's Coffee Bar",
                "score": 0.78,
                "explanation": "Authentic South Indian cuisine with traditional breakfast options. Perfect for budget-conscious diners seeking local flavors.",
                "highlights": ["Authentic South Indian", "Traditional", "Budget-friendly", "Quick service"],
                "considerations": ["Limited to breakfast and snacks", "No dinner service"],
                "cuisine": "South Indian",
                "rating": 4.2,
                "price_range": "$",
                "avg_cost_for_two": 200,
                "location": "Indiranagar",
                "address": "7th Main Rd, Indiranagar, Bangalore",
                "features": ["traditional", "breakfast", "quick service", "vegetarian"]
            },
            {
                "rank": 4,
                "restaurant_name": "Toit",
                "score": 0.85,
                "explanation": "Popular brewery with European cuisine and craft beer. Great for evening dining with live music.",
                "highlights": ["Craft beer", "Live music", "Rooftop seating", "European cuisine"],
                "considerations": ["Expensive", "Usually crowded", "Reservation recommended"],
                "cuisine": "Brewery & European",
                "rating": 4.5,
                "price_range": "$$$",
                "avg_cost_for_two": 1200,
                "location": "Indiranagar",
                "address": "298, 12th Main Rd, Indiranagar, Bangalore",
                "features": ["brewery", "live music", "rooftop", "bar"]
            },
            {
                "rank": 5,
                "restaurant_name": "Punjab Grill",
                "score": 0.82,
                "explanation": "Upscale North Indian cuisine with modern twist and fine dining experience. Perfect for special occasions.",
                "highlights": ["Fine dining", "North Indian", "Modern twist", "Excellent service"],
                "considerations": ["Very expensive", "Formal dress code", "Reservation required"],
                "cuisine": "North Indian",
                "rating": 4.7,
                "price_range": "$$$$",
                "avg_cost_for_two": 1800,
                "location": "Indiranagar",
                "address": "4th Block, Indiranagar, Bangalore",
                "features": ["fine dining", "bar", "valet parking", "private dining"]
            }
        ],
        "summary": "The recommendations offer a diverse range of dining experiences in Indiranagar, from cozy cafes to fine dining establishments, catering to different budgets and preferences.",
        "alternatives": "Consider exploring nearby areas like Koramangala or Brigade Road for additional restaurant options if these don't meet your specific needs.",
        "processing_time": 2.14,
        "model_used": "llama-3.3-70b-versatile",
        "tokens_used": 1450,
        "fallback_used": False,
        "validation_summary": {
            "total_validations": 1,
            "level_counts": {"info": 1, "warning": 0, "error": 0, "critical": 0},
            "is_valid": True,
            "fallback_triggered": False
        }
    }


def demo_cli_outputs():
    """Demonstrate different CLI output formats"""
    print("=" * 80)
    print("PHASE 5 CLI OUTPUT DEMONSTRATION")
    print("=" * 80)
    
    # Create Phase 5 integration
    phase5 = create_phase5_integration(
        default_output_format=OutputFormat.CARD,
        default_render_target=RenderTarget.CLI,
        enable_summaries=True
    )
    
    # Get sample data
    phase4_result = create_sample_phase4_result()
    
    # Demo 1: Text output with card format
    print("\n" + "-" * 80)
    print("DEMO 1: TEXT OUTPUT - CARD FORMAT")
    print("-" * 80)
    text_output = phase5.get_cli_output(
        phase4_result,
        output_format=OutputFormat.CARD,
        use_markdown=False
    )
    print(text_output)
    
    # Demo 2: Markdown output with list format
    print("\n" + "-" * 80)
    print("DEMO 2: MARKDOWN OUTPUT - LIST FORMAT")
    print("-" * 80)
    markdown_output = phase5.get_cli_output(
        phase4_result,
        output_format=OutputFormat.LIST,
        use_markdown=True
    )
    print(markdown_output)
    
    # Demo 3: Compact format
    print("\n" + "-" * 80)
    print("DEMO 3: COMPACT FORMAT")
    print("-" * 80)
    compact_output = phase5.get_cli_output(
        phase4_result,
        output_format=OutputFormat.COMPACT,
        use_markdown=False
    )
    print(compact_output)


def demo_json_outputs():
    """Demonstrate JSON output formats"""
    print("\n" + "=" * 80)
    print("PHASE 5 JSON OUTPUT DEMONSTRATION")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    phase4_result = create_sample_phase4_result()
    
    # Demo 1: Card format JSON
    print("\n" + "-" * 80)
    print("DEMO 1: CARD FORMAT JSON")
    print("-" * 80)
    card_json = phase5.get_json_output(
        phase4_result,
        output_format=OutputFormat.CARD,
        max_recommendations=3
    )
    print(card_json)
    
    # Demo 2: Table format JSON
    print("\n" + "-" * 80)
    print("DEMO 2: TABLE FORMAT JSON")
    print("-" * 80)
    table_json = phase5.get_json_output(
        phase4_result,
        output_format=OutputFormat.TABLE,
        max_recommendations=3
    )
    print(table_json)


def demo_api_responses():
    """Demonstrate API response formats"""
    print("\n" + "=" * 80)
    print("PHASE 5 API RESPONSE DEMONSTRATION")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    phase4_result = create_sample_phase4_result()
    
    # Demo 1: Standard API response
    print("\n" + "-" * 80)
    print("DEMO 1: STANDARD API RESPONSE")
    print("-" * 80)
    api_response = phase5.get_api_response(
        phase4_result,
        output_format=OutputFormat.CARD,
        include_summary=True,
        max_recommendations=3
    )
    print(json.dumps(api_response, indent=2))
    
    # Demo 2: Mobile-optimized response
    print("\n" + "-" * 80)
    print("DEMO 2: MOBILE-OPTIMIZED RESPONSE")
    print("-" * 80)
    mobile_response = phase5.get_mobile_response(
        phase4_result,
        output_format=OutputFormat.CARD,
        max_recommendations=3
    )
    print(json.dumps(mobile_response, indent=2))


def demo_html_output():
    """Demonstrate HTML output"""
    print("\n" + "=" * 80)
    print("PHASE 5 HTML OUTPUT DEMONSTRATION")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    phase4_result = create_sample_phase4_result()
    
    print("\n" + "-" * 80)
    print("DEMO: HTML OUTPUT (CARD FORMAT)")
    print("-" * 80)
    html_output = phase5.get_html_output(
        phase4_result,
        output_format=OutputFormat.CARD,
        max_recommendations=3
    )
    
    # Show first 500 characters of HTML
    print(html_output[:500] + "..." if len(html_output) > 500 else html_output)
    
    # Save full HTML to file for viewing
    with open("phase5_demo_output.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    print("\nFull HTML saved to 'phase5_demo_output.html' for viewing in browser")


def demo_summaries():
    """Demonstrate summary generation"""
    print("\n" + "=" * 80)
    print("PHASE 5 SUMMARY GENERATION DEMONSTRATION")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    phase4_result = create_sample_phase4_result()
    
    # Demo 1: Quick comparison
    print("\n" + "-" * 80)
    print("DEMO 1: QUICK COMPARISON")
    print("-" * 80)
    quick_summary = phase5.create_comparison_summary(
        phase4_result,
        summary_type=SummaryType.QUICK_COMPARISON,
        max_items=3
    )
    print(f"Title: {quick_summary.title}")
    print(f"Type: {quick_summary.summary_type.value}")
    print("Insights:")
    for insight in quick_summary.insights:
        print(f"  - {insight}")
    print("Recommendations:")
    for rec in quick_summary.recommendations:
        print(f"  - {rec}")
    
    # Demo 2: Best for categories
    print("\n" + "-" * 80)
    print("DEMO 2: BEST FOR CATEGORIES")
    print("-" * 80)
    best_for_summary = phase5.create_comparison_summary(
        phase4_result,
        summary_type=SummaryType.BEST_FOR,
        max_items=5
    )
    print(f"Title: {best_for_summary.title}")
    print("Category Winners:")
    for category, winner in best_for_summary.content.get("category_winners", {}).items():
        print(f"  {category}: {winner['restaurant']} - {winner['reason']}")
    
    # Demo 3: Price comparison
    print("\n" + "-" * 80)
    print("DEMO 3: PRICE COMPARISON")
    print("-" * 80)
    price_summary = phase5.create_comparison_summary(
        phase4_result,
        summary_type=SummaryType.PRICE_COMPARISON,
        max_items=5
    )
    print(f"Title: {price_summary.title}")
    price_comp = price_summary.content.get("price_comparison", {})
    if price_comp.get("most_affordable"):
        print(f"Most Affordable: {price_comp['most_affordable']['restaurant']} ({price_comp['most_affordable']['price_range']})")
    if price_comp.get("most_expensive"):
        print(f"Most Expensive: {price_comp['most_expensive']['restaurant']} ({price_comp['most_expensive']['price_range']})")
    
    # Demo 4: Feature comparison
    print("\n" + "-" * 80)
    print("DEMO 4: FEATURE COMPARISON")
    print("-" * 80)
    feature_summary = phase5.create_comparison_summary(
        phase4_result,
        summary_type=SummaryType.FEATURE_COMPARISON,
        max_items=5
    )
    print(f"Title: {feature_summary.title}")
    print(f"Total Features Analyzed: {feature_summary.metadata.get('total_features', 0)}")
    print(f"Common Features: {', '.join(feature_summary.content.get('common_features', []))}")
    print("Unique Features:")
    for restaurant, features in feature_summary.content.get("unique_features", {}).items():
        print(f"  {restaurant}: {', '.join(features)}")


def demo_different_formats():
    """Demonstrate different output formats"""
    print("\n" + "=" * 80)
    print("PHASE 5 DIFFERENT FORMATS DEMONSTRATION")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    phase4_result = create_sample_phase4_result()
    
    formats = [
        (OutputFormat.CARD, "Card Format"),
        (OutputFormat.LIST, "List Format"),
        (OutputFormat.TABLE, "Table Format"),
        (OutputFormat.COMPACT, "Compact Format"),
        (OutputFormat.DETAILED, "Detailed Format")
    ]
    
    for output_format, format_name in formats:
        print("\n" + "-" * 80)
        print(f"DEMO: {format_name}")
        print("-" * 80)
        
        output = phase5.get_cli_output(
            phase4_result,
            output_format=output_format,
            use_markdown=False
        )
        
        # Show first 300 characters
        print(output[:300] + "..." if len(output) > 300 else output)


def demo_system_status():
    """Demonstrate system status"""
    print("\n" + "=" * 80)
    print("PHASE 5 SYSTEM STATUS")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    status = phase5.get_system_status()
    
    print("Components:")
    for component, status_msg in status["components"].items():
        print(f"  {component}: {status_msg}")
    
    print("\nConfiguration:")
    for key, value in status["config"].items():
        print(f"  {key}: {value}")
    
    print("\nSupported Formats:")
    print(f"  Output Formats: {', '.join(status['supported_formats'])}")
    print(f"  Render Targets: {', '.join(status['supported_targets'])}")
    print(f"  Response Formats: {', '.join(status['supported_response_formats'])}")
    print(f"  Summary Types: {', '.join(status['supported_summary_types'])}")


def main():
    """Main demonstration function"""
    print("Phase 5: Response Assembly and Presentation Layer Demo")
    print("Demonstrating various output formats and rendering options")
    
    # Set up logging
    setup_logging()
    
    # Run demonstrations
    demo_system_status()
    demo_cli_outputs()
    demo_json_outputs()
    demo_api_responses()
    demo_html_output()
    demo_summaries()
    demo_different_formats()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("Phase 5 successfully demonstrated:")
    print("  - CLI text and markdown outputs")
    print("  - JSON structured outputs")
    print("  - API and mobile responses")
    print("  - HTML web outputs")
    print("  - Summary generation")
    print("  - Multiple output formats")
    print("  - System status and configuration")


def test_error_handling():
    """Test error handling scenarios"""
    print("\n" + "=" * 80)
    print("PHASE 5 ERROR HANDLING TEST")
    print("=" * 80)
    
    phase5 = create_phase5_integration()
    
    # Test with empty recommendations
    print("\n" + "-" * 80)
    print("TEST: EMPTY RECOMMENDATIONS")
    print("-" * 80)
    empty_result = {
        "success": True,
        "recommendations": [],
        "summary": "No recommendations available",
        "alternatives": "Try different search criteria"
    }
    
    output = phase5.get_cli_output(empty_result)
    print(output)
    
    # Test with invalid data
    print("\n" + "-" * 80)
    print("TEST: INVALID DATA")
    print("-" * 80)
    invalid_result = {
        "success": False,
        "recommendations": None,
        "summary": "Error occurred",
        "alternatives": "Please try again"
    }
    
    output = phase5.get_cli_output(invalid_result)
    print(output)


if __name__ == "__main__":
    # Run main demonstration
    main()
    
    # Uncomment to run error handling tests
    # test_error_handling()
