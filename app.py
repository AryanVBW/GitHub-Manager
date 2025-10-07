"""
GitHub Manager - Main Flask Application
Continuously running backend for GitHub repository management.
Supports multi-repository management and personalized AI responses.
"""
from flask import Flask, request, jsonify
import sys
import os

from src.config import Config
from src.logger import setup_logger
from src.github_client import GitHubClient
from src.ai_service import AIService
from src.email_service import EmailService
from src.issue_manager import IssueManager
from src.pr_manager import PRManager
from src.webhook_handler import WebhookHandler

# Setup logger
logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global instances
github_client = None
ai_service = None
email_service = None
issue_manager = None
pr_manager = None
webhook_handler = None


def initialize_services():
    """Initialize all services and validate configuration."""
    global github_client, ai_service, email_service
    global issue_manager, pr_manager, webhook_handler
    
    try:
        # Validate configuration
        is_valid, errors = Config.validate()
        
        if not is_valid:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            sys.exit(1)
        
        logger.info("Configuration validated successfully")
        
        # Log email configuration status
        if Config.has_email_configured():
            logger.info("Email notifications enabled")
        else:
            logger.info("Email notifications disabled (optional)")
        
        # Initialize services
        logger.info("Initializing services...")
        
        github_client = GitHubClient()
        ai_service = AIService()
        email_service = EmailService()
        
        issue_manager = IssueManager(github_client, ai_service, email_service)
        pr_manager = PRManager(github_client, ai_service, email_service)
        webhook_handler = WebhookHandler(github_client, issue_manager, pr_manager)
        
        logger.info("All services initialized successfully")

        # Log user info
        user_info = github_client.get_user_info()
        logger.info(f"Authenticated as: {user_info.get('login')}")
        logger.info(f"Public repositories: {user_info.get('public_repos')}")

        # Log public repositories
        repos = github_client.get_all_public_repositories()
        logger.info(f"Managing {len(repos)} public repositories:")
        for repo in repos[:5]:  # Log first 5
            logger.info(f"  - {repo.full_name}")
        if len(repos) > 5:
            logger.info(f"  ... and {len(repos) - 5} more")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        sys.exit(1)


@app.route('/')
def index():
    """Health check endpoint."""
    user_info = github_client.get_user_info() if github_client else {}
    repos = github_client.get_all_public_repositories() if github_client else []

    return jsonify({
        'status': 'running',
        'service': 'GitHub Manager',
        'version': '2.0.0',
        'authenticated_user': user_info.get('login', 'unknown'),
        'managing_repositories': len(repos),
        'ai_provider': Config.AI_PROVIDER,
        'ai_model': Config.OPENAI_MODEL if Config.AI_PROVIDER == 'openai' else Config.GEMINI_MODEL,
        'email_enabled': Config.has_email_configured(),
        'features': {
            'multi_repo': True,
            'personalized_responses': True,
            'custom_system_prompt': bool(os.getenv('SYSTEM_PROMPT'))
        }
    })


@app.route('/health')
def health():
    """Detailed health check endpoint."""
    try:
        # Check GitHub connection
        user_info = github_client.get_user_info()
        repos = github_client.get_all_public_repositories()
        github_status = 'connected' if user_info else 'disconnected'

        return jsonify({
            'status': 'healthy',
            'github': github_status,
            'authenticated_user': user_info.get('login', 'unknown'),
            'managing_repositories': len(repos),
            'ai_provider': Config.AI_PROVIDER,
            'ai_model': Config.OPENAI_MODEL if Config.AI_PROVIDER == 'openai' else Config.GEMINI_MODEL,
            'email_enabled': Config.has_email_configured()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/webhook', methods=['POST'])
def webhook():
    """GitHub webhook endpoint."""
    try:
        # Verify signature
        if not webhook_handler.verify_signature(request):
            logger.warning("Webhook signature verification failed")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Get event type
        event_type = request.headers.get('X-GitHub-Event')
        
        if not event_type:
            logger.warning("No event type in webhook request")
            return jsonify({'error': 'No event type'}), 400
        
        # Get payload
        payload = request.json
        
        if not payload:
            logger.warning("No payload in webhook request")
            return jsonify({'error': 'No payload'}), 400
        
        # Handle event
        success = webhook_handler.handle_event(event_type, payload)
        
        if success:
            return jsonify({'status': 'processed'}), 200
        else:
            return jsonify({'status': 'ignored'}), 200
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        
        # Send error notification
        if email_service:
            email_service.notify_error(
                "Webhook Processing Error",
                f"Event: {request.headers.get('X-GitHub-Event')}\nError: {str(e)}"
            )
        
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize services on startup
    initialize_services()
    
    # Run Flask app
    port = Config.PORT
    logger.info(f"Starting GitHub Manager on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=(Config.FLASK_ENV == 'development')
    )

