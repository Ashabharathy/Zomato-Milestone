# Phase 4: LLM Recommendation and Reasoning Layer

This module implements Phase 4 of the AI-Powered Restaurant Recommendation System, focusing on LLM-based recommendation generation with explainability using Groq API.

## Overview

Phase 4 takes shortlisted restaurant candidates from Phase 3 and generates personalized recommendations with detailed explanations using Large Language Models. The layer includes:

- **Prompt Builder**: Creates structured prompts with user context and instruction templates
- **LLM Inference**: Handles Groq API integration for generating recommendations
- **Response Parser**: Extracts and validates rankings and explanations from LLM responses
- **Guardrails**: Implements format checks and fallback behavior for invalid outputs

## Architecture

```
Input: Shortlisted candidates + user preferences
    |
    v
[Prompt Builder] -> Structured prompt for LLM
    |
    v
[LLM Inference] -> Groq API response
    |
    v
[Response Parser] -> Extract structured recommendations
    |
    v
[Guardrails] -> Validate and process response
    |
    v
Output: Ranked recommendations with explanations
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

## Quick Start

```python
from phase4 import create_phase4_integration, UserPreference, Restaurant

# Create integration
phase4 = create_phase4_integration(
    groq_api_key="your_api_key",
    model="llama3-70b-8192",
    use_mock=False  # Set to True for testing without API
)

# Define user preferences
preferences = UserPreference(
    location="New York",
    budget_min=50,
    budget_max=100,
    cuisine="Italian",
    min_rating=4.0,
    dietary_constraints=["vegetarian"],
    meal_type="dinner",
    group_size=2
)

# Define candidate restaurants
restaurants = [
    Restaurant(
        name="Bella Italia",
        cuisine="Italian",
        location="New York",
        rating=4.5,
        price_range="$$",
        avg_cost_for_two=60,
        address="123 Main St, New York, NY",
        features=["vegetarian options", "outdoor seating"],
        description="Authentic Italian cuisine"
    )
    # ... more restaurants
]

# Generate recommendations
result = phase4.generate_recommendations(preferences, restaurants)

# Process results
if result.success:
    for rec in result.recommendations:
        print(f"{rec['rank']}. {rec['restaurant_name']} (Score: {rec['score']:.2f})")
        print(f"   {rec['explanation']}")
else:
    print(f"Error: {result.error_message}")
```

## Components

### Prompt Builder (`prompt_builder.py`)

Creates structured prompts for the LLM with:
- System instructions for recommendation generation
- User preference formatting
- Restaurant candidate presentation
- Validation of prompt components

### LLM Inference (`llm_inference.py`)

Handles Groq API integration:
- Multiple model support (llama3-70b-8192, llama3-8b-8192, mixtral-8x7b-32768, gemma-7b-it)
- Retry logic with exponential backoff
- Connection testing and health monitoring
- Mock client for testing without API keys

### Response Parser (`response_parser.py`)

Extracts and validates LLM responses:
- JSON extraction from various formats
- Structured recommendation parsing
- Validation against candidate restaurants
- Quality assessment metrics

### Guardrails (`guardrails.py`)

Implements validation and fallback mechanisms:
- Multi-level validation (info, warning, error, critical)
- Format and content validation
- Fallback response generation
- Strict mode for production use

## Configuration

### Phase4Config

```python
Phase4Config(
    groq_api_key="your_api_key",
    groq_model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=4096,
    top_p=0.9,
    timeout=30,
    max_retries=3,
    strict_validation=False,
    use_mock=False
)
```

### Available Groq Models

- `llama3-70b-8192` - Most capable model (recommended)
- `llama3-8b-8192` - Faster, less capable
- `mixtral-8x7b-32768` - Good balance of speed/capability
- `gemma-7b-it` - Lightweight option

## Data Structures

### UserPreference

```python
UserPreference(
    location="New York",           # Required
    budget_min=50,                # Optional
    budget_max=100,               # Optional
    cuisine="Italian",            # Optional
    min_rating=4.0,               # Optional
    dietary_constraints=["veg"],  # Optional
    meal_type="dinner",           # Optional
    group_size=2                  # Optional
)
```

### Restaurant

```python
Restaurant(
    name="Restaurant Name",
    cuisine="Cuisine Type",
    location="City",
    rating=4.5,
    price_range="$$",
    avg_cost_for_two=60,          # Optional
    address="Full Address",       # Optional
    features=["feature1"],        # Optional
    description="Description"     # Optional
)
```

### Phase4Result

```python
Phase4Result(
    success=True,
    recommendations=[...],
    summary="Brief summary",
    alternatives="Alternative suggestions",
    processing_time=1.23,
    tokens_used=500,
    model_used="llama3-70b-8192",
    validation_summary={...},
    fallback_used=False
)
```

## Testing

### Mock Mode

For testing without API calls:

```python
phase4 = create_phase4_integration(use_mock=True)
```

### Example Usage

Run the example script:

```bash
python example_usage.py
```

This demonstrates:
- Basic recommendation generation
- Different user scenarios
- Error handling and fallbacks
- System status checking

## Error Handling

The system includes comprehensive error handling:

1. **Input Validation**: Validates user preferences and restaurant data
2. **API Errors**: Retry logic with exponential backoff
3. **Response Validation**: Multi-level validation of LLM outputs
4. **Fallback Mechanisms**: Graceful degradation when validation fails

## Performance Considerations

- **Token Usage**: Monitor tokens used for cost optimization
- **Response Time**: Track processing time for user experience
- **Model Selection**: Choose appropriate model based on speed/capability needs
- **Batch Processing**: Consider batching for multiple recommendations

## Integration with Other Phases

### Input from Phase 3
- Shortlisted restaurant candidates (filtered by location, budget, cuisine, rating)
- User preference object

### Output to Phase 5
- Structured recommendation data with rankings and explanations
- Validation metadata and quality metrics
- Fallback indicators for monitoring

## Monitoring and Logging

- Comprehensive logging at all levels
- Validation metrics tracking
- API usage monitoring
- Error rate tracking

## Security Considerations

- API key management through environment variables
- Input sanitization and validation
- Rate limiting and timeout handling
- Secure fallback mechanisms

## Future Enhancements

- Support for additional LLM providers
- Advanced prompt engineering strategies
- Real-time learning from user feedback
- Multi-language support
- Personalization based on user history
