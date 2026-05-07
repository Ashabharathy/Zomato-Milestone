"""
Phase 4: LLM Recommendation and Reasoning Layer
Main package initialization for Phase 4 components.
"""

from .phase4_integration import (
    Phase4Integration,
    Phase4Config,
    Phase4Result,
    create_phase4_integration
)

from .prompt_builder import (
    PromptBuilder,
    UserPreference,
    Restaurant
)

from .llm_inference import (
    GroqInference,
    MockGroqInference,
    LLMResponse,
    create_inference_client
)

from .response_parser import (
    ResponseParser,
    ParsedResponse,
    Recommendation
)

from .guardrails import (
    Guardrails,
    GuardrailResult,
    ValidationResult,
    ValidationLevel
)

__version__ = "1.0.0"
__description__ = "Phase 4: LLM Recommendation and Reasoning Layer using Groq API"

__all__ = [
    # Main integration
    "Phase4Integration",
    "Phase4Config", 
    "Phase4Result",
    "create_phase4_integration",
    
    # Data structures
    "UserPreference",
    "Restaurant",
    "Recommendation",
    "ParsedResponse",
    "LLMResponse",
    "ValidationResult",
    "GuardrailResult",
    
    # Components
    "PromptBuilder",
    "GroqInference",
    "MockGroqInference",
    "ResponseParser",
    "Guardrails",
    
    # Utilities
    "create_inference_client",
    "ValidationLevel"
]
