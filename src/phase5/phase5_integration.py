"""
Phase 5 Integration Module: Response Assembly and Presentation Layer
Main integration point for Phase 5 components that deliver clear, useful recommendations.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

from .result_formatter import ResultFormatter, OutputFormat, FormattedResult, FormattedRecommendation
from .output_renderer import OutputRenderer, RenderTarget, ResponseFormat, RenderedOutput
from .summary_generator import SummaryGenerator, SummaryType, SummaryResult


@dataclass
class Phase5Config:
    """Configuration for Phase 5 integration"""
    default_output_format: OutputFormat = OutputFormat.CARD
    default_render_target: RenderTarget = RenderTarget.CLI
    default_response_format: Optional[ResponseFormat] = None
    max_recommendations: int = 10
    enable_summaries: bool = True
    enable_comparisons: bool = True
    include_metadata: bool = True


@dataclass
class Phase5Result:
    """Result from Phase 5 processing"""
    success: bool
    formatted_result: Optional[FormattedResult]
    rendered_output: Optional[RenderedOutput]
    summary_result: Optional[SummaryResult]
    processing_time: float
    output_format: OutputFormat
    render_target: RenderTarget
    error_message: Optional[str] = None


class Phase5Integration:
    """Main integration class for Phase 5: Response Assembly and Presentation Layer"""
    
    def __init__(self, config: Phase5Config):
        """
        Initialize Phase 5 integration
        
        Args:
            config: Configuration for Phase 5 components
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.result_formatter = ResultFormatter()
        self.output_renderer = OutputRenderer()
        self.summary_generator = SummaryGenerator()
        
        self.logger.info(f"Phase 5 initialized with format: {config.default_output_format.value}")
    
    def process_recommendations(
        self,
        phase4_result: Dict[str, Any],
        output_format: Optional[OutputFormat] = None,
        render_target: Optional[RenderTarget] = None,
        response_format: Optional[ResponseFormat] = None,
        generate_summary: Optional[bool] = None,
        max_recommendations: Optional[int] = None
    ) -> Phase5Result:
        """
        Process Phase 4 recommendations into final user-visible output
        
        Args:
            phase4_result: Raw result from Phase 4 LLM processing
            output_format: Desired output format (card, list, table, etc.)
            render_target: Target platform (cli, web, api, mobile)
            response_format: Specific response format (text, html, json, etc.)
            generate_summary: Whether to generate summary comparison
            max_recommendations: Maximum recommendations to include
            
        Returns:
            Phase5Result with formatted and rendered output
        """
        start_time = time.time()
        
        try:
            # Use defaults from config if not specified
            output_format = output_format or self.config.default_output_format
            render_target = render_target or self.config.default_render_target
            response_format = response_format or self.config.default_response_format
            generate_summary = generate_summary if generate_summary is not None else self.config.enable_summaries
            max_recommendations = max_recommendations or self.config.max_recommendations
            
            # Step 1: Format recommendations
            formatted_result = self.result_formatter.format_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                max_recommendations=max_recommendations
            )
            
            # Step 2: Render output
            rendered_output = self.output_renderer.render(
                formatted_result=formatted_result,
                target=render_target,
                response_format=response_format
            )
            
            # Step 3: Generate summary (if enabled)
            summary_result = None
            if generate_summary and formatted_result.success and formatted_result.recommendations:
                summary_result = self.summary_generator.generate_summary(
                    recommendations=formatted_result.recommendations,
                    summary_type=SummaryType.QUICK_COMPARISON,
                    max_items=min(3, len(formatted_result.recommendations))
                )
            
            processing_time = time.time() - start_time
            
            return Phase5Result(
                success=True,
                formatted_result=formatted_result,
                rendered_output=rendered_output,
                summary_result=summary_result,
                processing_time=processing_time,
                output_format=output_format,
                render_target=render_target
            )
            
        except Exception as e:
            self.logger.error(f"Error in Phase 5 processing: {str(e)}")
            processing_time = time.time() - start_time
            
            return Phase5Result(
                success=False,
                formatted_result=None,
                rendered_output=None,
                summary_result=None,
                processing_time=processing_time,
                output_format=output_format or self.config.default_output_format,
                render_target=render_target or self.config.default_render_target,
                error_message=str(e)
            )
    
    def get_json_output(
        self,
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        max_recommendations: Optional[int] = None
    ) -> str:
        """
        Get JSON output for API responses
        
        Args:
            phase4_result: Raw result from Phase 4
            output_format: Desired output format
            max_recommendations: Maximum recommendations to include
            
        Returns:
            JSON string with formatted recommendations
        """
        try:
            formatted_result = self.result_formatter.format_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                max_recommendations=max_recommendations
            )
            
            return self.result_formatter.to_json(formatted_result)
            
        except Exception as e:
            self.logger.error(f"Error generating JSON output: {str(e)}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "recommendations": []
            })
    
    def get_html_output(
        self,
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        max_recommendations: Optional[int] = None
    ) -> str:
        """
        Get HTML output for web display
        
        Args:
            phase4_result: Raw result from Phase 4
            output_format: Desired output format
            max_recommendations: Maximum recommendations to include
            
        Returns:
            HTML string with formatted recommendations
        """
        try:
            result = self.process_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                render_target=RenderTarget.WEB,
                response_format=ResponseFormat.HTML,
                generate_summary=True,
                max_recommendations=max_recommendations
            )
            
            return result.rendered_output.content if result.rendered_output else ""
            
        except Exception as e:
            self.logger.error(f"Error generating HTML output: {str(e)}")
            return f"<div class='error'>Error generating recommendations: {str(e)}</div>"
    
    def get_cli_output(
        self,
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        use_markdown: bool = False,
        max_recommendations: Optional[int] = None
    ) -> str:
        """
        Get CLI output for command-line display
        
        Args:
            phase4_result: Raw result from Phase 4
            output_format: Desired output format
            use_markdown: Whether to use markdown formatting
            max_recommendations: Maximum recommendations to include
            
        Returns:
            Formatted string for CLI display
        """
        try:
            response_format = ResponseFormat.MARKDOWN if use_markdown else ResponseFormat.TEXT
            
            result = self.process_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                render_target=RenderTarget.CLI,
                response_format=response_format,
                generate_summary=True,
                max_recommendations=max_recommendations
            )
            
            return result.rendered_output.content if result.rendered_output else ""
            
        except Exception as e:
            self.logger.error(f"Error generating CLI output: {str(e)}")
            return f"Error generating recommendations: {str(e)}"
    
    def get_api_response(
        self,
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        include_summary: bool = True,
        max_recommendations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get structured API response
        
        Args:
            phase4_result: Raw result from Phase 4
            output_format: Desired output format
            include_summary: Whether to include summary data
            max_recommendations: Maximum recommendations to include
            
        Returns:
            Structured dictionary for API response
        """
        try:
            result = self.process_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                render_target=RenderTarget.API,
                response_format=ResponseFormat.JSON,
                generate_summary=include_summary,
                max_recommendations=max_recommendations
            )
            
            if not result.success:
                return {
                    "success": False,
                    "error": result.error_message,
                    "data": None
                }
            
            api_response = {
                "success": True,
                "data": json.loads(result.rendered_output.content) if result.rendered_output else None,
                "metadata": {
                    "processing_time": result.processing_time,
                    "output_format": result.output_format.value,
                    "total_recommendations": result.formatted_result.total_count if result.formatted_result else 0
                }
            }
            
            # Add summary if available
            if result.summary_result and include_summary:
                api_response["summary"] = {
                    "type": result.summary_result.summary_type.value,
                    "title": result.summary_result.title,
                    "insights": result.summary_result.insights,
                    "recommendations": result.summary_result.recommendations,
                    "content": result.summary_result.content
                }
            
            return api_response
            
        except Exception as e:
            self.logger.error(f"Error generating API response: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def get_mobile_response(
        self,
        phase4_result: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.CARD,
        max_recommendations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get mobile-optimized response
        
        Args:
            phase4_result: Raw result from Phase 4
            output_format: Desired output format
            max_recommendations: Maximum recommendations to include
            
        Returns:
            Mobile-optimized dictionary
        """
        try:
            result = self.process_recommendations(
                phase4_result=phase4_result,
                output_format=output_format,
                render_target=RenderTarget.MOBILE,
                response_format=ResponseFormat.JSON,
                generate_summary=False,  # Mobile apps typically handle their own summaries
                max_recommendations=max_recommendations
            )
            
            if not result.success:
                return {
                    "success": False,
                    "error": result.error_message,
                    "ui_data": None
                }
            
            return json.loads(result.rendered_output.content) if result.rendered_output else {}
            
        except Exception as e:
            self.logger.error(f"Error generating mobile response: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "ui_data": None
            }
    
    def create_comparison_summary(
        self,
        phase4_result: Dict[str, Any],
        summary_type: SummaryType = SummaryType.QUICK_COMPARISON,
        max_items: int = 3
    ) -> SummaryResult:
        """
        Create detailed comparison summary
        
        Args:
            phase4_result: Raw result from Phase 4
            summary_type: Type of summary to generate
            max_items: Maximum items to compare
            
        Returns:
            SummaryResult with comparison data
        """
        try:
            # First format the recommendations
            formatted_result = self.result_formatter.format_recommendations(
                phase4_result=phase4_result,
                output_format=OutputFormat.DETAILED,
                max_recommendations=max_items
            )
            
            if not formatted_result.success or not formatted_result.recommendations:
                return self.summary_generator._create_empty_summary(summary_type)
            
            # Generate summary
            return self.summary_generator.generate_summary(
                recommendations=formatted_result.recommendations,
                summary_type=summary_type,
                max_items=max_items
            )
            
        except Exception as e:
            self.logger.error(f"Error creating comparison summary: {str(e)}")
            return self.summary_generator._create_error_summary(str(e), summary_type)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all Phase 5 components"""
        return {
            "components": {
                "result_formatter": "initialized",
                "output_renderer": "initialized",
                "summary_generator": "initialized"
            },
            "config": {
                "default_output_format": self.config.default_output_format.value,
                "default_render_target": self.config.default_render_target.value,
                "max_recommendations": self.config.max_recommendations,
                "enable_summaries": self.config.enable_summaries,
                "enable_comparisons": self.config.enable_comparisons
            },
            "supported_formats": [fmt.value for fmt in OutputFormat],
            "supported_targets": [target.value for target in RenderTarget],
            "supported_response_formats": [fmt.value for fmt in ResponseFormat],
            "supported_summary_types": [summary_type.value for summary_type in SummaryType]
        }
    
    def update_config(self, **kwargs) -> None:
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config parameter: {key}")
    
    def create_sample_phase4_result(self) -> Dict[str, Any]:
        """Create sample Phase 4 result for testing"""
        return {
            "success": True,
            "recommendations": [
                {
                    "rank": 1,
                    "restaurant_name": "The Hole in the Wall",
                    "score": 0.92,
                    "explanation": "This Continental cafe stands out for its high rating of 4.6 and cozy atmosphere.",
                    "highlights": ["Highly rated", "Cozy atmosphere", "Pet friendly"],
                    "considerations": ["Moderately expensive"],
                    "cuisine": "Continental",
                    "rating": 4.6,
                    "price_range": "$$",
                    "avg_cost_for_two": 800,
                    "location": "Indiranagar",
                    "address": "1st Cross Rd, Indiranagar, Bangalore",
                    "features": ["cafe", "brunch", "pet friendly"]
                },
                {
                    "rank": 2,
                    "restaurant_name": "Truffles",
                    "score": 0.88,
                    "explanation": "Famous for burgers and American comfort food with fast-casual service.",
                    "highlights": ["Famous for burgers", "Fast casual", "Delivery available"],
                    "considerations": ["Less cozy atmosphere"],
                    "cuisine": "American",
                    "rating": 4.4,
                    "price_range": "$$",
                    "avg_cost_for_two": 600,
                    "location": "Indiranagar",
                    "address": "38th Cross Rd, Indiranagar, Bangalore",
                    "features": ["burgers", "fast casual", "delivery"]
                },
                {
                    "rank": 3,
                    "restaurant_name": "Brahmin's Coffee Bar",
                    "score": 0.78,
                    "explanation": "Authentic South Indian cuisine with traditional breakfast options.",
                    "highlights": ["Authentic South Indian", "Traditional", "Budget-friendly"],
                    "considerations": ["Limited to breakfast and snacks"],
                    "cuisine": "South Indian",
                    "rating": 4.2,
                    "price_range": "$",
                    "avg_cost_for_two": 200,
                    "location": "Indiranagar",
                    "address": "7th Main Rd, Indiranagar, Bangalore",
                    "features": ["traditional", "breakfast", "quick service"]
                }
            ],
            "summary": "The recommendations prioritize high-quality dining experiences in Indiranagar.",
            "alternatives": "Consider exploring restaurants outside Indiranagar for more options.",
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


def create_phase5_integration(
    default_output_format: OutputFormat = OutputFormat.CARD,
    default_render_target: RenderTarget = RenderTarget.CLI,
    max_recommendations: int = 10,
    enable_summaries: bool = True,
    **kwargs
) -> Phase5Integration:
    """
    Factory function to create Phase 5 integration
    
    Args:
        default_output_format: Default output format for recommendations
        default_render_target: Default target platform
        max_recommendations: Maximum recommendations to include
        enable_summaries: Whether to enable summary generation
        **kwargs: Additional configuration parameters
        
    Returns:
        Configured Phase5Integration instance
    """
    config = Phase5Config(
        default_output_format=default_output_format,
        default_render_target=default_render_target,
        max_recommendations=max_recommendations,
        enable_summaries=enable_summaries,
        **kwargs
    )
    
    return Phase5Integration(config)


# Example usage function
def example_usage():
    """Example of how to use Phase 5 integration"""
    import json
    
    # Create integration
    phase5 = create_phase5_integration(
        default_output_format=OutputFormat.CARD,
        default_render_target=RenderTarget.CLI,
        enable_summaries=True
    )
    
    # Get system status
    status = phase5.get_system_status()
    print("System Status:", json.dumps(status, indent=2))
    
    # Create sample data
    phase4_result = phase5.create_sample_phase4_result()
    
    # Generate CLI output
    print("\n" + "=" * 80)
    print("CLI OUTPUT")
    print("=" * 80)
    cli_output = phase5.get_cli_output(phase4_result)
    print(cli_output)
    
    # Generate JSON output
    print("\n" + "=" * 80)
    print("JSON OUTPUT")
    print("=" * 80)
    json_output = phase5.get_json_output(phase4_result)
    print(json_output)
    
    # Generate API response
    print("\n" + "=" * 80)
    print("API RESPONSE")
    print("=" * 80)
    api_response = phase5.get_api_response(phase4_result)
    print(json.dumps(api_response, indent=2))
    
    # Generate comparison summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    summary = phase5.create_comparison_summary(
        phase4_result,
        summary_type=SummaryType.QUICK_COMPARISON
    )
    print(f"Title: {summary.title}")
    print(f"Type: {summary.summary_type.value}")
    print("Insights:")
    for insight in summary.insights:
        print(f"  - {insight}")
    print("Recommendations:")
    for rec in summary.recommendations:
        print(f"  - {rec}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run example
    example_usage()
