"""
Output Renderer Module for Phase 5: Response Assembly and Presentation Layer
Renders formatted recommendations for CLI, Web, and API responses.
"""

import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

from .result_formatter import FormattedResult, OutputFormat, FormattedRecommendation


class RenderTarget(Enum):
    """Target output platforms"""
    CLI = "cli"
    WEB = "web"
    API = "api"
    MOBILE = "mobile"


class ResponseFormat(Enum):
    """Response format types"""
    TEXT = "text"
    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"


@dataclass
class RenderedOutput:
    """Rendered output data"""
    content: str
    format_type: ResponseFormat
    target: RenderTarget
    metadata: Dict[str, Any]
    content_type: str
    success: bool


class OutputRenderer:
    """Renders formatted recommendations for different output targets"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize templates
        self.cli_templates = self._init_cli_templates()
        self.web_templates = self._init_web_templates()
        self.api_templates = self._init_api_templates()
    
    def render(
        self, 
        formatted_result: FormattedResult,
        target: RenderTarget = RenderTarget.CLI,
        response_format: Optional[ResponseFormat] = None
    ) -> RenderedOutput:
        """
        Render formatted result for specified target
        
        Args:
            formatted_result: Formatted result from ResultFormatter
            target: Target platform (cli, web, api, mobile)
            response_format: Specific response format (if None, uses target default)
            
        Returns:
            RenderedOutput with rendered content
        """
        try:
            # Determine response format
            if response_format is None:
                response_format = self._get_default_format(target)
            
            # Route to appropriate renderer
            if target == RenderTarget.CLI:
                content = self._render_cli(formatted_result, response_format)
                content_type = self._get_content_type(response_format)
            elif target == RenderTarget.WEB:
                content = self._render_web(formatted_result, response_format)
                content_type = self._get_content_type(response_format)
            elif target == RenderTarget.API:
                content = self._render_api(formatted_result, response_format)
                content_type = self._get_content_type(response_format)
            elif target == RenderTarget.MOBILE:
                content = self._render_mobile(formatted_result, response_format)
                content_type = self._get_content_type(response_format)
            else:
                raise ValueError(f"Unsupported target: {target}")
            
            # Create metadata
            metadata = {
                "target": target.value,
                "format": response_format.value,
                "rendered_at": datetime.now().isoformat(),
                "content_length": len(content),
                "recommendation_count": formatted_result.total_count
            }
            
            return RenderedOutput(
                content=content,
                format_type=response_format,
                target=target,
                metadata=metadata,
                content_type=content_type,
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Error rendering output: {str(e)}")
            return self._create_error_output(str(e), target, response_format)
    
    def _get_default_format(self, target: RenderTarget) -> ResponseFormat:
        """Get default response format for target"""
        defaults = {
            RenderTarget.CLI: ResponseFormat.TEXT,
            RenderTarget.WEB: ResponseFormat.HTML,
            RenderTarget.API: ResponseFormat.JSON,
            RenderTarget.MOBILE: ResponseFormat.JSON
        }
        return defaults.get(target, ResponseFormat.TEXT)
    
    def _get_content_type(self, response_format: ResponseFormat) -> str:
        """Get HTTP content type for response format"""
        content_types = {
            ResponseFormat.TEXT: "text/plain",
            ResponseFormat.HTML: "text/html",
            ResponseFormat.JSON: "application/json",
            ResponseFormat.MARKDOWN: "text/markdown"
        }
        return content_types.get(response_format, "text/plain")
    
    def _render_cli(self, formatted_result: FormattedResult, response_format: ResponseFormat) -> str:
        """Render for CLI output"""
        if response_format == ResponseFormat.TEXT:
            return self._render_cli_text(formatted_result)
        elif response_format == ResponseFormat.MARKDOWN:
            return self._render_cli_markdown(formatted_result)
        elif response_format == ResponseFormat.JSON:
            return self._render_cli_json(formatted_result)
        else:
            return self._render_cli_text(formatted_result)
    
    def _render_cli_text(self, formatted_result: FormattedResult) -> str:
        """Render CLI text output"""
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("RESTAURANT RECOMMENDATIONS")
        lines.append("=" * 80)
        
        # Summary
        lines.append(f"Total Recommendations: {formatted_result.total_count}")
        lines.append(f"Format: {formatted_result.format_type.value}")
        if formatted_result.metadata.get("processing_time"):
            lines.append(f"Processing Time: {formatted_result.metadata['processing_time']:.2f}s")
        
        # Recommendations
        lines.append("\n" + "-" * 80)
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        
        for rec in formatted_result.recommendations:
            lines.append(f"\n{rec.rank}. {rec.restaurant_name} (Score: {rec.score:.2f})")
            
            if rec.cuisine:
                lines.append(f"   Cuisine: {rec.cuisine}")
            if rec.rating:
                lines.append(f"   Rating: {rec.rating}/5")
            if rec.price_range:
                lines.append(f"   Price: {rec.price_range}")
            if rec.avg_cost_for_two:
                lines.append(f"   Avg Cost for Two: ${rec.avg_cost_for_two}")
            
            if rec.explanation:
                lines.append(f"   Explanation: {rec.explanation}")
            
            if rec.highlights:
                lines.append(f"   Highlights: {', '.join(rec.highlights)}")
            
            if rec.considerations:
                lines.append(f"   Considerations: {', '.join(rec.considerations)}")
        
        # Summary and alternatives
        if formatted_result.summary:
            lines.append("\n" + "-" * 80)
            lines.append("SUMMARY")
            lines.append("-" * 80)
            lines.append(formatted_result.summary)
        
        if formatted_result.alternatives:
            lines.append("\n" + "-" * 80)
            lines.append("ALTERNATIVES")
            lines.append("-" * 80)
            lines.append(formatted_result.alternatives)
        
        lines.append("\n" + "=" * 80)
        
        return "\n".join(lines)
    
    def _render_cli_markdown(self, formatted_result: FormattedResult) -> str:
        """Render CLI markdown output"""
        lines = []
        
        # Header
        lines.append("# Restaurant Recommendations")
        lines.append(f"**Total Recommendations:** {formatted_result.total_count}")
        lines.append(f"**Format:** {formatted_result.format_type.value}")
        
        # Metadata
        if formatted_result.metadata.get("processing_time"):
            lines.append(f"**Processing Time:** {formatted_result.metadata['processing_time']:.2f}s")
        
        # Recommendations
        lines.append("\n## Recommendations")
        
        for rec in formatted_result.recommendations:
            lines.append(f"\n### {rec.rank}. {rec.restaurant_name}")
            lines.append(f"**Score:** {rec.score:.2f}")
            
            if rec.cuisine:
                lines.append(f"**Cuisine:** {rec.cuisine}")
            if rec.rating:
                lines.append(f"**Rating:** {rec.rating}/5")
            if rec.price_range:
                lines.append(f"**Price:** {rec.price_range}")
            if rec.avg_cost_for_two:
                lines.append(f"**Avg Cost for Two:** ${rec.avg_cost_for_two}")
            
            if rec.explanation:
                lines.append(f"\n**Explanation:** {rec.explanation}")
            
            if rec.highlights:
                lines.append(f"\n**Highlights:**")
                for highlight in rec.highlights:
                    lines.append(f"- {highlight}")
            
            if rec.considerations:
                lines.append(f"\n**Considerations:**")
                for consideration in rec.considerations:
                    lines.append(f"- {consideration}")
        
        # Summary and alternatives
        if formatted_result.summary:
            lines.append("\n## Summary")
            lines.append(formatted_result.summary)
        
        if formatted_result.alternatives:
            lines.append("\n## Alternatives")
            lines.append(formatted_result.alternatives)
        
        return "\n".join(lines)
    
    def _render_cli_json(self, formatted_result: FormattedResult) -> str:
        """Render CLI JSON output"""
        return json.dumps({
            "success": formatted_result.success,
            "total_count": formatted_result.total_count,
            "format_type": formatted_result.format_type.value,
            "summary": formatted_result.summary,
            "alternatives": formatted_result.alternatives,
            "metadata": formatted_result.metadata,
            "recommendations": [
                {
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
                for rec in formatted_result.recommendations
            ]
        }, indent=2)
    
    def _render_web(self, formatted_result: FormattedResult, response_format: ResponseFormat) -> str:
        """Render for Web output"""
        if response_format == ResponseFormat.HTML:
            return self._render_web_html(formatted_result)
        elif response_format == ResponseFormat.JSON:
            return self._render_web_json(formatted_result)
        else:
            return self._render_web_html(formatted_result)
    
    def _render_web_html(self, formatted_result: FormattedResult) -> str:
        """Render web HTML output"""
        html = []
        
        # HTML structure
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("    <meta charset='UTF-8'>")
        html.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("    <title>Restaurant Recommendations</title>")
        html.append("    <style>")
        html.append(self._get_web_css())
        html.append("    </style>")
        html.append("</head>")
        html.append("<body>")
        
        # Header
        html.append("    <div class='container'>")
        html.append("        <header>")
        html.append("            <h1>Restaurant Recommendations</h1>")
        html.append(f"            <p class='meta'>Total: {formatted_result.total_count} recommendations</p>")
        if formatted_result.metadata.get("processing_time"):
            html.append(f"            <p class='meta'>Generated in {formatted_result.metadata['processing_time']:.2f}s</p>")
        html.append("        </header>")
        
        # Recommendations
        html.append("        <main>")
        html.append("            <div class='recommendations'>")
        
        for rec in formatted_result.recommendations:
            html.append(f"                <div class='recommendation-card'>")
            html.append(f"                    <div class='rank'>#{rec.rank}</div>")
            html.append(f"                    <div class='content'>")
            html.append(f"                        <h2>{rec.restaurant_name}</h2>")
            html.append(f"                        <div class='score'>Score: {rec.score:.2f}</div>")
            
            if rec.cuisine or rec.rating or rec.price_range:
                html.append(f"                        <div class='details'>")
                if rec.cuisine:
                    html.append(f"                            <span class='cuisine'>{rec.cuisine}</span>")
                if rec.rating:
                    html.append(f"                            <span class='rating'>{'&#9733;' * int(rec.rating)} {rec.rating}</span>")
                if rec.price_range:
                    html.append(f"                            <span class='price'>{rec.price_range}</span>")
                html.append(f"                        </div>")
            
            if rec.explanation:
                html.append(f"                        <p class='explanation'>{rec.explanation}</p>")
            
            if rec.highlights:
                html.append(f"                        <div class='highlights'>")
                html.append(f"                            <h4>Highlights:</h4>")
                html.append(f"                            <ul>")
                for highlight in rec.highlights:
                    html.append(f"                                <li>{highlight}</li>")
                html.append(f"                            </ul>")
                html.append(f"                        </div>")
            
            if rec.considerations:
                html.append(f"                        <div class='considerations'>")
                html.append(f"                            <h4>Considerations:</h4>")
                html.append(f"                            <ul>")
                for consideration in rec.considerations:
                    html.append(f"                                <li>{consideration}</li>")
                html.append(f"                            </ul>")
                html.append(f"                        </div>")
            
            html.append(f"                    </div>")
            html.append(f"                </div>")
        
        html.append("            </div>")
        
        # Summary and alternatives
        if formatted_result.summary:
            html.append("            <section class='summary'>")
            html.append("                <h3>Summary</h3>")
            html.append(f"                <p>{formatted_result.summary}</p>")
            html.append("            </section>")
        
        if formatted_result.alternatives:
            html.append("            <section class='alternatives'>")
            html.append("                <h3>Alternatives</h3>")
            html.append(f"                <p>{formatted_result.alternatives}</p>")
            html.append("            </section>")
        
        html.append("        </main>")
        html.append("    </div>")
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
    
    def _render_web_json(self, formatted_result: FormattedResult) -> str:
        """Render web JSON output"""
        return self._render_cli_json(formatted_result)
    
    def _render_api(self, formatted_result: FormattedResult, response_format: ResponseFormat) -> str:
        """Render for API output"""
        if response_format == ResponseFormat.JSON:
            return self._render_api_json(formatted_result)
        else:
            return self._render_api_json(formatted_result)
    
    def _render_api_json(self, formatted_result: FormattedResult) -> str:
        """Render API JSON output"""
        return json.dumps({
            "success": formatted_result.success,
            "data": {
                "recommendations": [
                    {
                        "id": rec.rank,
                        "name": rec.restaurant_name,
                        "score": rec.score,
                        "explanation": rec.explanation,
                        "attributes": {
                            "cuisine": rec.cuisine,
                            "rating": rec.rating,
                            "price_range": rec.price_range,
                            "avg_cost_for_two": rec.avg_cost_for_two,
                            "location": rec.location,
                            "address": rec.address,
                            "features": rec.features or []
                        },
                        "highlights": rec.highlights or [],
                        "considerations": rec.considerations or []
                    }
                    for rec in formatted_result.recommendations
                ],
                "summary": formatted_result.summary,
                "alternatives": formatted_result.alternatives,
                "pagination": {
                    "total": formatted_result.total_count,
                    "page": 1,
                    "per_page": formatted_result.total_count
                }
            },
            "metadata": formatted_result.metadata
        }, indent=2)
    
    def _render_mobile(self, formatted_result: FormattedResult, response_format: ResponseFormat) -> str:
        """Render for mobile output"""
        if response_format == ResponseFormat.JSON:
            return self._render_mobile_json(formatted_result)
        else:
            return self._render_mobile_json(formatted_result)
    
    def _render_mobile_json(self, formatted_result: FormattedResult) -> str:
        """Render mobile JSON output"""
        return json.dumps({
            "success": formatted_result.success,
            "ui_data": {
                "header": {
                    "title": "Restaurant Recommendations",
                    "subtitle": f"{formatted_result.total_count} places found"
                },
                "recommendations": [
                    {
                        "id": rec.rank,
                        "title": rec.restaurant_name,
                        "subtitle": rec.cuisine or "Restaurant",
                        "rating": rec.rating,
                        "price": rec.price_range,
                        "score": rec.score,
                        "description": rec.explanation,
                        "tags": rec.highlights or [],
                        "warnings": rec.considerations or [],
                        "metadata": {
                            "avg_cost": rec.avg_cost_for_two,
                            "location": rec.location
                        }
                    }
                    for rec in formatted_result.recommendations
                ],
                "footer": {
                    "summary": formatted_result.summary,
                    "alternatives": formatted_result.alternatives
                }
            },
            "metadata": formatted_result.metadata
        }, indent=2)
    
    def _get_web_css(self) -> str:
        """Get CSS styles for web output"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .meta {
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .recommendations {
            display: grid;
            gap: 20px;
        }
        
        .recommendation-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            gap: 20px;
        }
        
        .rank {
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
            min-width: 40px;
        }
        
        .content {
            flex: 1;
        }
        
        .content h2 {
            margin: 0 0 8px 0;
            color: #2c3e50;
        }
        
        .score {
            background: #27ae60;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 12px;
        }
        
        .details {
            display: flex;
            gap: 12px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        
        .cuisine, .rating, .price {
            background: #ecf0f1;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .explanation {
            color: #555;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        
        .highlights, .considerations {
            margin-bottom: 12px;
        }
        
        .highlights h4, .considerations h4 {
            margin: 0 0 8px 0;
            color: #2c3e50;
            font-size: 14px;
        }
        
        .highlights ul, .considerations ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .highlights li, .considerations li {
            margin-bottom: 4px;
            font-size: 14px;
        }
        
        .summary, .alternatives {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        
        .summary h3, .alternatives h3 {
            margin: 0 0 12px 0;
            color: #2c3e50;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .recommendation-card {
                flex-direction: column;
                gap: 12px;
            }
            
            .rank {
                min-width: auto;
            }
        }
        """
    
    def _create_error_output(self, error_message: str, target: RenderTarget, response_format: ResponseFormat) -> RenderedOutput:
        """Create error output"""
        error_content = json.dumps({
            "success": False,
            "error": error_message,
            "target": target.value,
            "format": response_format.value
        }, indent=2)
        
        return RenderedOutput(
            content=error_content,
            format_type=response_format,
            target=target,
            metadata={"error": error_message},
            content_type="application/json",
            success=False
        )
    
    def _init_cli_templates(self) -> Dict[str, str]:
        """Initialize CLI templates"""
        return {
            "text_header": "=" * 80 + "\n{title}\n" + "=" * 80,
            "text_recommendation": "{rank}. {name} (Score: {score})\n{details}\n{explanation}\n{highlights}",
            "json_template": "{{\"success\": {success}, \"data\": {data}}}"
        }
    
    def _init_web_templates(self) -> Dict[str, str]:
        """Initialize web templates"""
        return {
            "html_template": "<!DOCTYPE html>...",
            "css_template": "body { font-family: ... }"
        }
    
    def _init_api_templates(self) -> Dict[str, str]:
        """Initialize API templates"""
        return {
            "json_template": "{{\"success\": {success}, \"data\": {data}}}",
            "error_template": "{{\"success\": false, \"error\": {error}}}"
        }
