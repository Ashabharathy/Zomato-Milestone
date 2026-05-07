"""
Voice Search Service Implementation

Advanced voice recognition and natural language processing
for restaurant search and recommendations.
"""

import speech_recognition as sr
import pyttsx3
import spacy
import re
from typing import Dict, List, Optional, Tuple
import json
import logging
from dataclasses import dataclass
from enum import Enum


class SearchIntent(Enum):
    """Types of search intents"""
    RESTAURANT_SEARCH = "restaurant_search"
    CUISINE_SEARCH = "cuisine_search"
    LOCATION_SEARCH = "location_search"
    PRICE_SEARCH = "price_search"
    RATING_SEARCH = "rating_search"
    AMENITY_SEARCH = "amenity_search"


@dataclass
class SearchQuery:
    """Structured search query from voice input"""
    intent: SearchIntent
    entities: Dict[str, str]
    original_text: str
    confidence: float


@dataclass
class VoiceSearchResult:
    """Voice search result with recommendations"""
    query: SearchQuery
    recommendations: List[Dict]
    response_text: str
    confidence: float


class VoiceSearchEngine:
    """Advanced voice search engine for restaurant recommendations"""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.nlp = self._load_nlp_model()
        self.logger = self._setup_logging()
        
        # Configure speech recognition
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Configure TTS
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
    
    def _load_nlp_model(self):
        """Load spaCy NLP model"""
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy model not found. Using basic NLP.")
            return None
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def listen_for_voice(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                self.logger.info("🎤 Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                self.logger.info("🎤 Listening for voice input...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
                self.logger.info("🔍 Processing speech...")
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.logger.info(f"✅ Recognized: {text}")
                    return text
                except sr.UnknownValueError:
                    self.logger.warning("❌ Google Speech Recognition could not understand audio")
                    
                    # Fallback to Sphinx
                    try:
                        text = self.recognizer.recognize_sphinx(audio)
                        self.logger.info(f"✅ Recognized (Sphinx): {text}")
                        return text
                    except sr.UnknownValueError:
                        self.logger.error("❌ Could not understand audio with any engine")
                        return None
                        
        except sr.RequestError as e:
            self.logger.error(f"❌ Speech recognition service error: {e}")
            return None
        except sr.WaitTimeoutError:
            self.logger.warning("⏰ No speech detected within timeout")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in voice recognition: {e}")
            return None
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """Extract entities from text using NLP"""
        entities = {}
        
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract named entities
            for ent in doc.ents:
                entities[ent.label_.lower()] = ent.text
        
        # Extract patterns with regex
        patterns = {
            'cuisine': r'\b(italian|chinese|indian|mexican|american|thai|japanese|french|greek|spanish)\b',
            'price_range': r'\b(\$+|cheap|expensive|affordable|moderate|budget|luxury)\b',
            'rating': r'\b(\d+ stars?|\d\.?\d stars?|excellent|good|great|amazing|fantastic)\b',
            'location': r'\b(near|in|at|around)\s+([a-zA-Z\s]+)',
            'amenity': r'\b(outdoor|parking|wifi|delivery|takeout|reservation|bar|lounge)\b',
            'distance': r'\b(\d+ miles?|\d+ km|\d+ kilometers?)\b'
        }
        
        for entity_type, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities[entity_type] = match.group(0)
        
        return entities
    
    def classify_intent(self, text: str, entities: Dict[str, str]) -> SearchIntent:
        """Classify the intent of the search query"""
        text_lower = text.lower()
        
        # Priority-based intent classification
        if 'cuisine' in entities:
            return SearchIntent.CUISINE_SEARCH
        elif 'price_range' in entities:
            return SearchIntent.PRICE_SEARCH
        elif 'rating' in entities:
            return SearchIntent.RATING_SEARCH
        elif 'amenity' in entities:
            return SearchIntent.AMENITY_SEARCH
        elif 'location' in entities or any(word in text_lower for word in ['near', 'in', 'around']):
            return SearchIntent.LOCATION_SEARCH
        else:
            return SearchIntent.RESTAURANT_SEARCH
    
    def process_voice_query(self, audio_file: Optional[str] = None) -> Optional[SearchQuery]:
        """Process voice query and return structured search query"""
        if audio_file:
            # Process from file
            try:
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
            except Exception as e:
                self.logger.error(f"❌ Error processing audio file: {e}")
                return None
        else:
            # Listen for voice input
            text = self.listen_for_voice()
        
        if not text:
            return None
        
        # Extract entities
        entities = self.extract_entities(text)
        
        # Classify intent
        intent = self.classify_intent(text, entities)
        
        # Calculate confidence (simple heuristic)
        confidence = min(1.0, len(entities) * 0.2 + 0.4)
        
        return SearchQuery(
            intent=intent,
            entities=entities,
            original_text=text,
            confidence=confidence
        )
    
    def generate_recommendations(self, query: SearchQuery) -> List[Dict]:
        """Generate recommendations based on voice query"""
        # Mock recommendations - in real implementation, this would call the API
        recommendations = []
        
        base_restaurants = [
            {"name": "Bella Italia", "cuisine": "Italian", "rating": 4.5, "price": "$$", "location": "Downtown"},
            {"name": "Golden Dragon", "cuisine": "Chinese", "rating": 4.2, "price": "$", "location": "Chinatown"},
            {"name": "Spice Garden", "cuisine": "Indian", "rating": 4.7, "price": "$$", "location": "Midtown"},
            {"name": "Taco Fiesta", "cuisine": "Mexican", "rating": 4.3, "price": "$", "location": "West Side"},
            {"name": "The Steakhouse", "cuisine": "American", "rating": 4.8, "price": "$$$", "location": "Uptown"}
        ]
        
        # Filter based on query entities
        filtered_restaurants = base_restaurants.copy()
        
        if 'cuisine' in query.entities:
            cuisine = query.entities['cuisine'].lower()
            filtered_restaurants = [r for r in filtered_restaurants 
                                  if r['cuisine'].lower() == cuisine]
        
        if 'price_range' in query.entities:
            price = query.entities['price_range'].lower()
            if 'cheap' in price or '$' in price and price.count('$') == 1:
                filtered_restaurants = [r for r in filtered_restaurants if r['price'] == '$']
            elif 'expensive' in price or price.count('$') >= 3:
                filtered_restaurants = [r for r in filtered_restaurants if r['price'] == '$$$']
            else:
                filtered_restaurants = [r for r in filtered_restaurants if r['price'] == '$$']
        
        if 'rating' in query.entities:
            rating_text = query.entities['rating'].lower()
            if 'excellent' in rating_text or '5' in rating_text:
                filtered_restaurants = [r for r in filtered_restaurants if r['rating'] >= 4.5]
            elif 'good' in rating_text or '4' in rating_text:
                filtered_restaurants = [r for r in filtered_restaurants if r['rating'] >= 4.0]
        
        # Return top 3 recommendations
        recommendations = filtered_restaurants[:3]
        
        return recommendations
    
    def generate_response(self, query: SearchQuery, recommendations: List[Dict]) -> str:
        """Generate natural language response"""
        if not recommendations:
            return "I'm sorry, I couldn't find any restaurants matching your criteria."
        
        response_parts = [f"I found {len(recommendations)} great restaurants for you:"]
        
        for i, restaurant in enumerate(recommendations, 1):
            response_parts.append(
                f"Number {i}: {restaurant['name']}, "
                f"{restaurant['cuisine']} cuisine with {restaurant['rating']} stars, "
                f"located in {restaurant['location']}, price range {restaurant['price']}."
            )
        
        response_parts.append("Would you like more details about any of these restaurants?")
        
        return " ".join(response_parts)
    
    def speak_response(self, text: str) -> bool:
        """Convert text to speech"""
        try:
            self.logger.info(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"❌ Error in text-to-speech: {e}")
            return False
    
    def process_voice_search(self, audio_file: Optional[str] = None, speak_response: bool = True) -> Optional[VoiceSearchResult]:
        """Complete voice search pipeline"""
        try:
            # Process voice query
            query = self.process_voice_query(audio_file)
            
            if not query:
                if speak_response:
                    self.speak_response("I'm sorry, I didn't catch that. Could you please repeat?")
                return None
            
            self.logger.info(f"🔍 Processed query: {query.original_text}")
            self.logger.info(f"🎯 Intent: {query.intent.value}")
            self.logger.info(f"📊 Entities: {query.entities}")
            
            # Generate recommendations
            recommendations = self.generate_recommendations(query)
            
            # Generate response
            response_text = self.generate_response(query, recommendations)
            
            # Speak response if requested
            if speak_response:
                self.speak_response(response_text)
            
            return VoiceSearchResult(
                query=query,
                recommendations=recommendations,
                response_text=response_text,
                confidence=query.confidence
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error in voice search pipeline: {e}")
            if speak_response:
                self.speak_response("I'm sorry, I encountered an error while processing your request.")
            return None


def main():
    """Example usage of Voice Search Engine"""
    print("🎤 Voice Search Engine for Restaurant Recommendations")
    print("🚀 Initializing voice search...")
    
    # Initialize voice search engine
    voice_engine = VoiceSearchEngine()
    
    print("🎤 Voice search engine ready!")
    print("📝 Say something like: 'Find me Italian restaurants near downtown' or 'Show me cheap Chinese food'")
    print("🔊 Press Ctrl+C to exit")
    
    try:
        while True:
            print("\n" + "="*50)
            print("🎤 Listening for your voice command...")
            
            # Process voice search
            result = voice_engine.process_voice_search(speak_response=True)
            
            if result:
                print(f"✅ Query: {result.query.original_text}")
                print(f"🎯 Intent: {result.query.intent.value}")
                print(f"📊 Entities: {result.query.entities}")
                print(f"🔊 Response: {result.response_text}")
                print(f"⭐ Found {len(result.recommendations)} recommendations")
                
                for i, rec in enumerate(result.recommendations, 1):
                    print(f"  {i}. {rec['name']} - {rec['cuisine']} ({rec['rating']}⭐)")
            else:
                print("❌ No valid query detected")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
