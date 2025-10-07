#!/usr/bin/env python3
"""
Local testing script for GitHub Manager.
Tests basic functionality without deploying to Heroku.
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.config import Config
from src.logger import setup_logger
from src.github_client import GitHubClient
from src.ai_service import AIService
from src.email_service import EmailService

logger = setup_logger(__name__)


def test_configuration():
    """Test configuration validation."""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)
    
    is_valid, errors = Config.validate()
    
    if is_valid:
        print("✅ Configuration is valid")
        print(f"   Repository: {Config.GITHUB_REPO}")
        print(f"   AI Provider: {Config.AI_PROVIDER}")
        print(f"   Email Enabled: {Config.has_email_configured()}")
        return True
    else:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False


def test_github_connection():
    """Test GitHub API connection."""
    print("\n" + "="*60)
    print("Testing GitHub Connection")
    print("="*60)
    
    try:
        client = GitHubClient()
        repo_info = client.get_repository_info()
        
        if repo_info:
            print("✅ Successfully connected to GitHub")
            print(f"   Repository: {repo_info.get('full_name')}")
            print(f"   Owner: {repo_info.get('owner')}")
            print(f"   Default Branch: {repo_info.get('default_branch')}")
            print(f"   Open Issues: {repo_info.get('open_issues')}")
            print(f"   Stars: {repo_info.get('stars')}")
            return True
        else:
            print("❌ Failed to retrieve repository information")
            return False
    
    except Exception as e:
        print(f"❌ GitHub connection failed: {e}")
        return False


def test_ai_service():
    """Test AI service."""
    print("\n" + "="*60)
    print("Testing AI Service")
    print("="*60)
    
    try:
        ai_service = AIService()
        print(f"✅ AI service initialized with provider: {Config.AI_PROVIDER}")
        
        # Test simple response
        print("\n   Testing AI response generation...")
        test_prompt = "Say 'Hello, I am working!' in a friendly way."
        response = ai_service.generate_response(test_prompt)
        
        if response:
            print("✅ AI response generated successfully")
            print(f"   Response: {response[:100]}...")
            return True
        else:
            print("❌ Failed to generate AI response")
            return False
    
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False


def test_email_service():
    """Test email service."""
    print("\n" + "="*60)
    print("Testing Email Service")
    print("="*60)
    
    try:
        email_service = EmailService()
        
        if email_service.enabled:
            print("✅ Email service is enabled")
            print(f"   Owner Email: {Config.OWNER_EMAIL}")
            print("\n   Note: Not sending test email to avoid spam.")
            print("   Email functionality will be tested during actual use.")
            return True
        else:
            print("ℹ️  Email service is disabled (optional)")
            print("   This is normal if you haven't configured Resend.")
            return True
    
    except Exception as e:
        print(f"❌ Email service test failed: {e}")
        return False


def test_assignment_detection():
    """Test assignment request detection."""
    print("\n" + "="*60)
    print("Testing Assignment Detection")
    print("="*60)
    
    try:
        from src.issue_manager import IssueManager
        from src.github_client import GitHubClient
        from src.ai_service import AIService
        from src.email_service import EmailService
        
        github_client = GitHubClient()
        ai_service = AIService()
        email_service = EmailService()
        issue_manager = IssueManager(github_client, ai_service, email_service)
        
        test_cases = [
            ("assign me", True),
            ("I want to work on this", True),
            ("Can I work on this?", True),
            ("This is a great issue", False),
            ("Please assign me", True),
            ("Just a regular comment", False),
        ]
        
        all_passed = True
        for comment, expected in test_cases:
            result = issue_manager.is_assignment_request(comment)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{comment}' -> {result} (expected {expected})")
            if result != expected:
                all_passed = False
        
        if all_passed:
            print("\n✅ All assignment detection tests passed")
            return True
        else:
            print("\n❌ Some assignment detection tests failed")
            return False
    
    except Exception as e:
        print(f"❌ Assignment detection test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "🧪 GitHub Manager - Local Testing Suite" + "\n")
    
    results = {
        "Configuration": test_configuration(),
        "GitHub Connection": test_github_connection(),
        "AI Service": test_ai_service(),
        "Email Service": test_email_service(),
        "Assignment Detection": test_assignment_detection(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed! Ready to deploy to Heroku.")
        print("\nNext steps:")
        print("1. Deploy to Heroku: git push heroku main")
        print("2. Configure GitHub webhook")
        print("3. Test with real issues and PRs")
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        print("\nTroubleshooting:")
        print("1. Check your .env file")
        print("2. Verify all API keys are correct")
        print("3. Ensure GitHub token has correct permissions")
        print("4. Review error messages above")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

