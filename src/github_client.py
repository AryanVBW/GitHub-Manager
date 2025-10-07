"""
GitHub API client with rate limiting and error handling.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import time
from github import Github, GithubException, RateLimitExceededException
from github.Repository import Repository
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.IssueComment import IssueComment

from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class GitHubClient:
    """GitHub API client with enhanced error handling and rate limiting."""
    
    def __init__(self):
        """Initialize GitHub client."""
        self.client = Github(Config.GITHUB_TOKEN, per_page=100)
        self.repo: Optional[Repository] = None
        self._rate_limit_reset_time: Optional[datetime] = None
        self._initialize_repository()
    
    def _initialize_repository(self):
        """Initialize repository connection."""
        try:
            owner, repo_name = Config.get_repo_owner_and_name()
            self.repo = self.client.get_repo(f"{owner}/{repo_name}")
            logger.info(f"Successfully connected to repository: {Config.GITHUB_REPO}")
        except GithubException as e:
            logger.error(f"Failed to connect to repository: {e}")
            raise
    
    def _check_rate_limit(self):
        """Check and handle rate limiting."""
        try:
            rate_limit = self.client.get_rate_limit()
            core_limit = rate_limit.core
            
            if core_limit.remaining < 10:
                reset_time = core_limit.reset
                wait_seconds = (reset_time - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    logger.warning(
                        f"Rate limit nearly exceeded. "
                        f"Remaining: {core_limit.remaining}. "
                        f"Waiting {wait_seconds:.0f} seconds until reset."
                    )
                    time.sleep(wait_seconds + 1)
            
            logger.debug(f"Rate limit remaining: {core_limit.remaining}/{core_limit.limit}")
        
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
    
    def get_issue(self, issue_number: int) -> Optional[Issue]:
        """
        Get an issue by number.
        
        Args:
            issue_number: Issue number
        
        Returns:
            Issue object or None if not found
        """
        try:
            self._check_rate_limit()
            issue = self.repo.get_issue(issue_number)
            logger.debug(f"Retrieved issue #{issue_number}")
            return issue
        except GithubException as e:
            logger.error(f"Error retrieving issue #{issue_number}: {e}")
            return None
    
    def get_pull_request(self, pr_number: int) -> Optional[PullRequest]:
        """
        Get a pull request by number.
        
        Args:
            pr_number: Pull request number
        
        Returns:
            PullRequest object or None if not found
        """
        try:
            self._check_rate_limit()
            pr = self.repo.get_pull(pr_number)
            logger.debug(f"Retrieved PR #{pr_number}")
            return pr
        except GithubException as e:
            logger.error(f"Error retrieving PR #{pr_number}: {e}")
            return None
    
    def get_issue_comments(self, issue: Issue) -> List[IssueComment]:
        """
        Get all comments for an issue.
        
        Args:
            issue: Issue object
        
        Returns:
            List of comment objects
        """
        try:
            self._check_rate_limit()
            comments = list(issue.get_comments())
            logger.debug(f"Retrieved {len(comments)} comments for issue #{issue.number}")
            return comments
        except GithubException as e:
            logger.error(f"Error retrieving comments for issue #{issue.number}: {e}")
            return []
    
    def add_comment(self, issue: Issue, comment: str) -> bool:
        """
        Add a comment to an issue or pull request.
        
        Args:
            issue: Issue or PullRequest object
            comment: Comment text
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._check_rate_limit()
            issue.create_comment(comment)
            logger.info(f"Added comment to issue #{issue.number}")
            return True
        except GithubException as e:
            logger.error(f"Error adding comment to issue #{issue.number}: {e}")
            return False
    
    def assign_issue(self, issue: Issue, assignee: str) -> bool:
        """
        Assign an issue to a user.
        
        Args:
            issue: Issue object
            assignee: GitHub username
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._check_rate_limit()
            issue.add_to_assignees(assignee)
            logger.info(f"Assigned issue #{issue.number} to {assignee}")
            return True
        except GithubException as e:
            logger.error(f"Error assigning issue #{issue.number} to {assignee}: {e}")
            return False
    
    def get_user_comment_count(self, issue: Issue, username: str) -> int:
        """
        Count how many times a user has commented on an issue.
        
        Args:
            issue: Issue object
            username: GitHub username
        
        Returns:
            Number of comments by the user
        """
        try:
            comments = self.get_issue_comments(issue)
            count = sum(1 for comment in comments if comment.user.login == username)
            logger.debug(f"User {username} has {count} comments on issue #{issue.number}")
            return count
        except Exception as e:
            logger.error(f"Error counting comments for {username} on issue #{issue.number}: {e}")
            return 0
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get repository information.
        
        Returns:
            Dictionary with repository details
        """
        try:
            self._check_rate_limit()
            return {
                "name": self.repo.name,
                "full_name": self.repo.full_name,
                "owner": self.repo.owner.login,
                "description": self.repo.description,
                "default_branch": self.repo.default_branch,
                "open_issues": self.repo.open_issues_count,
                "stars": self.repo.stargazers_count,
            }
        except GithubException as e:
            logger.error(f"Error retrieving repository info: {e}")
            return {}

