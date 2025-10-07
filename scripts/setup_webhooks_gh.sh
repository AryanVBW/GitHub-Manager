#!/bin/bash
#
# GitHub Webhook Bulk Setup Script (using GitHub CLI)
# 
# This script uses the GitHub CLI (gh) to add webhooks to all your public repositories.
# It's an alternative to the Python script for users who prefer bash/gh.
#
# Prerequisites:
#   - GitHub CLI installed: brew install gh (macOS) or https://cli.github.com/
#   - Authenticated: gh auth login
#   - jq installed: brew install jq (for JSON parsing)
#
# Usage:
#   chmod +x scripts/setup_webhooks_gh.sh
#   ./scripts/setup_webhooks_gh.sh
#

set -e  # Exit on error

# Configuration
WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"
WEBHOOK_SECRET="YOUR_WEBHOOK_SECRET_HERE"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it with: brew install gh"
    echo "Or visit: https://cli.github.com/"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}❌ Error: jq is not installed${NC}"
    echo "Install it with: brew install jq"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${BLUE}🚀 GitHub Webhook Bulk Setup (using gh CLI)${NC}"
echo "============================================================"
echo -e "${BLUE}📍 Webhook URL:${NC} $WEBHOOK_URL"
echo -e "${BLUE}🔐 Secret:${NC} $(echo $WEBHOOK_SECRET | sed 's/./*/g')"
echo ""

# Get authenticated user
USERNAME=$(gh api user -q .login)
echo -e "${GREEN}✅ Authenticated as:${NC} $USERNAME"
echo ""

# Get all public repositories
echo -e "${BLUE}📦 Fetching your public repositories...${NC}"
REPOS=$(gh repo list --json nameWithOwner,visibility --limit 1000 | jq -r '.[] | select(.visibility == "PUBLIC") | .nameWithOwner')

if [ -z "$REPOS" ]; then
    echo -e "${RED}❌ No public repositories found${NC}"
    exit 1
fi

REPO_COUNT=$(echo "$REPOS" | wc -l | tr -d ' ')
echo -e "   Found ${GREEN}$REPO_COUNT${NC} public repositories"
echo ""

# Confirm before proceeding
echo -e "${YELLOW}⚠️  This will add webhooks to $REPO_COUNT repositories.${NC}"
read -p "   Continue? (yes/no): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy][Ee][Ss]$ ]] && [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Aborted by user${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🔧 Adding webhooks...${NC}"
echo "------------------------------------------------------------"

# Counters
SUCCESS=0
SKIP=0
ERROR=0
CURRENT=0

# Process each repository
while IFS= read -r REPO; do
    CURRENT=$((CURRENT + 1))
    echo -ne "[${CURRENT}/${REPO_COUNT}] ${REPO}... "
    
    # Check if webhook already exists
    EXISTING=$(gh api "/repos/$REPO/hooks" 2>/dev/null | jq -r --arg url "$WEBHOOK_URL" '.[] | select(.config.url == $url) | .id' || echo "")
    
    if [ -n "$EXISTING" ]; then
        echo -e "${YELLOW}⏭️  Already exists${NC}"
        SKIP=$((SKIP + 1))
        continue
    fi
    
    # Create webhook
    RESULT=$(gh api \
        -X POST \
        "/repos/$REPO/hooks" \
        -f name='web' \
        -f config[url]="$WEBHOOK_URL" \
        -f config[content_type]='json' \
        -f config[secret]="$WEBHOOK_SECRET" \
        -f config[insecure_ssl]='0' \
        -f events[]='issues' \
        -f events[]='issue_comment' \
        -f events[]='pull_request' \
        -f events[]='pull_request_review' \
        -f events[]='pull_request_review_comment' \
        -F active=true \
        2>&1)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Added${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        # Check error type
        if echo "$RESULT" | grep -q "403"; then
            echo -e "${RED}❌ Permission denied${NC}"
        elif echo "$RESULT" | grep -q "404"; then
            echo -e "${RED}❌ Not found${NC}"
        elif echo "$RESULT" | grep -q "422"; then
            echo -e "${YELLOW}⏭️  Already exists${NC}"
            SKIP=$((SKIP + 1))
            continue
        else
            echo -e "${RED}❌ Error${NC}"
        fi
        ERROR=$((ERROR + 1))
    fi
    
    # Rate limit protection (GitHub allows 5000 requests/hour)
    # Sleep briefly to avoid hitting rate limits
    sleep 0.1
    
done <<< "$REPOS"

# Summary
echo ""
echo "============================================================"
echo -e "${BLUE}📊 Summary:${NC}"
echo -e "   ${GREEN}✅ Successfully added:${NC} $SUCCESS"
echo -e "   ${YELLOW}⏭️  Already existed:${NC} $SKIP"
echo -e "   ${RED}❌ Errors:${NC} $ERROR"
echo -e "   ${BLUE}📦 Total repositories:${NC} $REPO_COUNT"
echo ""

if [ $SUCCESS -gt 0 ]; then
    echo -e "${GREEN}🎉 Webhook setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Test the webhooks by creating an issue in any repository"
    echo "2. Check Heroku logs: heroku logs --tail -a github-manager"
    echo "3. Verify webhook deliveries in GitHub repository settings"
fi

if [ $ERROR -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Some webhooks failed to install.${NC}"
    echo "   Common reasons:"
    echo "   - You don't have admin access to the repository"
    echo "   - The repository is archived"
    echo "   - Rate limit exceeded (wait a few minutes)"
fi

echo ""
echo -e "${BLUE}📝 To list all webhooks:${NC}"
echo "   ./scripts/setup_webhooks_gh.sh list"
echo ""
echo -e "${BLUE}📝 To remove all webhooks:${NC}"
echo "   ./scripts/setup_webhooks_gh.sh remove"

