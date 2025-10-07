# Webhook Management Scripts

## Overview

This directory contains scripts to help you manage GitHub webhooks across all your repositories.

## 📋 Available Scripts

### 1. `setup_webhooks.py` - Bulk Webhook Setup

Automatically adds webhooks to all your public repositories with a single command.

#### **Usage:**

```bash
# Set environment variables
export GITHUB_TOKEN="ghp_YOUR_GITHUB_TOKEN_HERE"
export GITHUB_WEBHOOK_SECRET="YOUR_WEBHOOK_SECRET_HERE"
export WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"

# Run the setup script
python scripts/setup_webhooks.py setup
```

#### **What it does:**

1. ✅ Authenticates with GitHub using your token
2. ✅ Fetches all your public repositories
3. ✅ Checks if webhooks already exist (skips duplicates)
4. ✅ Adds webhooks to repositories that don't have them
5. ✅ Provides a detailed summary of results

#### **Example Output:**

```
🚀 GitHub Webhook Bulk Setup
============================================================
📍 Webhook URL: https://github-manager-d89575ed2bc3.herokuapp.com/webhook
🔐 Secret: ****************************

✅ Authenticated as: AryanVBW

📦 Fetching your public repositories...
   Found 218 public repositories

⚠️  This will add webhooks to 218 repositories.
   Continue? (yes/no): yes

🔧 Adding webhooks...
------------------------------------------------------------
[1/218] AryanVBW/repo1... ✅ Added
[2/218] AryanVBW/repo2... ⏭️  Already exists
[3/218] AryanVBW/repo3... ✅ Added
...

============================================================
📊 Summary:
   ✅ Successfully added: 180
   ⏭️  Already existed: 35
   ❌ Errors: 3
   📦 Total repositories: 218

🎉 Webhook setup complete!
```

---

### 2. List Existing Webhooks

View all webhooks currently configured across your repositories.

#### **Usage:**

```bash
export GITHUB_TOKEN="ghp_YOUR_GITHUB_TOKEN_HERE"
python scripts/setup_webhooks.py list
```

#### **Example Output:**

```
📋 Listing Existing Webhooks
============================================================

📦 AryanVBW/GitHub-Manager
   ✅ https://github-manager-d89575ed2bc3.herokuapp.com/webhook
      Events: issues, issue_comment, pull_request

📦 AryanVBW/another-repo
   ✅ https://github-manager-d89575ed2bc3.herokuapp.com/webhook
      Events: issues, issue_comment, pull_request

============================================================
Total webhooks found: 2
```

---

### 3. Remove Webhooks

Remove webhooks from all repositories (useful for cleanup or migration).

#### **Usage:**

```bash
export GITHUB_TOKEN="ghp_YOUR_GITHUB_TOKEN_HERE"
export WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"
python scripts/setup_webhooks.py remove
```

⚠️ **Warning:** This will remove webhooks matching the URL from ALL repositories!

---

## 🔧 Installation

The script uses PyGithub, which is already in your requirements.txt:

```bash
pip install -r requirements.txt
```

Or install just PyGithub:

```bash
pip install PyGithub
```

---

## 🔐 Security Notes

1. **Never commit your tokens**: The script reads from environment variables
2. **Use .env file**: Store tokens in `.env` (already in .gitignore)
3. **Token permissions**: Requires `repo` scope for webhook management
4. **Webhook secret**: Keep your webhook secret secure

---

## 🚀 Quick Start Guide

### **Step 1: Set Environment Variables**

Create a `.env` file or export variables:

```bash
# Option 1: Export directly
export GITHUB_TOKEN="ghp_YOUR_GITHUB_TOKEN_HERE"
export GITHUB_WEBHOOK_SECRET="YOUR_WEBHOOK_SECRET_HERE"

# Option 2: Use .env file (recommended)
# The script will automatically load from .env if python-dotenv is installed
```

### **Step 2: Run the Script**

```bash
# Add webhooks to all repositories
python scripts/setup_webhooks.py setup

# List existing webhooks
python scripts/setup_webhooks.py list

# Remove webhooks
python scripts/setup_webhooks.py remove
```

### **Step 3: Verify**

Check Heroku logs to see webhook events:

```bash
heroku logs --tail -a github-manager
```

---

## 📊 Comparison: Script vs Manual vs GitHub App

| Feature | Bulk Script | Manual Setup | GitHub App |
|---------|-------------|--------------|------------|
| **Setup Time** | 2 minutes | Hours | 30 minutes |
| **Maintenance** | Re-run for new repos | Manual per repo | Automatic |
| **User-Friendly** | Technical | Technical | One-click |
| **Scalability** | Good | Poor | Excellent |
| **Best For** | Personal use | Single repo | Public distribution |

---

## 🐛 Troubleshooting

### **Error: "Permission denied"**

You need admin access to the repository to add webhooks.

**Solution:** The script will skip repositories where you don't have admin access.

### **Error: "Rate limit exceeded"**

GitHub API has rate limits (5000 requests/hour).

**Solution:** Wait a few minutes and try again.

### **Error: "GITHUB_TOKEN not set"**

Environment variable is missing.

**Solution:**
```bash
export GITHUB_TOKEN="your_token_here"
```

### **Webhook not triggering**

**Check:**
1. Webhook is active in repository settings
2. Webhook URL is correct
3. Secret matches between GitHub and Heroku
4. Heroku app is running: `heroku ps -a github-manager`
5. Check webhook delivery logs in GitHub

---

## 📝 Advanced Usage

### **Custom Webhook URL**

```bash
export WEBHOOK_URL="https://your-custom-domain.com/webhook"
python scripts/setup_webhooks.py setup
```

### **Dry Run (Check without adding)**

Modify the script to add a `--dry-run` flag:

```python
# In setup_webhooks() function, add:
if args.dry_run:
    print(f"Would add webhook to {repo_name}")
    continue
```

### **Filter by Repository Name**

Add filtering logic:

```python
# Only add to repos matching pattern
if 'pattern' in repo.name:
    # Add webhook
```

---

## 🎯 Next Steps

After running the script:

1. ✅ Test by creating an issue in any repository
2. ✅ Monitor Heroku logs: `heroku logs --tail -a github-manager`
3. ✅ Check webhook deliveries in GitHub repository settings
4. ✅ Verify bot responses in issues/PRs

---

## 📚 Additional Resources

- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Heroku Logs](https://devcenter.heroku.com/articles/logging)

