"""
Issue management system with intelligent assignment and AI-powered responses.
"""
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import re

from github.Issue import Issue
from github.IssueComment import IssueComment

from src.github_client import GitHubClient
from src.ai_service import AIService
from src.email_service import EmailService
from src.logger import setup_logger

logger = setup_logger(__name__)


class IssueManager:
    """Manages issue monitoring, assignment, and responses."""
    
    # Keywords that indicate assignment request
    ASSIGNMENT_KEYWORDS = [
        r'\bassign\s+me\b',
        r'\bi\s+want\s+to\s+work\s+on\s+this\b',
        r'\bcan\s+i\s+work\s+on\s+this\b',
        r'\bi\s+would\s+like\s+to\s+work\s+on\s+this\b',
        r'\bi\'d\s+like\s+to\s+take\s+this\b',
        r'\bplease\s+assign\s+me\b',
        r'\bi\s+can\s+work\s+on\s+this\b',
        r'\blet\s+me\s+work\s+on\s+this\b',
    ]
    
    def __init__(
        self,
        github_client: GitHubClient,
        ai_service: AIService,
        email_service: EmailService
    ):
        """
        Initialize issue manager.
        
        Args:
            github_client: GitHub API client
            ai_service: AI service for generating responses
            email_service: Email notification service
        """
        self.github = github_client
        self.ai = ai_service
        self.email = email_service
    
    def is_assignment_request(self, comment_text: str) -> bool:
        """
        Check if a comment is requesting assignment.
        
        Args:
            comment_text: Comment text to analyze
        
        Returns:
            True if comment requests assignment
        """
        comment_lower = comment_text.lower()
        return any(re.search(pattern, comment_lower) for pattern in self.ASSIGNMENT_KEYWORDS)
    
    def analyze_assignment_candidates(
        self,
        issue: Issue,
        assignment_requests: List[Tuple[str, IssueComment]]
    ) -> Optional[str]:
        """
        Analyze candidates and select the best user to assign.
        
        Selection criteria:
        1. User who commented most frequently on the issue
        2. If tied, user who requested assignment first
        
        Args:
            issue: Issue object
            assignment_requests: List of (username, comment) tuples
        
        Returns:
            Username of selected candidate or None
        """
        if not assignment_requests:
            return None
        
        # Count comments for each candidate
        candidate_scores = {}
        
        for username, request_comment in assignment_requests:
            comment_count = self.github.get_user_comment_count(issue, username)
            request_time = request_comment.created_at
            
            candidate_scores[username] = {
                'comment_count': comment_count,
                'request_time': request_time,
                'request_comment': request_comment
            }
        
        # Sort by comment count (descending), then by request time (ascending)
        sorted_candidates = sorted(
            candidate_scores.items(),
            key=lambda x: (-x[1]['comment_count'], x[1]['request_time'])
        )
        
        selected_username = sorted_candidates[0][0]
        
        logger.info(
            f"Selected {selected_username} for issue #{issue.number} "
            f"(comments: {candidate_scores[selected_username]['comment_count']}, "
            f"requested: {candidate_scores[selected_username]['request_time']})"
        )
        
        return selected_username
    
    def generate_assignment_confirmation(
        self,
        username: str,
        issue: Issue
    ) -> str:
        """
        Generate a confirmation message for the assigned user.
        
        Args:
            username: Username of assigned user
            issue: Issue object
        
        Returns:
            Confirmation message
        """
        return (
            f"@{username} Thank you for your interest! "
            f"I've assigned this issue to you. "
            f"Feel free to ask any questions if you need clarification. "
            f"Looking forward to your contribution! 🚀"
        )
    
    def generate_decline_message(
        self,
        username: str,
        assigned_to: str,
        issue: Issue
    ) -> str:
        """
        Generate a polite decline message for non-selected users.
        
        Args:
            username: Username of user to decline
            assigned_to: Username of user who was assigned
            issue: Issue object
        
        Returns:
            Decline message
        """
        return (
            f"@{username} Thank you so much for your interest in working on this issue! "
            f"I really appreciate your willingness to contribute. "
            f"However, this issue has been assigned to @{assigned_to} based on their engagement. "
            f"Please feel free to check out other open issues where you can contribute. "
            f"Your participation in this project is valued! 🙏"
        )
    
    def handle_assignment_requests(
        self,
        issue: Issue,
        new_comment: IssueComment
    ) -> bool:
        """
        Handle assignment requests on an issue.
        
        Args:
            issue: Issue object
            new_comment: The new comment that triggered this
        
        Returns:
            True if assignment was handled
        """
        try:
            # Check if issue is already assigned
            if issue.assignees:
                logger.info(f"Issue #{issue.number} already assigned, skipping")
                return False
            
            # Get all comments
            comments = self.github.get_issue_comments(issue)
            
            # Find all assignment requests
            assignment_requests = []
            for comment in comments:
                if self.is_assignment_request(comment.body):
                    assignment_requests.append((comment.user.login, comment))
            
            if not assignment_requests:
                return False
            
            # Analyze and select best candidate
            selected_user = self.analyze_assignment_candidates(issue, assignment_requests)
            
            if not selected_user:
                return False
            
            # Assign the issue
            success = self.github.assign_issue(issue, selected_user)
            
            if not success:
                logger.error(f"Failed to assign issue #{issue.number}")
                return False
            
            # Send confirmation to selected user
            confirmation_msg = self.generate_assignment_confirmation(selected_user, issue)
            self.github.add_comment(issue, confirmation_msg)
            
            # Send decline messages to other users
            for username, _ in assignment_requests:
                if username != selected_user:
                    decline_msg = self.generate_decline_message(username, selected_user, issue)
                    self.github.add_comment(issue, decline_msg)
            
            # Send email notification
            self.email.notify_issue_assignment(
                issue.number,
                issue.title,
                selected_user,
                issue.html_url
            )
            
            logger.info(f"Successfully handled assignment for issue #{issue.number}")
            return True
        
        except Exception as e:
            logger.error(f"Error handling assignment requests for issue #{issue.number}: {e}")
            return False
    
    def generate_issue_context(self, issue: Issue) -> str:
        """
        Generate context about an issue for AI.
        
        Args:
            issue: Issue object
        
        Returns:
            Context string
        """
        context_parts = [
            f"Issue #{issue.number}: {issue.title}",
            f"State: {issue.state}",
        ]
        
        if issue.body:
            context_parts.append(f"Description: {issue.body[:500]}")
        
        if issue.labels:
            labels = ", ".join([label.name for label in issue.labels])
            context_parts.append(f"Labels: {labels}")
        
        return "\n".join(context_parts)
    
    def handle_comment(self, issue: Issue, comment: IssueComment) -> bool:
        """
        Handle a new comment on an issue.
        
        Args:
            issue: Issue object
            comment: Comment object
        
        Returns:
            True if handled successfully
        """
        try:
            # Skip bot's own comments
            if comment.user.login.endswith('[bot]'):
                logger.debug(f"Skipping bot comment on issue #{issue.number}")
                return False
            
            # Check for assignment request
            if self.is_assignment_request(comment.body):
                return self.handle_assignment_requests(issue, comment)
            
            # Generate AI response for other comments
            issue_context = self.generate_issue_context(issue)
            ai_response = self.ai.generate_issue_response(comment.body, issue_context)
            
            if ai_response:
                self.github.add_comment(issue, ai_response)
                logger.info(f"Added AI response to issue #{issue.number}")
                return True
            else:
                logger.warning(f"Failed to generate AI response for issue #{issue.number}")
                return False
        
        except Exception as e:
            logger.error(f"Error handling comment on issue #{issue.number}: {e}")
            return False

