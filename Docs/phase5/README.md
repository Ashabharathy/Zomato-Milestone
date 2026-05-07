# Phase 5: Response Assembly and Presentation Layer

This module implements Phase 5 of the AI-Powered Restaurant Recommendation System, focusing on delivering clear, useful recommendations to end users through various output formats.

## Overview

Phase 5 takes the ranked recommendations from Phase 4 and transforms them into user-visible outputs suitable for different platforms and use cases. The layer includes:

- **Result Formatter**: Formats recommendations into card/list/table JSON structures
- **Output Renderer**: Renders formatted data for CLI, Web, API, and Mobile responses  
- **Summary Generator**: Creates quick comparisons and analysis between top options
- **Integration Layer**: Coordinates all components for seamless output generation

## Architecture

```
Input: Ranked recommendation output from LLM (Phase 4)
    |
    v
[Result Formatter] -> Structured JSON data (card/list/table formats)
    |
    v
[Output Renderer] -> Platform-specific outputs (CLI/Web/API/Mobile)
    |
    v
[Summary Generator] -> Comparative analysis and insights
    |
    v
Output: Final user-visible recommendation list
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. The module primarily uses Python standard library, with optional dependencies for enhanced features.

## Quick Start

```python
from phase5 import create_phase5_integration, OutputFormat, RenderTarget

# Create Phase 5 integration
phase5 = create_phase5_integration(
    default_output_format=OutputFormat.CARD,
    default_render_target=RenderTarget.CLI,
    enable_summaries=True
)

# Process Phase 4 recommendations
phase4_result = {
    "success": True,
    "recommendations": [
        {
            "rank": 1,
            "restaurant_name": "The Hole in the Wall",
            "score": 0.92,
            "explanation": "Great cafe with cozy atmosphere...",
            "highlights": ["Highly rated", "Pet friendly"],
            "considerations": ["Moderately expensive"],
            "cuisine": "Continental",
            "rating": 4.6,
            "price_range": "$$",
            "avg_cost_for_two": 800
        }
        # ... more recommendations
    ],
    "summary": "Top recommendations for your preferences...",
    "alternatives": "Consider exploring other options..."
}

# Generate CLI output
cli_output = phase5.get_cli_output(phase4_result)
print(cli_output)

# Generate JSON output
json_output = phase5.get_json_output(phase4_result)

# Generate HTML output
html_output = phase5.get_html_output(phase4_result)

# Generate API response
api_response = phase5.get_api_response(phase4_result)
```

## Components

### Result Formatter (`result_formatter.py`)

Transforms raw LLM recommendations into structured formats:

**Supported Output Formats:**
- `CARD`: Rich card format with full details
- `LIST`: Simple list format with essential information
- `TABLE`: Tabular format for data display
- `COMPACT`: Minimal format for space-constrained displays
- `DETAILED`: Full format with all available information

**Key Features:**
- Flexible formatting based on target platform
- Automatic content truncation for different display sizes
- JSON serialization for API integration
- Comparison table generation

### Output Renderer (`output_renderer.py`)

Renders formatted data for different platforms:

**Supported Targets:**
- `CLI`: Command-line interface (text/markdown)
- `WEB`: Web interface (HTML)
- `API`: REST API responses (JSON)
- `MOBILE`: Mobile applications (optimized JSON)

**Response Formats:**
- `TEXT`: Plain text output
- `HTML`: Styled HTML with CSS
- `JSON`: Structured JSON data
- `MARKDOWN`: Markdown-formatted text

**Key Features:**
- Platform-specific optimization
- Responsive HTML generation
- API-structured responses
- Mobile-optimized data structures

### Summary Generator (`summary_generator.py`)

Creates comparative analysis and insights:

**Summary Types:**
- `QUICK_COMPARISON`: Fast comparison of top options
- `DETAILED_ANALYSIS`: Comprehensive analysis with pros/cons
- `BEST_FOR`: Category-based recommendations (best value, best quality, etc.)
- `PRICE_COMPARISON`: Price-focused analysis
- `FEATURE_COMPARISON`: Feature-based comparison

**Key Features:**
- Automatic insight generation
- Category-based recommendations
- Value for money analysis
- Feature comparison matrices

## Configuration

### Phase5Config

```python
Phase5Config(
    default_output_format=OutputFormat.CARD,
    default_render_target=RenderTarget.CLI,
    default_response_format=None,
    max_recommendations=10,
    enable_summaries=True,
    enable_comparisons=True,
    include_metadata=True
)
```

## Usage Examples

### CLI Output

```python
# Text format
text_output = phase5.get_cli_output(phase4_result, use_markdown=False)

# Markdown format
markdown_output = phase5.get_cli_output(phase4_result, use_markdown=True)

# Different formats
compact_output = phase5.get_cli_output(phase4_result, output_format=OutputFormat.COMPACT)
detailed_output = phase5.get_cli_output(phase4_result, output_format=OutputFormat.DETAILED)
```

### Web Integration

```python
# HTML output
html_content = phase5.get_html_output(phase4_result, output_format=OutputFormat.CARD)

# Save to file
with open("recommendations.html", "w") as f:
    f.write(html_content)
```

### API Integration

```python
# Standard API response
api_response = phase5.get_api_response(
    phase4_result,
    output_format=OutputFormat.CARD,
    include_summary=True
)

# Mobile-optimized response
mobile_response = phase5.get_mobile_response(
    phase4_result,
    output_format=OutputFormat.LIST
)
```

### Summary Generation

```python
# Quick comparison
quick_summary = phase5.create_comparison_summary(
    phase4_result,
    summary_type=SummaryType.QUICK_COMPARISON,
    max_items=3
)

# Best for categories
best_for_summary = phase5.create_comparison_summary(
    phase4_result,
    summary_type=SummaryType.BEST_FOR
)

# Price comparison
price_summary = phase5.create_comparison_summary(
    phase4_result,
    summary_type=SummaryType.PRICE_COMPARISON
)
```

## Data Structures

### FormattedResult

```python
FormattedResult(
    format_type=OutputFormat.CARD,
    recommendations=[FormattedRecommendation(...)],
    summary="Brief summary of recommendations",
    alternatives="Alternative suggestions",
    metadata={"processing_time": 1.23, "model_used": "..."},
    success=True,
    total_count=5
)
```

### RenderedOutput

```python
RenderedOutput(
    content="<html>...</html>",
    format_type=ResponseFormat.HTML,
    target=RenderTarget.WEB,
    metadata={"rendered_at": "...", "content_length": 1234},
    content_type="text/html",
    success=True
)
```

### SummaryResult

```python
SummaryResult(
    summary_type=SummaryType.QUICK_COMPARISON,
    title="Quick Comparison of Top Restaurants",
    content={"restaurants": [...], "winner": {...}},
    insights=["Average rating: 4.3 stars", "Price range: $ - $$$"],
    recommendations=["Best overall: Restaurant Name"],
    metadata={"items_compared": 3}
)
```

## Output Examples

### CLI Text Output

```
================================================================================
RESTAURANT RECOMMENDATIONS
================================================================================
Total Recommendations: 3
Format: card

--------------------------------------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------------------------------------

1. The Hole in the Wall (Score: 0.92)
   Cuisine: Continental
   Rating: 4.6/5
   Price: $$
   Explanation: This Continental cafe stands out for its high rating...
   Highlights: Highly rated, Cozy atmosphere, Pet friendly
   Considerations: Moderately expensive
```

### JSON Output

```json
{
  "format_type": "card",
  "success": true,
  "total_count": 3,
  "summary": "Top recommendations for your preferences...",
  "alternatives": "Consider exploring other options...",
  "metadata": {
    "processing_time": 0.15,
    "model_used": "llama-3.3-70b-versatile",
    "tokens_used": 1450
  },
  "recommendations": [
    {
      "rank": 1,
      "restaurant_name": "The Hole in the Wall",
      "score": 0.92,
      "explanation": "This Continental cafe...",
      "highlights": ["Highly rated", "Cozy atmosphere"],
      "cuisine": "Continental",
      "rating": 4.6,
      "price_range": "$$"
    }
  ]
}
```

### HTML Output

Generated HTML includes:
- Responsive design with CSS
- Card-based layout
- Star ratings display
- Highlight sections
- Mobile-friendly interface

### API Response

```json
{
  "success": true,
  "data": {
    "recommendations": [...],
    "summary": "...",
    "alternatives": "..."
  },
  "metadata": {
    "processing_time": 0.15,
    "output_format": "card",
    "total_recommendations": 3
  },
  "summary": {
    "type": "quick_comparison",
    "title": "Quick Comparison of Top Restaurants",
    "insights": [...],
    "recommendations": [...]
  }
}
```

## Advanced Features

### Custom Formatting

```python
# Custom output format
result = phase5.process_recommendations(
    phase4_result,
    output_format=OutputFormat.CARD,
    render_target=RenderTarget.WEB,
    response_format=ResponseFormat.HTML,
    generate_summary=True,
    max_recommendations=5
)

# Access components
formatted_result = result.formatted_result
rendered_output = result.rendered_output
summary_result = result.summary_result
```

### Error Handling

The system includes comprehensive error handling:
- Graceful degradation for missing data
- Fallback outputs for format failures
- Detailed error messages for debugging
- Validation of input data

### Performance Optimization

- Efficient JSON serialization
- Minimal memory usage for large datasets
- Lazy loading of optional components
- Configurable output limits

## Integration with Other Phases

### Input from Phase 4
- Ranked recommendations with scores
- Natural language explanations
- Restaurant metadata and features
- Processing metrics and validation data

### Output to Frontend/UI
- Formatted recommendation data
- Platform-specific rendering
- Comparative summaries
- Metadata for display and tracking

## Testing

Run the example script to see all features in action:

```bash
cd phase5
python example_usage.py
```

This demonstrates:
- All output formats (card, list, table, compact, detailed)
- All render targets (CLI, Web, API, Mobile)
- All summary types (quick comparison, best for, price, features)
- Error handling scenarios
- System status and configuration

## Monitoring and Logging

- Comprehensive logging at all levels
- Performance metrics tracking
- Error rate monitoring
- Output format validation

## Security Considerations

- Input sanitization and validation
- Safe HTML generation with XSS protection
- JSON serialization security
- Error message sanitization

## Future Enhancements

- Additional output formats (PDF, Excel)
- Real-time streaming updates
- Advanced personalization
- Multi-language support
- Accessibility features
- Custom theming and branding
