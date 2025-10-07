"""
GitHub webhook handler for processing repository events.
"""
import hmac
import hashlib
from typing import Dict, Any, Optional
from flask import Request

from src.config import Config
from src.github_client import GitHubClient
from src.issue_manager import IssueManager
from src.pr_manager import PRManager
from src.logger import setup_logger

logger = setup_logger(__name__)


class WebhookHandler:
    """Handles GitHub webhook events."""
    
    def __init__(
        self,
        github_client: GitHubClient,
        issue_manager: IssueManager,
        pr_manager: PRManager
    ):
        """
        Initialize webhook handler.
        
        Args:
            github_client: GitHub API client
            issue_manager: Issue manager instance
            pr_manager: PR manager instance
        """
        self.github = github_client
        self.issue_manager = issue_manager
        self.pr_manager = pr_manager
    
    def verify_signature(self, request: Request) -> bool:
        """
        Verify GitHub webhook signature.
        
        Args:
            request: Flask request object
        
        Returns:
            True if signature is valid
        """
        signature = request.headers.get('X-Hub-Signature-256')
        
        if not signature:
            logger.warning("No signature found in webhook request")
            return False
        
        # Compute expected signature
        secret = Config.GITHUB_WEBHOOK_SECRET.encode()
        body = request.get_data()
        expected_signature = 'sha256=' + hmac.new(
            secret,
            body,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        is_valid = hmac.compare_digest(signature, expected_signature)
        
        if not is_valid:
            logger.warning("Invalid webhook signature")
        
        return is_valid
    
    def handle_issue_comment(self, payload: Dict[str, Any]) -> bool:
        """
        Handle issue_comment event from any repository.

        Args:
            payload: Webhook payload

        Returns:
            True if handled successfully
        """
        try:
            action = payload.get('action')

            # Only handle created comments
            if action != 'created':
                logger.debug(f"Ignoring issue_comment action: {action}")
                return False

            # Get repository information
            repo_data = payload.get('repository', {})
            repo_full_name = repo_data.get('full_name')

            if not repo_full_name:
                logger.error("No repository information in payload")
                return False

            # Get the repository
            repo = self.github.get_repository(repo_full_name)
            if not repo:
                logger.error(f"Could not retrieve repository: {repo_full_name}")
                return False

            issue_data = payload.get('issue', {})
            comment_data = payload.get('comment', {})

            issue_number = issue_data.get('number')

            if not issue_number:
                logger.error("No issue number in payload")
                return False

            # Check if this is a PR (issues and PRs share the same endpoint)
            is_pull_request = 'pull_request' in issue_data

            if is_pull_request:
                # Handle as PR comment
                pr = self.github.get_pull_request(repo, issue_number)
                if pr:
                    # Create a mock comment object
                    from types import SimpleNamespace
                    comment = SimpleNamespace(
                        body=comment_data.get('body', ''),
                        user=SimpleNamespace(login=comment_data.get('user', {}).get('login', '')),
                        created_at=comment_data.get('created_at')
                    )
                    return self.pr_manager.handle_comment(pr, comment)
            else:
                # Handle as issue comment
                issue = self.github.get_issue(repo, issue_number)
                if issue:
                    # Get the actual comment object
                    comments = self.github.get_issue_comments(issue)
                    # Find the new comment (last one)
                    if comments:
                        new_comment = comments[-1]
                        return self.issue_manager.handle_comment(issue, new_comment)

            return False

        except Exception as e:
            logger.error(f"Error handling issue_comment event: {e}")
            return False
    
    def handle_pull_request(self, payload: Dict[str, Any]) -> bool:
        """
        Handle pull_request event from any repository.

        Args:
            payload: Webhook payload

        Returns:
            True if handled successfully
        """
        try:
            action = payload.get('action')

            # Get repository information
            repo_data = payload.get('repository', {})
            repo_full_name = repo_data.get('full_name')

            if not repo_full_name:
                logger.error("No repository information in payload")
                return False

            # Get the repository
            repo = self.github.get_repository(repo_full_name)
            if not repo:
                logger.error(f"Could not retrieve repository: {repo_full_name}")
                return False

            pr_data = payload.get('pull_request', {})
            pr_number = pr_data.get('number')

            if not pr_number:
                logger.error("No PR number in payload")
                return False

            pr = self.github.get_pull_request(repo, pr_number)

            if not pr:
                logger.error(f"Could not retrieve PR #{pr_number} from {repo_full_name}")
                return False

            # Handle different PR actions
            if action == 'opened':
                return self.pr_manager.handle_pr_opened(pr)

            elif action == 'review_requested':
                reviewer = payload.get('requested_reviewer', {}).get('login')
                if reviewer:
                    return self.pr_manager.handle_pr_review_requested(pr, reviewer)

            elif action == 'closed' and pr.merged:
                return self.pr_manager.handle_pr_merged(pr)

            else:
                logger.debug(f"Ignoring pull_request action: {action}")
                return False

        except Exception as e:
            logger.error(f"Error handling pull_request event: {e}")
            return False
    
    def handle_issues(self, payload: Dict[str, Any]) -> bool:
        """
        Handle issues event.
        
        Args:
            payload: Webhook payload
        
        Returns:
            True if handled successfully
        """
        try:
            action = payload.get('action')
            issue_data = payload.get('issue', {})
            issue_number = issue_data.get('number')
            
            if not issue_number:
                logger.error("No issue number in payload")
                return False
            
            # Log issue events but don't take action
            # (we mainly respond to comments)
            logger.info(f"Issue #{issue_number} {action}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error handling issues event: {e}")
            return False
    
    def handle_event(self, event_type: str, payload: Dict[str, Any]) -> bool:
        """
        Route webhook event to appropriate handler.
        
        Args:
            event_type: GitHub event type
            payload: Webhook payload
        
        Returns:
            True if handled successfully
        """
        logger.info(f"Received webhook event: {event_type}")
        
        handlers = {
            'issue_comment': self.handle_issue_comment,
            'pull_request': self.handle_pull_request,
            'issues': self.handle_issues,
        }
        
        handler = handlers.get(event_type)
        
        if handler:
            return handler(payload)
        else:
            logger.debug(f"No handler for event type: {event_type}")
            return False

