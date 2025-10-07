# Setup and Deployment Guide

This guide will walk you through setting up and deploying the GitHub Manager bot to Heroku.

## 📋 Prerequisites

- A GitHub account with a repository to manage
- A Heroku account (free tier works fine)
- Python 3.11+ installed locally (for testing)
- Git installed locally

## 🔑 Step 1: Create GitHub Personal Access Token

### Important: Use Classic Personal Access Token

**You MUST use a Classic Personal Access Token, NOT a Fine-grained token.**

Fine-grained tokens have limitations that prevent the bot from working across multiple repositories. Classic tokens are required for multi-repository management.

### Step-by-Step Token Creation

1. **Navigate to Token Settings**
   - Go to GitHub Settings → Developer settings → Personal access tokens → **Tokens (classic)**
   - Direct link: https://github.com/settings/tokens
   - **DO NOT** use "Fine-grained tokens" - use "Tokens (classic)"

2. **Generate New Token**
   - Click "Generate new token" → "Generate new token (classic)"
   - You may need to confirm your password

3. **Configure Token Details**
   - **Note**: Give it a descriptive name (e.g., "GitHub Manager Bot - Multi-Repo")
   - **Expiration**: Recommended "No expiration" for production use
     - If you choose an expiration date, set a calendar reminder to regenerate before it expires

4. **Select Required Permissions** (CRITICAL - Follow Exactly)

   #### ✅ Required Permissions for Public Repositories Only:

   **repo section:**
   - ✅ `public_repo` - Access public repositories
     - *Why needed*: Read and write to issues, PRs, and comments in public repos

   **admin:org section (if managing organization repos):**
   - ✅ `read:org` - Read org and team membership
     - *Why needed*: Access organization repositories

   **user section:**
   - ✅ `read:user` - Read user profile data
     - *Why needed*: Identify the authenticated user and analyze user activity

   #### ✅ Additional Permissions for Private Repositories:

   If you want to manage private repositories, also select:

   **repo section:**
   - ✅ `repo` - Full control of private repositories
     - *Why needed*: Access private repositories
     - *Note*: This grants full access to private repos, so use carefully

5. **Generate and Save Token**
   - Click "Generate token" at the bottom
   - **CRITICAL**: Copy the token immediately (starts with `ghp_`)
   - Save it securely - you won't be able to see it again!
   - Store it in a password manager or secure note

### 🔒 Security & Permission Details

#### What These Permissions Allow:
- ✅ Read all public repositories you own
- ✅ Read issues and pull requests
- ✅ Create comments on issues and pull requests
- ✅ Assign issues to users
- ✅ Read user profiles and activity
- ✅ Access organization repositories (if `read:org` is selected)

#### What These Permissions PREVENT:
- ❌ **Cannot delete repositories** (no `delete_repo` permission)
- ❌ **Cannot force push** (no `repo:write` for protected branches)
- ❌ **Cannot delete branches** (no branch deletion permission)
- ❌ **Cannot modify repository settings** (no `admin:repo` permission)
- ❌ **Cannot create or delete repositories** (no creation/deletion permissions)
- ❌ **Cannot modify webhooks** (no webhook management permission)
- ❌ **Cannot access repository secrets** (no secrets permission)

#### Permission Scope Explanation:

| Permission | What It Does | Why We Need It | Risk Level |
|------------|--------------|----------------|------------|
| `public_repo` | Read/write public repos | Access issues, PRs, comments | Low |
| `read:org` | Read org membership | Access org repositories | Very Low |
| `read:user` | Read user profiles | Analyze user activity patterns | Very Low |
| `repo` (optional) | Full private repo access | Manage private repositories | Medium |

### ⚠️ Important Security Notes

1. **Token Storage**:
   - Never commit tokens to git
   - Never share tokens publicly
   - Store in environment variables only
   - Use password managers for backup

2. **Token Rotation**:
   - Rotate tokens every 90 days for security
   - Set calendar reminders
   - Update Heroku config when rotating

3. **Minimal Permissions**:
   - Only select permissions you actually need
   - Don't select `repo` unless you need private repo access
   - Review permissions periodically

4. **Monitoring**:
   - Check GitHub's "Settings → Developer settings → Personal access tokens" regularly
   - Review token usage and last used date
   - Revoke unused or suspicious tokens immediately

### 🎯 Quick Checklist

Before proceeding, verify:
- [ ] Used "Tokens (classic)" NOT "Fine-grained tokens"
- [ ] Selected `public_repo` permission
- [ ] Selected `read:user` permission
- [ ] Selected `read:org` if managing org repos
- [ ] Token starts with `ghp_`
- [ ] Token saved securely
- [ ] Understand what the token can and cannot do

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
heroku config:set GITHUB_WEBHOOK_SECRET="your_random_secret_here"

# Required: AI Configuration (choose one)
# Option A: Gemini (Recommended - Free Tier)
heroku config:set AI_PROVIDER="gemini"
heroku config:set GEMINI_API_KEY="your_gemini_api_key_here"
heroku config:set GEMINI_MODEL="gemini-pro"  # Options: gemini-pro, gemini-1.5-pro, gemini-1.5-flash

# Option B: OpenAI
heroku config:set AI_PROVIDER="openai"
heroku config:set OPENAI_API_KEY="your_openai_api_key_here"
heroku config:set OPENAI_MODEL="gpt-3.5-turbo"  # Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini

# Optional: Custom System Prompt (defines bot personality)
# Leave unset to use default, or customize:
heroku config:set SYSTEM_PROMPT="You are a helpful and professional GitHub assistant. Be concise and actionable."

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

### 📝 Environment Variables Explained

#### Required Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_TOKEN` | Classic Personal Access Token | `ghp_abc123...` |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook verification | `a1b2c3d4...` (32+ chars) |
| `AI_PROVIDER` | AI service to use | `gemini` or `openai` |
| `GEMINI_API_KEY` | Gemini API key (if using Gemini) | Your Gemini key |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | `sk-...` |

#### Optional Variables:

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `GEMINI_MODEL` | Gemini model to use | `gemini-pro` | `gemini-pro`, `gemini-1.5-pro`, `gemini-1.5-flash` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` | `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-4o-mini` |
| `SYSTEM_PROMPT` | Custom AI personality | Default prompt | Any custom prompt |
| `RESEND_API_KEY` | Resend API key for emails | None | `re_...` |
| `OWNER_EMAIL` | Email for notifications | None | `you@example.com` |
| `LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### 🎨 Customizing System Prompt

The `SYSTEM_PROMPT` variable allows you to customize the bot's personality and response style. Here are some examples:

**Default (if not set):**
```
You are a helpful, humble, and professional GitHub assistant. Your responses should be concise, respectful, and actionable. Always maintain a friendly and supportive tone. Keep responses brief and to the point.
```

**Formal and Technical:**
```bash
heroku config:set SYSTEM_PROMPT="You are a technical GitHub assistant. Provide detailed, precise responses with code examples when relevant. Use formal language and technical terminology."
```

**Casual and Friendly:**
```bash
heroku config:set SYSTEM_PROMPT="You are a friendly GitHub helper. Keep things casual and approachable. Use simple language and be encouraging. Add relevant emojis when appropriate."
```

**Brief and Direct:**
```bash
heroku config:set SYSTEM_PROMPT="You are a concise GitHub assistant. Give brief, direct answers. No fluff. Get straight to the point."
```

**Educational:**
```bash
heroku config:set SYSTEM_PROMPT="You are an educational GitHub mentor. Explain concepts clearly, provide learning resources, and encourage best practices. Be patient and thorough."
```

### 🤖 AI Model Selection Guide

#### Gemini Models:

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| `gemini-pro` | Fast | Good | Free | General use, high volume |
| `gemini-1.5-pro` | Medium | Excellent | Free | Complex questions, detailed responses |
| `gemini-1.5-flash` | Very Fast | Good | Free | Quick responses, simple questions |

#### OpenAI Models:

| Model | Speed | Quality | Cost/1K tokens | Best For |
|-------|-------|---------|----------------|----------|
| `gpt-3.5-turbo` | Fast | Good | $0.002 | General use, cost-effective |
| `gpt-4` | Slow | Excellent | $0.03 | Complex reasoning, high quality |
| `gpt-4-turbo` | Medium | Excellent | $0.01 | Balance of speed and quality |
| `gpt-4o` | Fast | Excellent | $0.005 | Best overall balance |
| `gpt-4o-mini` | Very Fast | Good | $0.0015 | Cost-effective, simple tasks |

**Recommendation**: Start with `gemini-pro` (free) or `gpt-3.5-turbo` (cheap), then upgrade if needed.

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

## 🔗 Step 5: Configure GitHub Webhooks

### Multi-Repository Support

The GitHub Manager now supports **all your public repositories automatically**! You need to set up webhooks for each repository you want to manage.

### Option A: Organization-Wide Webhook (Recommended for Multiple Repos)

If you have an organization with multiple repositories:

1. Go to your GitHub Organization Settings
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
7. This webhook will now work for ALL repositories in your organization!

### Option B: Individual Repository Webhooks

For each repository you want to manage:

1. Go to the GitHub repository
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

### Webhook Events Explained

| Event | When It Triggers | What the Bot Does |
|-------|------------------|-------------------|
| Issue comments | Someone comments on an issue | Analyzes user style, generates personalized AI response |
| Issues | Issue opened/closed/assigned | Handles issue assignment requests |
| Pull requests | PR opened/closed/merged | Welcomes new PRs, congratulates on merge |
| PR review comments | Comment on PR code | Generates personalized AI response |

### Verifying Webhooks

After adding webhooks:

1. Go to the webhook settings page
2. Click on the webhook you just created
3. Scroll to "Recent Deliveries"
4. You should see a ping event with a green checkmark ✅
5. If you see a red X ❌, click on it to see the error details

Common issues:
- **404 Not Found**: Check your Payload URL is correct
- **500 Internal Server Error**: Check Heroku logs for errors
- **Signature verification failed**: Check your webhook secret matches

## ✅ Step 6: Test the Bot

### Test 1: Multi-Repository Detection

1. Visit your app's health endpoint:
   ```bash
   curl https://your-app-name.herokuapp.com/health
   ```
2. You should see:
   - Your authenticated username
   - Number of public repositories being managed
   - AI provider and model being used
   - Feature flags showing multi-repo and personalized responses enabled

### Test 2: Issue Assignment

1. Create a test issue in any of your public repositories
2. Comment "assign me" on the issue
3. The bot should:
   - Assign the issue to you
   - Respond with a confirmation message (as you, not as a bot)
   - Message should be professional and humble

### Test 3: Personalized AI Responses

1. Comment a question on any issue or PR
2. The bot should:
   - Analyze your previous comment history
   - Generate a response matching your writing style
   - Respond as the authenticated user (you), not as a bot
   - Provide helpful, context-aware answers

**Try different types of questions:**
- Technical: "How do I implement this feature?"
- Clarification: "What does this error mean?"
- Discussion: "What do you think about this approach?"

### Test 4: User-Specific Responses

1. Have multiple users comment on the same issue
2. Each user should receive responses tailored to their:
   - Writing style (formal vs casual)
   - Comment length preferences
   - Emoji usage patterns
   - Technical level

### Test 5: Pull Request Handling

1. Create a test pull request
2. The bot should welcome the PR (as you, not as a bot)
3. Comment on the PR with a question
4. The bot should respond with context about the PR changes

### Test 6: Email Notifications (if configured)

1. Check your email for notifications about the test activities
2. Emails should include:
   - Issue/PR number and title
   - Activity type
   - Link to the issue/PR

### Expected Behavior

✅ **Correct Behavior:**
- Responses appear as comments from your GitHub account
- No "I'm a bot" or bot signatures
- Responses match each user's communication style
- Professional, humble, and helpful tone
- Works across all your public repositories

❌ **Incorrect Behavior:**
- Responses appear as a separate bot account
- Generic responses for all users
- Bot identifies itself as a bot
- Only works on one repository

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

