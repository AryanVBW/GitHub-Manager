"""
AI service abstraction supporting multiple providers (Gemini and OpenAI).
Includes user-specific response analysis and personalization.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
import time
import re

from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class UserAnalyzer:
    """Analyzes user writing style and interaction patterns."""

    @staticmethod
    def analyze_writing_style(user_comments: List[str]) -> Dict[str, Any]:
        """
        Analyze a user's writing style from their comment history.

        Args:
            user_comments: List of user's previous comments

        Returns:
            Dictionary with writing style characteristics
        """
        if not user_comments:
            return {
                "avg_length": 0,
                "tone": "neutral",
                "formality": "neutral",
                "uses_emojis": False,
                "avg_sentences": 0
            }

        total_length = sum(len(comment) for comment in user_comments)
        avg_length = total_length / len(user_comments)

        # Check for emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            "]+", flags=re.UNICODE)
        uses_emojis = any(emoji_pattern.search(comment) for comment in user_comments)

        # Count sentences (rough estimate)
        total_sentences = sum(comment.count('.') + comment.count('!') + comment.count('?')
                            for comment in user_comments)
        avg_sentences = total_sentences / len(user_comments) if total_sentences > 0 else 1

        # Determine formality (simple heuristic)
        formal_indicators = ['please', 'thank you', 'would', 'could', 'kindly']
        casual_indicators = ['hey', 'yeah', 'cool', 'awesome', 'lol', 'btw']

        formal_count = sum(
            sum(1 for indicator in formal_indicators if indicator in comment.lower())
            for comment in user_comments
        )
        casual_count = sum(
            sum(1 for indicator in casual_indicators if indicator in comment.lower())
            for comment in user_comments
        )

        if formal_count > casual_count * 1.5:
            formality = "formal"
        elif casual_count > formal_count * 1.5:
            formality = "casual"
        else:
            formality = "neutral"

        # Determine tone
        positive_indicators = ['thanks', 'great', 'awesome', 'excellent', 'good', 'appreciate']
        question_indicators = ['?', 'how', 'what', 'why', 'when', 'where']

        positive_count = sum(
            sum(1 for indicator in positive_indicators if indicator in comment.lower())
            for comment in user_comments
        )
        question_count = sum(
            sum(1 for indicator in question_indicators if indicator in comment.lower())
            for comment in user_comments
        )

        if positive_count > len(user_comments) * 0.5:
            tone = "positive"
        elif question_count > len(user_comments) * 0.5:
            tone = "inquisitive"
        else:
            tone = "neutral"

        return {
            "avg_length": int(avg_length),
            "tone": tone,
            "formality": formality,
            "uses_emojis": uses_emojis,
            "avg_sentences": round(avg_sentences, 1)
        }

    @staticmethod
    def build_personalized_context(
        user_style: Dict[str, Any],
        base_context: str
    ) -> str:
        """
        Build personalized context based on user's writing style.

        Args:
            user_style: User's writing style characteristics
            base_context: Base context about the issue/PR

        Returns:
            Enhanced context with personalization instructions
        """
        personalization = "\n\nPersonalization Guidelines:\n"

        # Adjust response length
        if user_style["avg_length"] < 100:
            personalization += "- Keep response very brief (1-2 sentences)\n"
        elif user_style["avg_length"] < 300:
            personalization += "- Keep response concise (2-3 sentences)\n"
        else:
            personalization += "- Provide detailed response (3-5 sentences)\n"

        # Adjust formality
        if user_style["formality"] == "formal":
            personalization += "- Use formal, professional language\n"
        elif user_style["formality"] == "casual":
            personalization += "- Use friendly, casual language\n"
        else:
            personalization += "- Use balanced, professional yet friendly language\n"

        # Adjust tone
        if user_style["tone"] == "positive":
            personalization += "- Match their positive, enthusiastic tone\n"
        elif user_style["tone"] == "inquisitive":
            personalization += "- Be thorough and educational in your response\n"

        # Emoji usage
        if user_style["uses_emojis"]:
            personalization += "- Feel free to use appropriate emojis\n"
        else:
            personalization += "- Avoid using emojis\n"

        return base_context + personalization


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        """
        Generate a response using the AI provider.
        
        Args:
            prompt: The prompt/question to respond to
            context: Additional context for the response
        
        Returns:
            Generated response or None if failed
        """
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""

    def __init__(self):
        """Initialize Gemini provider."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            logger.info(f"Gemini AI provider initialized successfully with model: {Config.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini provider: {e}")
            raise
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        """Generate response using Gemini."""
        try:
            full_prompt = self._build_prompt(prompt, context)
            
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                logger.debug("Successfully generated response with Gemini")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return None
        
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {e}")
            return None
    
    def _build_prompt(self, prompt: str, context: Optional[str] = None) -> str:
        """Build the full prompt with context."""
        system_instruction = Config.SYSTEM_PROMPT

        if context:
            return f"{system_instruction}\n\nContext:\n{context}\n\nUser message:\n{prompt}\n\nResponse:"
        else:
            return f"{system_instruction}\n\nUser message:\n{prompt}\n\nResponse:"


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""

    def __init__(self):
        """Initialize OpenAI provider."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
            logger.info(f"OpenAI provider initialized successfully with model: {Config.OPENAI_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {e}")
            raise
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        """Generate response using OpenAI."""
        try:
            messages = self._build_messages(prompt, context)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            if response.choices and response.choices[0].message.content:
                logger.debug("Successfully generated response with OpenAI")
                return response.choices[0].message.content.strip()
            else:
                logger.warning("OpenAI returned empty response")
                return None
        
        except Exception as e:
            logger.error(f"Error generating response with OpenAI: {e}")
            return None
    
    def _build_messages(self, prompt: str, context: Optional[str] = None) -> list:
        """Build messages array for OpenAI."""
        system_message = {
            "role": "system",
            "content": Config.SYSTEM_PROMPT
        }

        if context:
            user_message = {
                "role": "user",
                "content": f"Context:\n{context}\n\nUser message:\n{prompt}"
            }
        else:
            user_message = {
                "role": "user",
                "content": prompt
            }

        return [system_message, user_message]


class AIService:
    """Main AI service that manages provider selection and fallback."""
    
    def __init__(self):
        """Initialize AI service with configured provider."""
        self.provider: Optional[AIProvider] = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the configured AI provider."""
        try:
            if Config.AI_PROVIDER == "gemini":
                self.provider = GeminiProvider()
            elif Config.AI_PROVIDER == "openai":
                self.provider = OpenAIProvider()
            else:
                raise ValueError(f"Unsupported AI provider: {Config.AI_PROVIDER}")
            
            logger.info(f"AI service initialized with provider: {Config.AI_PROVIDER}")
        
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            raise
    
    def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        max_retries: int = 3
    ) -> Optional[str]:
        """
        Generate a response with retry logic.
        
        Args:
            prompt: The prompt/question to respond to
            context: Additional context for the response
            max_retries: Maximum number of retry attempts
        
        Returns:
            Generated response or None if all attempts failed
        """
        for attempt in range(max_retries):
            try:
                response = self.provider.generate_response(prompt, context)
                if response:
                    return response
                
                logger.warning(f"Attempt {attempt + 1}/{max_retries} returned empty response")
            
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        logger.error("All attempts to generate AI response failed")
        return None
    
    def generate_issue_response(
        self,
        comment_text: str,
        issue_context: str,
        user_comments: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Generate a personalized response to an issue comment.

        Args:
            comment_text: The comment to respond to
            issue_context: Context about the issue
            user_comments: User's previous comments for style analysis

        Returns:
            Generated response
        """
        # Analyze user's writing style if comments provided
        if user_comments:
            user_style = UserAnalyzer.analyze_writing_style(user_comments)
            enhanced_context = UserAnalyzer.build_personalized_context(user_style, issue_context)
            logger.debug(f"Generated personalized context based on user style: {user_style}")
            return self.generate_response(comment_text, enhanced_context)

        return self.generate_response(comment_text, issue_context)

    def generate_pr_response(
        self,
        comment_text: str,
        pr_context: str,
        user_comments: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Generate a personalized response to a pull request comment.

        Args:
            comment_text: The comment to respond to
            pr_context: Context about the pull request
            user_comments: User's previous comments for style analysis

        Returns:
            Generated response
        """
        # Analyze user's writing style if comments provided
        if user_comments:
            user_style = UserAnalyzer.analyze_writing_style(user_comments)
            enhanced_context = UserAnalyzer.build_personalized_context(user_style, pr_context)
            logger.debug(f"Generated personalized context based on user style: {user_style}")
            return self.generate_response(comment_text, enhanced_context)

        return self.generate_response(comment_text, pr_context)

