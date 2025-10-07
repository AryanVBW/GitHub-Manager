# GitHub App Setup Guide

## Why Create a GitHub App?

A GitHub App allows users to install your bot to their account with a single click, automatically applying to all their repositories (or selected ones). This is the **best solution** for user-wide deployment.

## Benefits Over Webhooks:

- ✅ **One-Click Installation**: Users can install to all repos at once
- ✅ **Automatic Updates**: New repos automatically get the bot
- ✅ **Better Permissions**: Fine-grained access control
- ✅ **User-Friendly**: No manual webhook configuration needed
- ✅ **Scalable**: Works for organizations and personal accounts

## Step-by-Step: Create a GitHub App

### 1. Navigate to GitHub App Settings

```
GitHub.com → Your Profile → Settings → Developer settings → 
GitHub Apps → New GitHub App
```

### 2. Basic Information

**GitHub App name:**
```
GitHub Manager Bot
```

**Description:**
```
AI-powered GitHub assistant that helps manage issues and pull requests with intelligent, personalized responses.
```

**Homepage URL:**
```
https://github.com/AryanVBW/GitHub-Manager
```

### 3. Webhook Configuration

**Webhook URL:**
```
https://github-manager-d89575ed2bc3.herokuapp.com/webhook
```

**Webhook secret:**
```
YOUR_WEBHOOK_SECRET_HERE
```

**✅ Active:** Check this box

### 4. Permissions

#### **Repository permissions:**

| Permission | Access Level | Why Needed |
|------------|--------------|------------|
| Issues | **Read & write** | Create and respond to issues |
| Pull requests | **Read & write** | Manage and respond to PRs |
| Metadata | **Read-only** | Access repository metadata |

#### **Organization permissions:**
- None required (leave all as "No access")

#### **User permissions:**
- None required (leave all as "No access")

### 5. Subscribe to Events

Check these events:

- ✅ Issues
- ✅ Issue comment
- ✅ Pull request
- ✅ Pull request review
- ✅ Pull request review comment

### 6. Where can this GitHub App be installed?

Choose one:

- **Option 1**: "Only on this account" (for personal use)
- **Option 2**: "Any account" (to allow others to install)

### 7. Create the App

Click **"Create GitHub App"**

### 8. Generate Private Key

After creation:

1. Scroll down to **"Private keys"**
2. Click **"Generate a private key"**
3. Save the downloaded `.pem` file securely
4. You'll need this for authentication

### 9. Note Your App ID

At the top of the page, you'll see:
```
App ID: 123456
```
Save this number - you'll need it for configuration.

### 10. Install the App

1. Click **"Install App"** in the left sidebar
2. Select your account
3. Choose:
   - **All repositories** (recommended)
   - Or select specific repositories
4. Click **"Install"**

## Update Your Application Code

You'll need to modify your GitHub Manager to support GitHub App authentication instead of Personal Access Token.

### Required Environment Variables:

```bash
# GitHub App Configuration
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
GITHUB_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE

# Keep existing variables
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-3.5-turbo
SYSTEM_PROMPT="..."
```

### Code Changes Needed:

1. Install GitHub App authentication library:
   ```bash
   pip install PyGithub[app]
   ```

2. Update `src/github_client.py` to use App authentication
3. Handle installation events
4. Use installation access tokens instead of PAT

## Installation URL for Users

After creating the app, share this URL:

```
https://github.com/apps/github-manager-bot/installations/new
```

Users can click this link to install the bot to their account!

## Advantages of This Approach

1. **No Manual Webhook Setup**: Users don't need to configure webhooks
2. **Automatic for New Repos**: Works on new repositories automatically
3. **Easy Uninstall**: Users can uninstall anytime from their settings
4. **Better Security**: Fine-grained permissions, no need for full PAT
5. **Professional**: Appears in GitHub Marketplace (optional)

## Next Steps

Would you like me to:
1. Update the code to support GitHub App authentication?
2. Create a migration guide from PAT to GitHub App?
3. Add installation instructions to your README?

