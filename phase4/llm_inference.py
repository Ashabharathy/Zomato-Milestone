"""
LLM Inference Module for Phase 4: LLM Recommendation and Reasoning Layer
Handles Groq API integration for generating restaurant recommendations.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

try:
    from groq import Groq
except ImportError:
    print("Groq library not installed. Please install with: pip install groq")
    Groq = None

from prompt_builder import UserPreference, Restaurant


@dataclass
class LLMResponse:
    """Structured response from LLM inference"""
    content: str
    model_used: str
    tokens_used: Optional[int] = None
    response_time: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None


class GroqInference:
    """Handles LLM inference using Groq API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-70b-8192"):
        """
        Initialize Groq inference client
        
        Args:
            api_key: Groq API key (if None, will try to get from environment)
            model: Groq model to use for inference
        """
        if Groq is None:
            raise ImportError("Groq library is required. Install with: pip install groq")
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter")
        
        self.model = model
        self.client = Groq(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
        
        # Available Groq models (as of current version)
        self.available_models = [
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
        
        if model not in self.available_models:
            self.logger.warning(f"Model {model} may not be available. Available models: {self.available_models}")
    
    def generate_recommendations(
        self, 
        prompt: str, 
        temperature: float = 0.3,
        max_tokens: int = 4096,
        top_p: float = 0.9,
        timeout: int = 30
    ) -> LLMResponse:
        """
        Generate restaurant recommendations using Groq API
        
        Args:
            prompt: Complete prompt for LLM
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            top_p: Top-p sampling parameter
            timeout: Request timeout in seconds
            
        Returns:
            LLMResponse with generated content and metadata
        """
        start_time = time.time()
        
        try:
            # Make API call
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=False,
                timeout=timeout
            )
            
            # Extract response data
            content = chat_completion.choices[0].message.content
            tokens_used = chat_completion.usage.total_tokens if chat_completion.usage else None
            response_time = time.time() - start_time
            
            response = LLMResponse(
                content=content,
                model_used=self.model,
                tokens_used=tokens_used,
                response_time=response_time,
                success=True
            )
            
            self.logger.info(f"Successfully generated response in {response_time:.2f}s using {tokens_used} tokens")
            return response
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f"Groq API error: {str(e)}"
            self.logger.error(error_msg)
            
            return LLMResponse(
                content="",
                model_used=self.model,
                response_time=response_time,
                success=False,
                error_message=error_msg
            )
    
    def generate_with_retry(
        self, 
        prompt: str, 
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        **kwargs
    ) -> LLMResponse:
        """
        Generate recommendations with retry logic for resilience
        
        Args:
            prompt: Complete prompt for LLM
            max_retries: Maximum number of retry attempts
            backoff_factor: Backoff multiplier for retry delays
            **kwargs: Additional arguments for generate_recommendations
            
        Returns:
            LLMResponse from last attempt
        """
        last_response = None
        
        for attempt in range(max_retries + 1):
            if attempt > 0:
                # Exponential backoff
                delay = backoff_factor * (2 ** (attempt - 1))
                self.logger.info(f"Retrying in {delay}s (attempt {attempt + 1}/{max_retries + 1})")
                time.sleep(delay)
            
            response = self.generate_recommendations(prompt, **kwargs)
            
            if response.success:
                return response
            
            last_response = response
            self.logger.warning(f"Attempt {attempt + 1} failed: {response.error_message}")
        
        self.logger.error(f"All {max_retries + 1} attempts failed")
        return last_response
    
    def test_connection(self) -> bool:
        """Test connection to Groq API"""
        try:
            test_prompt = "Hello! Please respond with 'Connection successful' in JSON format."
            response = self.generate_recommendations(test_prompt, max_tokens=50)
            return response.success
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "available_models": self.available_models,
            "connection_test": self.test_connection()
        }


class MockGroqInference:
    """Mock inference for testing without API keys"""
    
    def __init__(self, model: str = "mock-model"):
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def generate_recommendations(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate mock response for testing"""
        mock_response = {
            "recommendations": [
                {
                    "rank": 1,
                    "restaurant_name": "Mock Restaurant 1",
                    "score": 0.95,
                    "explanation": "This is a mock recommendation for testing purposes.",
                    "highlights": ["Great food", "Good service"],
                    "considerations": ["Mock consideration"]
                },
                {
                    "rank": 2,
                    "restaurant_name": "Mock Restaurant 2", 
                    "score": 0.85,
                    "explanation": "Another mock recommendation for testing.",
                    "highlights": ["Nice ambiance", "Reasonable prices"],
                    "considerations": ["Mock consideration 2"]
                }
            ],
            "summary": "Mock summary of recommendations",
            "alternatives": "Mock alternatives suggestion"
        }
        
        return LLMResponse(
            content=json.dumps(mock_response, indent=2),
            model_used=self.model,
            response_time=0.1,
            success=True
        )
    
    def generate_with_retry(self, prompt: str, **kwargs) -> LLMResponse:
        """Mock version with retry"""
        return self.generate_recommendations(prompt, **kwargs)
    
    def test_connection(self) -> bool:
        """Mock connection test"""
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Mock model info"""
        return {
            "model": self.model,
            "available_models": ["mock-model-1", "mock-model-2"],
            "connection_test": True
        }


def create_inference_client(
    api_key: Optional[str] = None, 
    model: str = "llama3-70b-8192",
    use_mock: bool = False
) -> GroqInference | MockGroqInference:
    """
    Factory function to create inference client
    
    Args:
        api_key: Groq API key
        model: Model to use
        use_mock: Whether to use mock client for testing
        
    Returns:
        Inference client instance
    """
    if use_mock:
        return MockGroqInference(model)
    
    return GroqInference(api_key=api_key, model=model)
