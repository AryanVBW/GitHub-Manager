#!/usr/bin/env python3
"""
Bulk Webhook Setup Script
Automatically adds webhooks to all your public repositories.

Usage:
    python scripts/setup_webhooks.py

Environment Variables Required:
    GITHUB_TOKEN - Your GitHub Personal Access Token
    GITHUB_WEBHOOK_SECRET - Webhook secret for signature verification
    WEBHOOK_URL - Your Heroku app webhook URL
"""

import os
import sys
from github import Github
from github.GithubException import GithubException


def setup_webhooks():
    """Add webhooks to all public repositories."""
    
    # Get configuration from environment
    github_token = os.getenv('GITHUB_TOKEN')
    webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')
    webhook_url = os.getenv('WEBHOOK_URL', 'https://github-manager-d89575ed2bc3.herokuapp.com/webhook')
    
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    if not webhook_secret:
        print("❌ Error: GITHUB_WEBHOOK_SECRET environment variable not set")
        print("   Set it with: export GITHUB_WEBHOOK_SECRET='your_secret_here'")
        sys.exit(1)
    
    print("🚀 GitHub Webhook Bulk Setup")
    print("=" * 60)
    print(f"📍 Webhook URL: {webhook_url}")
    print(f"🔐 Secret: {'*' * len(webhook_secret)}")
    print()
    
    # Initialize GitHub client
    try:
        g = Github(github_token)
        user = g.get_user()
        print(f"✅ Authenticated as: {user.login}")
        print()
    except GithubException as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)
    
    # Webhook configuration
    webhook_config = {
        "url": webhook_url,
        "content_type": "json",
        "secret": webhook_secret,
        "insecure_ssl": "0"  # Require SSL
    }
    
    # Events to subscribe to
    events = [
        "issues",
        "issue_comment",
        "pull_request",
        "pull_request_review",
        "pull_request_review_comment"
    ]
    
    # Get all public repositories
    print("📦 Fetching your public repositories...")
    try:
        repos = list(user.get_repos(type='public'))
        print(f"   Found {len(repos)} public repositories")
        print()
    except GithubException as e:
        print(f"❌ Failed to fetch repositories: {e}")
        sys.exit(1)
    
    # Confirm before proceeding
    print(f"⚠️  This will add webhooks to {len(repos)} repositories.")
    response = input("   Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Aborted by user")
        sys.exit(0)
    
    print()
    print("🔧 Adding webhooks...")
    print("-" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, repo in enumerate(repos, 1):
        repo_name = repo.full_name
        print(f"[{i}/{len(repos)}] {repo_name}...", end=" ")
        
        try:
            # Check if webhook already exists
            existing_webhooks = repo.get_hooks()
            webhook_exists = False
            
            for hook in existing_webhooks:
                if hook.config.get('url') == webhook_url:
                    webhook_exists = True
                    print("⏭️  Already exists")
                    skip_count += 1
                    break
            
            if not webhook_exists:
                # Create webhook
                repo.create_hook(
                    name="web",
                    config=webhook_config,
                    events=events,
                    active=True
                )
                print("✅ Added")
                success_count += 1
                
        except GithubException as e:
            if e.status == 403:
                print(f"❌ Permission denied (need admin access)")
            elif e.status == 404:
                print(f"❌ Repository not found")
            else:
                print(f"❌ Error: {e.data.get('message', str(e))}")
            error_count += 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            error_count += 1
    
    # Summary
    print()
    print("=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully added: {success_count}")
    print(f"   ⏭️  Already existed: {skip_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📦 Total repositories: {len(repos)}")
    print()
    
    if success_count > 0:
        print("🎉 Webhook setup complete!")
        print()
        print("Next steps:")
        print("1. Test the webhooks by creating an issue in any repository")
        print("2. Check Heroku logs: heroku logs --tail -a github-manager")
        print("3. Verify webhook deliveries in GitHub repository settings")
    
    if error_count > 0:
        print()
        print("⚠️  Some webhooks failed to install.")
        print("   Common reasons:")
        print("   - You don't have admin access to the repository")
        print("   - The repository is archived")
        print("   - Rate limit exceeded (wait a few minutes)")


def list_webhooks():
    """List all existing webhooks across repositories."""
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    print("📋 Listing Existing Webhooks")
    print("=" * 60)
    
    g = Github(github_token)
    user = g.get_user()
    repos = list(user.get_repos(type='public'))
    
    webhook_count = 0
    
    for repo in repos:
        try:
            hooks = list(repo.get_hooks())
            if hooks:
                print(f"\n📦 {repo.full_name}")
                for hook in hooks:
                    webhook_count += 1
                    url = hook.config.get('url', 'N/A')
                    active = "✅" if hook.active else "❌"
                    print(f"   {active} {url}")
                    print(f"      Events: {', '.join(hook.events)}")
        except GithubException:
            pass  # Skip repos without access
    
    print()
    print("=" * 60)
    print(f"Total webhooks found: {webhook_count}")


def remove_webhooks():
    """Remove webhooks from all repositories."""
    
    github_token = os.getenv('GITHUB_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL', 'https://github-manager-d89575ed2bc3.herokuapp.com/webhook')
    
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    print("🗑️  Webhook Removal Tool")
    print("=" * 60)
    print(f"📍 Will remove webhooks matching: {webhook_url}")
    print()
    
    g = Github(github_token)
    user = g.get_user()
    repos = list(user.get_repos(type='public'))
    
    print(f"⚠️  This will remove webhooks from {len(repos)} repositories.")
    response = input("   Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("❌ Aborted by user")
        sys.exit(0)
    
    print()
    removed_count = 0
    
    for repo in repos:
        try:
            hooks = repo.get_hooks()
            for hook in hooks:
                if hook.config.get('url') == webhook_url:
                    hook.delete()
                    print(f"✅ Removed from {repo.full_name}")
                    removed_count += 1
        except GithubException:
            pass
    
    print()
    print(f"🎉 Removed {removed_count} webhooks")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GitHub Webhook Management Tool")
    parser.add_argument(
        'action',
        choices=['setup', 'list', 'remove'],
        help='Action to perform: setup (add webhooks), list (show existing), remove (delete webhooks)'
    )
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        setup_webhooks()
    elif args.action == 'list':
        list_webhooks()
    elif args.action == 'remove':
        remove_webhooks()

