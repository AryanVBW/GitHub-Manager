# Setup and Deployment Guide

This guide will walk you through setting up and deploying the GitHub Manager bot to Heroku.

## 📋 Prerequisites

- A GitHub account with a repository to manage
- A Heroku account (free tier works fine)
- Python 3.11+ installed locally (for testing)
- Git installed locally

## 🔑 Step 1: Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or visit: https://github.com/settings/tokens

2. Click "Generate new token" → "Generate new token (classic)"

3. Give your token a descriptive name (e.g., "GitHub Manager Bot")

4. Set expiration (recommend "No expiration" for production use)

5. **Select the following permissions** (IMPORTANT - only these):
   
   **Repository permissions:**
   - ✅ `repo:status` - Access commit status
   - ✅ `repo_deployment` - Access deployment status
   - ✅ `public_repo` - Access public repositories
   - ✅ `repo:invite` - Access repository invitations
   
   **For private repositories, also select:**
   - ✅ `repo` (Full control of private repositories)
   
   **Additional permissions:**
   - ✅ `read:org` - Read org and team membership
   - ✅ `read:user` - Read user profile data
   - ✅ `user:email` - Access user email addresses

6. Click "Generate token"

7. **IMPORTANT**: Copy the token immediately and save it securely. You won't be able to see it again!

### ⚠️ Security Notes

The permissions above are carefully selected to:
- ✅ Allow reading issues and pull requests
- ✅ Allow commenting on issues and pull requests
- ✅ Allow assigning issues
- ❌ **Prevent** repository deletion
- ❌ **Prevent** force pushing
- ❌ **Prevent** branch deletion
- ❌ **Prevent** repository settings modification

## 🤖 Step 2: Get AI API Key

Choose **ONE** of the following AI providers:

### Option A: Google Gemini (Recommended - Free Tier Available)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. Copy the API key
5. Save it securely

**Pricing**: Free tier includes 60 requests per minute

### Option B: OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Give it a name (e.g., "GitHub Manager")
5. Copy the API key
6. Save it securely

**Pricing**: Pay-as-you-go, approximately $0.002 per request with GPT-3.5-turbo

## 📧 Step 3: Set Up Email Notifications (Optional)

Email notifications are **completely optional**. Skip this step if you don't need email alerts.

### Using Resend

1. Go to [Resend](https://resend.com/)
2. Sign up for a free account
3. Verify your email
4. Go to API Keys section
5. Create a new API key
6. Copy the API key
7. Save it securely

**Pricing**: Free tier includes 100 emails per day

## 🚀 Step 4: Deploy to Heroku

### 4.1 Install Heroku CLI

Download and install from: https://devcenter.heroku.com/articles/heroku-cli

### 4.2 Clone and Prepare Repository

```bash
# Clone your repository (or create a new one)
git clone https://github.com/yourusername/github-manager.git
cd github-manager

# Or if starting fresh, initialize git
git init
git add .
git commit -m "Initial commit"
```

### 4.3 Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-github-manager-app

# Or if you want Heroku to generate a name
heroku create
```

### 4.4 Configure Environment Variables

Set all required environment variables:

```bash
# Required: GitHub Configuration
heroku config:set GITHUB_TOKEN="your_github_token_here"
heroku config:set GITHUB_REPO="owner/repository-name"
heroku config:set GITHUB_WEBHOOK_SECRET="your_random_secret_here"

# Required: AI Configuration (choose one)
# Option A: Gemini
heroku config:set AI_PROVIDER="gemini"
heroku config:set GEMINI_API_KEY="your_gemini_api_key_here"

# Option B: OpenAI
heroku config:set AI_PROVIDER="openai"
heroku config:set OPENAI_API_KEY="your_openai_api_key_here"

# Optional: Email Configuration
heroku config:set RESEND_API_KEY="your_resend_api_key_here"
heroku config:set OWNER_EMAIL="your-email@example.com"

# Optional: Application Configuration
heroku config:set LOG_LEVEL="INFO"
heroku config:set FLASK_ENV="production"
```

**Generate a webhook secret:**
```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
-join ((48..57) + (97..102) | Get-Random -Count 32 | % {[char]$_})
```

### 4.5 Deploy to Heroku

```bash
# Add Heroku remote (if not already added)
heroku git:remote -a your-github-manager-app

# Push to Heroku
git push heroku main

# Or if your branch is named 'master'
git push heroku master
```

### 4.6 Verify Deployment

```bash
# Check logs
heroku logs --tail

# Open the app
heroku open

# Check status
curl https://your-app-name.herokuapp.com/health
```

## 🔗 Step 5: Configure GitHub Webhook

1. Go to your GitHub repository
2. Navigate to Settings → Webhooks → Add webhook

3. Configure the webhook:
   - **Payload URL**: `https://your-app-name.herokuapp.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Use the same secret you set in `GITHUB_WEBHOOK_SECRET`
   
4. Select events to trigger:
   - ✅ Issue comments
   - ✅ Issues
   - ✅ Pull requests
   - ✅ Pull request reviews
   - ✅ Pull request review comments

5. Ensure "Active" is checked

6. Click "Add webhook"

7. GitHub will send a test ping. Check that it shows a green checkmark.

## ✅ Step 6: Test the Bot

### Test Issue Assignment

1. Create a test issue in your repository
2. Comment "assign me" on the issue
3. The bot should assign the issue to you and respond

### Test AI Responses

1. Comment a question on any issue or PR
2. The bot should respond with a helpful answer

### Test Email Notifications (if configured)

1. Check your email for notifications about the test activities

## 🔍 Monitoring and Logs

### View Logs

```bash
# Real-time logs
heroku logs --tail

# Last 100 lines
heroku logs -n 100

# Filter by source
heroku logs --source app
```

### Check Application Status

```bash
# Check dyno status
heroku ps

# Check config
heroku config

# Restart if needed
heroku restart
```

## 🐛 Troubleshooting

### Bot Not Responding

1. **Check Heroku logs**:
   ```bash
   heroku logs --tail
   ```

2. **Verify environment variables**:
   ```bash
   heroku config
   ```

3. **Check webhook delivery**:
   - Go to GitHub repo → Settings → Webhooks
   - Click on your webhook
   - Check "Recent Deliveries" tab
   - Look for failed deliveries

4. **Verify bot permissions**:
   - Ensure GitHub token has correct permissions
   - Check that webhook secret matches

### Rate Limit Issues

If you see rate limit errors:
- The bot automatically handles rate limits
- Wait for the rate limit to reset
- Consider upgrading your GitHub plan for higher limits

### AI Response Failures

If AI responses aren't working:
- Verify your AI API key is correct
- Check your AI provider's quota/billing
- Review logs for specific error messages

### Email Not Sending

If emails aren't being sent:
- Verify Resend API key is correct
- Check Resend dashboard for delivery status
- Ensure OWNER_EMAIL is set correctly
- Remember: Email is optional, bot works without it

## 🔄 Updating the Bot

```bash
# Pull latest changes
git pull origin main

# Push to Heroku
git push heroku main

# Check logs
heroku logs --tail
```

## 💰 Cost Considerations

### Heroku
- **Free Tier**: 550-1000 free dyno hours per month
- **Hobby Tier**: $7/month for always-on dyno

### AI Providers
- **Gemini**: Free tier with 60 requests/minute
- **OpenAI**: ~$0.002 per request (GPT-3.5-turbo)

### Resend (Optional)
- **Free Tier**: 100 emails/day
- **Paid**: Starting at $20/month for 50,000 emails

## 🆘 Getting Help

If you encounter issues:

1. Check the logs: `heroku logs --tail`
2. Review this setup guide
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. Verify all environment variables are set correctly
5. Test webhook delivery in GitHub settings

## 🔐 Security Best Practices

1. **Never commit secrets** to your repository
2. **Rotate tokens** periodically
3. **Use webhook secrets** to verify requests
4. **Monitor logs** for suspicious activity
5. **Keep dependencies updated**: `pip list --outdated`

---

Congratulations! Your GitHub Manager bot should now be up and running. 🎉

