"""
Phase 5: Response Assembly and Presentation Layer
Main package initialization for Phase 5 components.
"""

from .phase5_integration import (
    Phase5Integration,
    Phase5Config,
    Phase5Result,
    create_phase5_integration
)

from .result_formatter import (
    ResultFormatter,
    OutputFormat,
    FormattedResult,
    FormattedRecommendation
)

from .output_renderer import (
    OutputRenderer,
    RenderTarget,
    ResponseFormat,
    RenderedOutput
)

from .summary_generator import (
    SummaryGenerator,
    SummaryType,
    SummaryResult,
    ComparisonPoint
)

__version__ = "1.0.0"
__description__ = "Phase 5: Response Assembly and Presentation Layer"

__all__ = [
    # Main integration
    "Phase5Integration",
    "Phase5Config",
    "Phase5Result",
    "create_phase5_integration",
    
    # Data structures
    "FormattedResult",
    "FormattedRecommendation",
    "RenderedOutput",
    "SummaryResult",
    "ComparisonPoint",
    
    # Components
    "ResultFormatter",
    "OutputRenderer",
    "SummaryGenerator",
    
    # Enums and types
    "OutputFormat",
    "RenderTarget",
    "ResponseFormat",
    "SummaryType"
]
