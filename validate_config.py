#!/usr/bin/env python3
"""
Configuration validation script for GitHub Manager.
Run this before deploying to ensure all settings are correct.
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_status(check_name, status, message=""):
    """Print a check status."""
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    
    print(f"{color}{symbol}{reset} {check_name}")
    if message:
        print(f"  → {message}")


def validate_github_config():
    """Validate GitHub configuration."""
    print_header("GitHub Configuration")
    
    token = os.getenv("GITHUB_TOKEN", "")
    repo = os.getenv("GITHUB_REPO", "")
    webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    
    # Check token
    has_token = bool(token)
    print_status("GitHub Token", has_token, 
                 "Set" if has_token else "Missing - Required!")
    
    if has_token:
        if token.startswith("ghp_"):
            print_status("Token Format", True, "Valid personal access token format")
        else:
            print_status("Token Format", False, "Should start with 'ghp_'")
    
    # Check repo
    has_repo = bool(repo)
    print_status("Repository", has_repo,
                 f"{repo}" if has_repo else "Missing - Required!")
    
    if has_repo and "/" in repo:
        owner, name = repo.split("/", 1)
        print_status("Repository Format", True, f"Owner: {owner}, Name: {name}")
    elif has_repo:
        print_status("Repository Format", False, "Should be 'owner/repo'")
    
    # Check webhook secret
    has_secret = bool(webhook_secret)
    print_status("Webhook Secret", has_secret,
                 "Set" if has_secret else "Missing - Required!")
    
    if has_secret and len(webhook_secret) >= 32:
        print_status("Secret Length", True, f"{len(webhook_secret)} characters")
    elif has_secret:
        print_status("Secret Length", False, "Should be at least 32 characters")
    
    return has_token and has_repo and has_secret


def validate_ai_config():
    """Validate AI configuration."""
    print_header("AI Configuration")
    
    provider = os.getenv("AI_PROVIDER", "").lower()
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    # Check provider
    valid_provider = provider in ["gemini", "openai"]
    print_status("AI Provider", valid_provider,
                 f"{provider}" if valid_provider else f"Invalid: {provider} (must be 'gemini' or 'openai')")
    
    # Check keys based on provider
    if provider == "gemini":
        has_key = bool(gemini_key)
        print_status("Gemini API Key", has_key,
                     "Set" if has_key else "Missing - Required for Gemini!")
        return valid_provider and has_key
    
    elif provider == "openai":
        has_key = bool(openai_key)
        print_status("OpenAI API Key", has_key,
                     "Set" if has_key else "Missing - Required for OpenAI!")
        
        if has_key and openai_key.startswith("sk-"):
            print_status("Key Format", True, "Valid OpenAI key format")
        elif has_key:
            print_status("Key Format", False, "Should start with 'sk-'")
        
        return valid_provider and has_key
    
    return False


def validate_email_config():
    """Validate email configuration (optional)."""
    print_header("Email Configuration (Optional)")
    
    resend_key = os.getenv("RESEND_API_KEY", "")
    owner_email = os.getenv("OWNER_EMAIL", "")
    
    has_resend = bool(resend_key)
    has_email = bool(owner_email)
    
    if not has_resend and not has_email:
        print_status("Email Notifications", True, "Disabled (optional feature)")
        return True
    
    print_status("Resend API Key", has_resend,
                 "Set" if has_resend else "Missing")
    
    if has_resend and resend_key.startswith("re_"):
        print_status("Key Format", True, "Valid Resend key format")
    elif has_resend:
        print_status("Key Format", False, "Should start with 're_'")
    
    print_status("Owner Email", has_email,
                 owner_email if has_email else "Missing")
    
    if has_email and "@" in owner_email:
        print_status("Email Format", True, "Valid email format")
    elif has_email:
        print_status("Email Format", False, "Invalid email format")
    
    if has_resend and has_email:
        print_status("Email Notifications", True, "Enabled")
    elif has_resend or has_email:
        print_status("Email Notifications", False, "Partially configured")
    
    return True  # Email is optional, so always return True


def validate_app_config():
    """Validate application configuration."""
    print_header("Application Configuration")
    
    log_level = os.getenv("LOG_LEVEL", "INFO")
    flask_env = os.getenv("FLASK_ENV", "production")
    port = os.getenv("PORT", "5000")
    
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    valid_log = log_level.upper() in valid_log_levels
    print_status("Log Level", valid_log,
                 f"{log_level}" if valid_log else f"Invalid: {log_level}")
    
    print_status("Flask Environment", True, flask_env)
    
    try:
        port_num = int(port)
        valid_port = 1 <= port_num <= 65535
        print_status("Port", valid_port,
                     f"{port}" if valid_port else f"Invalid: {port}")
    except ValueError:
        print_status("Port", False, f"Invalid: {port} (not a number)")
        valid_port = False
    
    return valid_log and valid_port


def main():
    """Main validation function."""
    print("\n" + "🔍 GitHub Manager Configuration Validator" + "\n")
    
    # Run all validations
    github_valid = validate_github_config()
    ai_valid = validate_ai_config()
    email_valid = validate_email_config()
    app_valid = validate_app_config()
    
    # Summary
    print_header("Validation Summary")
    
    all_valid = github_valid and ai_valid and email_valid and app_valid
    
    if all_valid:
        print("\n✅ All required configuration is valid!")
        print("   You're ready to deploy to Heroku.\n")
        return 0
    else:
        print("\n❌ Configuration validation failed!")
        print("   Please fix the issues above before deploying.\n")
        
        if not github_valid:
            print("   → Fix GitHub configuration")
        if not ai_valid:
            print("   → Fix AI configuration")
        if not email_valid:
            print("   → Fix email configuration (if you want email notifications)")
        if not app_valid:
            print("   → Fix application configuration")
        
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())

