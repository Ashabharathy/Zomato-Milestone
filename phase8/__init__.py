"""
Phase 8: Advanced AI Features and Machine Learning

This module implements cutting-edge AI capabilities including:
- Collaborative filtering with neural networks
- Voice search and natural language processing
- Image recognition for restaurant analysis
- Predictive analytics and real-time personalization
- Advanced recommendation algorithms
"""

__version__ = "1.0.0"
__author__ = "Restaurant Recommendation System"

from .ml_models.collaborative_filtering import NeuralCollaborativeFiltering
from .ai_services.voice_service import VoiceSearchEngine
from .ai_services.vision_service import RestaurantImageAnalyzer
from .real_time.recommendation_engine import RealTimeRecommendationEngine

__all__ = [
    "NeuralCollaborativeFiltering",
    "VoiceSearchEngine", 
    "RestaurantImageAnalyzer",
    "RealTimeRecommendationEngine"
]
