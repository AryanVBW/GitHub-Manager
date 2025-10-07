"""
AI service abstraction supporting multiple providers (Gemini and OpenAI).
"""
from abc import ABC, abstractmethod
from typing import Optional
import time

from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


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
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini AI provider initialized successfully")
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
        system_instruction = (
            "You are a helpful, humble, and professional GitHub bot assistant. "
            "Your responses should be concise, respectful, and actionable. "
            "Always maintain a friendly and supportive tone. "
            "Keep responses brief and to the point."
        )
        
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
            self.model = "gpt-3.5-turbo"
            logger.info("OpenAI provider initialized successfully")
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
            "content": (
                "You are a helpful, humble, and professional GitHub bot assistant. "
                "Your responses should be concise, respectful, and actionable. "
                "Always maintain a friendly and supportive tone. "
                "Keep responses brief and to the point."
            )
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
    
    def generate_issue_response(self, comment_text: str, issue_context: str) -> Optional[str]:
        """
        Generate a response to an issue comment.
        
        Args:
            comment_text: The comment to respond to
            issue_context: Context about the issue
        
        Returns:
            Generated response
        """
        return self.generate_response(comment_text, issue_context)
    
    def generate_pr_response(self, comment_text: str, pr_context: str) -> Optional[str]:
        """
        Generate a response to a pull request comment.
        
        Args:
            comment_text: The comment to respond to
            pr_context: Context about the pull request
        
        Returns:
            Generated response
        """
        return self.generate_response(comment_text, pr_context)

