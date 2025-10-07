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
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "")
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    
    # AI Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini").lower()
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
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
        
        if not cls.GITHUB_REPO:
            errors.append("GITHUB_REPO is required")
        
        if not cls.GITHUB_WEBHOOK_SECRET:
            errors.append("GITHUB_WEBHOOK_SECRET is required")
        
        # AI Provider validation
        if cls.AI_PROVIDER not in ["gemini", "openai"]:
            errors.append("AI_PROVIDER must be either 'gemini' or 'openai'")
        
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required when AI_PROVIDER is 'gemini'")
        
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when AI_PROVIDER is 'openai'")
        
        return len(errors) == 0, errors
    
    @classmethod
    def has_email_configured(cls) -> bool:
        """Check if email notifications are configured."""
        return bool(cls.RESEND_API_KEY and cls.OWNER_EMAIL)
    
    @classmethod
    def get_repo_owner_and_name(cls) -> tuple[str, str]:
        """
        Parse repository owner and name from GITHUB_REPO.
        
        Returns:
            Tuple of (owner, repo_name)
        """
        if "/" not in cls.GITHUB_REPO:
            raise ValueError("GITHUB_REPO must be in format 'owner/repo'")
        
        parts = cls.GITHUB_REPO.split("/")
        return parts[0], parts[1]

