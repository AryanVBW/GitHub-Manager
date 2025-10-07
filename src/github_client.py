"""
GitHub API client with rate limiting and error handling.
Supports multi-repository management.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import time
from github import Github, GithubException, RateLimitExceededException
from github.Repository import Repository
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.IssueComment import IssueComment
from github.AuthenticatedUser import AuthenticatedUser

from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class GitHubClient:
    """GitHub API client with enhanced error handling and rate limiting.
    Supports multi-repository management."""

    def __init__(self):
        """Initialize GitHub client."""
        self.client = Github(Config.GITHUB_TOKEN, per_page=100)
        self.user: Optional[AuthenticatedUser] = None
        self._rate_limit_reset_time: Optional[datetime] = None
        self._repositories_cache: Dict[str, Repository] = {}
        self._initialize_user()

    def _initialize_user(self):
        """Initialize authenticated user."""
        try:
            self.user = self.client.get_user()
            logger.info(f"Successfully authenticated as: {self.user.login}")
        except GithubException as e:
            logger.error(f"Failed to authenticate user: {e}")
            raise
    
    def get_repository(self, repo_full_name: str) -> Optional[Repository]:
        """
        Get a repository by full name (owner/repo).
        Uses caching to avoid repeated API calls.

        Args:
            repo_full_name: Repository full name (e.g., "owner/repo")

        Returns:
            Repository object or None if not found
        """
        if repo_full_name in self._repositories_cache:
            return self._repositories_cache[repo_full_name]

        try:
            self._check_rate_limit()
            repo = self.client.get_repo(repo_full_name)
            self._repositories_cache[repo_full_name] = repo
            logger.debug(f"Retrieved and cached repository: {repo_full_name}")
            return repo
        except GithubException as e:
            logger.error(f"Error retrieving repository {repo_full_name}: {e}")
            return None

    def get_all_public_repositories(self) -> List[Repository]:
        """
        Get all public repositories owned by the authenticated user.

        Returns:
            List of Repository objects
        """
        try:
            self._check_rate_limit()
            repos = [repo for repo in self.user.get_repos() if not repo.private]
            logger.info(f"Found {len(repos)} public repositories")

            # Cache all repositories
            for repo in repos:
                self._repositories_cache[repo.full_name] = repo

            return repos
        except GithubException as e:
            logger.error(f"Error retrieving public repositories: {e}")
            return []

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
    
    def get_issue(self, repo: Repository, issue_number: int) -> Optional[Issue]:
        """
        Get an issue by number from a specific repository.

        Args:
            repo: Repository object
            issue_number: Issue number

        Returns:
            Issue object or None if not found
        """
        try:
            self._check_rate_limit()
            issue = repo.get_issue(issue_number)
            logger.debug(f"Retrieved issue #{issue_number} from {repo.full_name}")
            return issue
        except GithubException as e:
            logger.error(f"Error retrieving issue #{issue_number} from {repo.full_name}: {e}")
            return None

    def get_pull_request(self, repo: Repository, pr_number: int) -> Optional[PullRequest]:
        """
        Get a pull request by number from a specific repository.

        Args:
            repo: Repository object
            pr_number: Pull request number

        Returns:
            PullRequest object or None if not found
        """
        try:
            self._check_rate_limit()
            pr = repo.get_pull(pr_number)
            logger.debug(f"Retrieved PR #{pr_number} from {repo.full_name}")
            return pr
        except GithubException as e:
            logger.error(f"Error retrieving PR #{pr_number} from {repo.full_name}: {e}")
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

    def get_user_comment_history(
        self,
        repo: Repository,
        username: str,
        limit: int = 10
    ) -> List[str]:
        """
        Get a user's recent comment history from a repository.
        Used for writing style analysis.

        Args:
            repo: Repository object
            username: GitHub username
            limit: Maximum number of comments to retrieve

        Returns:
            List of comment texts
        """
        try:
            self._check_rate_limit()
            comments = []

            # Get recent issues
            issues = repo.get_issues(state='all', sort='updated', direction='desc')

            for issue in issues[:20]:  # Check last 20 issues
                if len(comments) >= limit:
                    break

                issue_comments = self.get_issue_comments(issue)
                for comment in issue_comments:
                    if comment.user.login == username:
                        comments.append(comment.body)
                        if len(comments) >= limit:
                            break

            logger.debug(f"Retrieved {len(comments)} comments from {username} in {repo.full_name}")
            return comments

        except Exception as e:
            logger.error(f"Error retrieving comment history for {username}: {e}")
            return []
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get authenticated user information.

        Returns:
            Dictionary with user details
        """
        try:
            self._check_rate_limit()
            return {
                "login": self.user.login,
                "name": self.user.name,
                "email": self.user.email,
                "public_repos": self.user.public_repos,
                "followers": self.user.followers,
            }
        except GithubException as e:
            logger.error(f"Error retrieving user info: {e}")
            return {}

    def get_repository_info(self, repo: Repository) -> Dict[str, Any]:
        """
        Get repository information.

        Args:
            repo: Repository object

        Returns:
            Dictionary with repository details
        """
        try:
            self._check_rate_limit()
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "description": repo.description,
                "default_branch": repo.default_branch,
                "open_issues": repo.open_issues_count,
                "stars": repo.stargazers_count,
            }
        except GithubException as e:
            logger.error(f"Error retrieving repository info: {e}")
            return {}

