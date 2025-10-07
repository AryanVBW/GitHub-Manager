"""
Email notification service using Resend API.
Fully optional - application works without email configuration.
"""
from typing import Optional, Dict, Any
from datetime import datetime

from src.config import Config
from src.logger import setup_logger

logger = setup_logger(__name__)


class EmailService:
    """Email notification service with optional configuration."""
    
    def __init__(self):
        """Initialize email service."""
        self.enabled = Config.has_email_configured()
        self.client = None
        
        if self.enabled:
            try:
                import resend
                resend.api_key = Config.RESEND_API_KEY
                self.client = resend
                logger.info("Email service initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize email service: {e}. Email notifications disabled.")
                self.enabled = False
        else:
            logger.info("Email service not configured. Email notifications disabled.")
    
    def send_notification(
        self,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email notification to the repository owner.
        
        Args:
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.debug("Email service not enabled, skipping notification")
            return False
        
        try:
            params = {
                "from": "GitHub Manager <noreply@updates.github-manager.app>",
                "to": [Config.OWNER_EMAIL],
                "subject": subject,
                "html": html_content,
            }
            
            if text_content:
                params["text"] = text_content
            
            response = self.client.Emails.send(params)
            logger.info(f"Email notification sent successfully: {subject}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def notify_issue_assignment(
        self,
        issue_number: int,
        issue_title: str,
        assignee: str,
        issue_url: str
    ) -> bool:
        """
        Notify owner about issue assignment.
        
        Args:
            issue_number: Issue number
            issue_title: Issue title
            assignee: Username of assigned user
            issue_url: URL to the issue
        
        Returns:
            True if sent successfully
        """
        subject = f"Issue #{issue_number} assigned to {assignee}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #0366d6;">Issue Assignment Notification</h2>
            <p>An issue has been automatically assigned in your repository.</p>
            
            <div style="background-color: #f6f8fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Issue:</strong> #{issue_number} - {issue_title}</p>
                <p><strong>Assigned to:</strong> @{assignee}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
            
            <p>
                <a href="{issue_url}" style="background-color: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Issue
                </a>
            </p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e1e4e8;">
            <p style="color: #586069; font-size: 12px;">
                This is an automated notification from GitHub Manager.
            </p>
        </body>
        </html>
        """
        
        text_content = f"""
        Issue Assignment Notification
        
        Issue: #{issue_number} - {issue_title}
        Assigned to: @{assignee}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        
        View issue: {issue_url}
        
        ---
        This is an automated notification from GitHub Manager.
        """
        
        return self.send_notification(subject, html_content, text_content)
    
    def notify_pr_activity(
        self,
        pr_number: int,
        pr_title: str,
        activity_type: str,
        details: str,
        pr_url: str
    ) -> bool:
        """
        Notify owner about pull request activity.
        
        Args:
            pr_number: PR number
            pr_title: PR title
            activity_type: Type of activity (e.g., "New Comment", "Question")
            details: Activity details
            pr_url: URL to the PR
        
        Returns:
            True if sent successfully
        """
        subject = f"PR #{pr_number}: {activity_type}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #0366d6;">Pull Request Activity</h2>
            <p>New activity detected on a pull request in your repository.</p>
            
            <div style="background-color: #f6f8fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Pull Request:</strong> #{pr_number} - {pr_title}</p>
                <p><strong>Activity:</strong> {activity_type}</p>
                <p><strong>Details:</strong> {details}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
            
            <p>
                <a href="{pr_url}" style="background-color: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Pull Request
                </a>
            </p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e1e4e8;">
            <p style="color: #586069; font-size: 12px;">
                This is an automated notification from GitHub Manager.
            </p>
        </body>
        </html>
        """
        
        text_content = f"""
        Pull Request Activity
        
        Pull Request: #{pr_number} - {pr_title}
        Activity: {activity_type}
        Details: {details}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        
        View pull request: {pr_url}
        
        ---
        This is an automated notification from GitHub Manager.
        """
        
        return self.send_notification(subject, html_content, text_content)
    
    def notify_error(self, error_type: str, error_details: str) -> bool:
        """
        Notify owner about application errors.
        
        Args:
            error_type: Type of error
            error_details: Error details
        
        Returns:
            True if sent successfully
        """
        subject = f"GitHub Manager Error: {error_type}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #d73a49;">Error Notification</h2>
            <p>An error occurred in GitHub Manager.</p>
            
            <div style="background-color: #ffeef0; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #d73a49;">
                <p><strong>Error Type:</strong> {error_type}</p>
                <p><strong>Details:</strong></p>
                <pre style="background-color: #f6f8fa; padding: 10px; border-radius: 3px; overflow-x: auto;">{error_details}</pre>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </div>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #e1e4e8;">
            <p style="color: #586069; font-size: 12px;">
                This is an automated notification from GitHub Manager.
            </p>
        </body>
        </html>
        """
        
        text_content = f"""
        Error Notification
        
        Error Type: {error_type}
        Details: {error_details}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        
        ---
        This is an automated notification from GitHub Manager.
        """
        
        return self.send_notification(subject, html_content, text_content)

