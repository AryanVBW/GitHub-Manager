"""
Pull request management system with AI-powered responses.
"""
from typing import Optional
from github.PullRequest import PullRequest
from github.IssueComment import IssueComment

from src.github_client import GitHubClient
from src.ai_service import AIService
from src.email_service import EmailService
from src.logger import setup_logger

logger = setup_logger(__name__)


class PRManager:
    """Manages pull request monitoring and responses."""
    
    def __init__(
        self,
        github_client: GitHubClient,
        ai_service: AIService,
        email_service: EmailService
    ):
        """
        Initialize PR manager.
        
        Args:
            github_client: GitHub API client
            ai_service: AI service for generating responses
            email_service: Email notification service
        """
        self.github = github_client
        self.ai = ai_service
        self.email = email_service
    
    def generate_pr_context(self, pr: PullRequest) -> str:
        """
        Generate context about a pull request for AI.
        
        Args:
            pr: PullRequest object
        
        Returns:
            Context string
        """
        context_parts = [
            f"Pull Request #{pr.number}: {pr.title}",
            f"State: {pr.state}",
            f"Base branch: {pr.base.ref}",
            f"Head branch: {pr.head.ref}",
        ]
        
        if pr.body:
            context_parts.append(f"Description: {pr.body[:500]}")
        
        if pr.labels:
            labels = ", ".join([label.name for label in pr.labels])
            context_parts.append(f"Labels: {labels}")
        
        # Add PR stats
        context_parts.append(f"Files changed: {pr.changed_files}")
        context_parts.append(f"Additions: +{pr.additions}, Deletions: -{pr.deletions}")
        
        # Add review status
        if pr.mergeable_state:
            context_parts.append(f"Mergeable state: {pr.mergeable_state}")
        
        return "\n".join(context_parts)
    
    def is_question(self, comment_text: str) -> bool:
        """
        Check if a comment contains a question.
        
        Args:
            comment_text: Comment text to analyze
        
        Returns:
            True if comment appears to be a question
        """
        # Simple heuristic: contains question mark or starts with question words
        question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should']
        
        if '?' in comment_text:
            return True
        
        first_word = comment_text.strip().split()[0].lower() if comment_text.strip() else ''
        return first_word in question_words
    
    def handle_comment(self, pr: PullRequest, comment: IssueComment) -> bool:
        """
        Handle a new comment on a pull request.
        
        Args:
            pr: PullRequest object
            comment: Comment object
        
        Returns:
            True if handled successfully
        """
        try:
            # Skip bot's own comments
            if comment.user.login.endswith('[bot]'):
                logger.debug(f"Skipping bot comment on PR #{pr.number}")
                return False
            
            # Generate context
            pr_context = self.generate_pr_context(pr)
            
            # Generate AI response
            ai_response = self.ai.generate_pr_response(comment.body, pr_context)
            
            if ai_response:
                # Add response as comment
                success = self.github.add_comment(pr, ai_response)
                
                if success:
                    logger.info(f"Added AI response to PR #{pr.number}")
                    
                    # Send email notification if it's a question
                    if self.is_question(comment.body):
                        self.email.notify_pr_activity(
                            pr.number,
                            pr.title,
                            "Question Asked",
                            f"User @{comment.user.login} asked: {comment.body[:200]}...",
                            pr.html_url
                        )
                    
                    return True
                else:
                    logger.warning(f"Failed to add comment to PR #{pr.number}")
                    return False
            else:
                logger.warning(f"Failed to generate AI response for PR #{pr.number}")
                return False
        
        except Exception as e:
            logger.error(f"Error handling comment on PR #{pr.number}: {e}")
            return False
    
    def handle_pr_opened(self, pr: PullRequest) -> bool:
        """
        Handle a newly opened pull request.
        
        Args:
            pr: PullRequest object
        
        Returns:
            True if handled successfully
        """
        try:
            logger.info(f"New PR opened: #{pr.number} - {pr.title}")
            
            # Send email notification
            self.email.notify_pr_activity(
                pr.number,
                pr.title,
                "New Pull Request",
                f"Opened by @{pr.user.login} from {pr.head.ref} to {pr.base.ref}",
                pr.html_url
            )
            
            # Optionally add a welcome comment
            welcome_message = (
                f"Thank you @{pr.user.login} for your pull request! 🎉\n\n"
                f"I'll help answer any questions you might have. "
                f"A maintainer will review your changes soon."
            )
            
            return self.github.add_comment(pr, welcome_message)
        
        except Exception as e:
            logger.error(f"Error handling new PR #{pr.number}: {e}")
            return False
    
    def handle_pr_review_requested(self, pr: PullRequest, reviewer: str) -> bool:
        """
        Handle review request on a pull request.
        
        Args:
            pr: PullRequest object
            reviewer: Username of requested reviewer
        
        Returns:
            True if handled successfully
        """
        try:
            logger.info(f"Review requested on PR #{pr.number} from @{reviewer}")
            
            # Send email notification
            self.email.notify_pr_activity(
                pr.number,
                pr.title,
                "Review Requested",
                f"Review requested from @{reviewer}",
                pr.html_url
            )
            
            return True
        
        except Exception as e:
            logger.error(f"Error handling review request on PR #{pr.number}: {e}")
            return False
    
    def handle_pr_merged(self, pr: PullRequest) -> bool:
        """
        Handle a merged pull request.
        
        Args:
            pr: PullRequest object
        
        Returns:
            True if handled successfully
        """
        try:
            logger.info(f"PR merged: #{pr.number} - {pr.title}")
            
            # Send email notification
            self.email.notify_pr_activity(
                pr.number,
                pr.title,
                "Pull Request Merged",
                f"Merged by @{pr.merged_by.login if pr.merged_by else 'unknown'}",
                pr.html_url
            )
            
            # Add congratulations comment
            congrats_message = (
                f"🎉 Congratulations @{pr.user.login}! "
                f"Your pull request has been merged. "
                f"Thank you for your contribution!"
            )
            
            return self.github.add_comment(pr, congrats_message)
        
        except Exception as e:
            logger.error(f"Error handling merged PR #{pr.number}: {e}")
            return False

