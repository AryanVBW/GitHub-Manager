"""
Configuration management for GitHub Manager application.
Handles environment variables and application settings.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""

    # GitHub Configuration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")

    # AI Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini").lower()
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # AI Model Selection
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")

    # AI System Prompt (Customizable)
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful, humble, and professional GitHub assistant. "
        "Your responses should be concise, respectful, and actionable. "
        "Always maintain a friendly and supportive tone. "
        "Keep responses brief and to the point."
    )

    # Email Configuration (Optional)
    RESEND_API_KEY: Optional[str] = os.getenv("RESEND_API_KEY")
    OWNER_EMAIL: Optional[str] = os.getenv("OWNER_EMAIL")

    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "production")
    PORT: int = int(os.getenv("PORT", "5000"))
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate required configuration.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Required fields
        if not cls.GITHUB_TOKEN:
            errors.append("GITHUB_TOKEN is required")

        if not cls.GITHUB_WEBHOOK_SECRET:
            errors.append("GITHUB_WEBHOOK_SECRET is required")

        # AI Provider validation
        if cls.AI_PROVIDER not in ["gemini", "openai"]:
            errors.append("AI_PROVIDER must be either 'gemini' or 'openai'")

        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when AI_PROVIDER is 'gemini'")

        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when AI_PROVIDER is 'openai'")

        # AI Model validation
        valid_openai_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]
        valid_gemini_models = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]

        if cls.AI_PROVIDER == "openai" and cls.OPENAI_MODEL not in valid_openai_models:
            errors.append(f"OPENAI_MODEL must be one of: {', '.join(valid_openai_models)}")

        if cls.AI_PROVIDER == "gemini" and cls.GEMINI_MODEL not in valid_gemini_models:
            errors.append(f"GEMINI_MODEL must be one of: {', '.join(valid_gemini_models)}")

        return len(errors) == 0, errors
    
    @classmethod
    def has_email_configured(cls) -> bool:
        """Check if email notifications are configured."""
        return bool(cls.RESEND_API_KEY and cls.OWNER_EMAIL)

    @classmethod
    def get_valid_openai_models(cls) -> list[str]:
        """Get list of valid OpenAI models."""
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]

    @classmethod
    def get_valid_gemini_models(cls) -> list[str]:
        """Get list of valid Gemini models."""
        return ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]

