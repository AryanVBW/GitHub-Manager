# 🚀 Quick Start: Fix 405 Error & Setup Webhooks

## ⚡ TL;DR - Run These Commands

### **1. Your Webhook Secret (Use Your Actual Value)**

Replace `YOUR_WEBHOOK_SECRET_HERE` with your actual secret from `.env` file:
```bash
# Your actual secret is in .env file, line 3
cat .env | grep GITHUB_WEBHOOK_SECRET
```

### **2. Update GitHub Webhook (Manual - 2 minutes)**

Go to: **https://github.com/AryanVBW/WIFIjam/settings/hooks**

Update these 3 fields:
1. **Payload URL**: `https://github-manager-d89575ed2bc3.herokuapp.com/webhook`
2. **Secret**: (paste your actual secret from .env)
3. **Events**: Uncheck "Pushes", Check: Issues, Issue comments, Pull requests

Click **"Update webhook"**

### **3. Test the Webhook**

```bash
# Watch logs in real-time
heroku logs --tail -a github-manager
```

Then create a test issue at: https://github.com/AryanVBW/WIFIjam/issues/new

### **4. Bulk Setup for All 218 Repos**

**Option A: GitHub CLI (Recommended - Faster)**

```bash
# Install (if not already installed)
brew install gh jq

# Authenticate
gh auth login

# Run setup
./scripts/setup_webhooks_gh.sh
```

**Option B: Python Script**

```bash
# Set environment variables (use your actual values from .env)
export GITHUB_TOKEN="$(grep GITHUB_TOKEN .env | cut -d '=' -f2)"
export GITHUB_WEBHOOK_SECRET="$(grep GITHUB_WEBHOOK_SECRET .env | cut -d '=' -f2)"
export WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"

# Run setup
python scripts/setup_webhooks.py setup
```

---

## 📋 What Was Fixed

### **Problem:**
```
❌ 405 Method Not Allowed
   URL: https://github-manager-d89575ed2bc3.herokuapp.com/
   Events: ["push"]
   Secret: "your_webhook_secret_here"
```

### **Solution:**
```
✅ 200 OK
   URL: https://github-manager-d89575ed2bc3.herokuapp.com/webhook
   Events: ["issues", "issue_comment", "pull_request", ...]
   Secret: YOUR_ACTUAL_SECRET
```

### **Changes Made:**
1. ✅ Updated `GITHUB_WEBHOOK_SECRET` on Heroku (v9)
2. ✅ Fixed `.env` file (removed malformed OPENAI_API_KEY prefix)
3. ✅ Created bulk webhook setup scripts (Python + GitHub CLI)
4. ✅ Added comprehensive documentation
5. ✅ Committed and pushed to GitHub

---

## 🎯 Current Status

### **Heroku App:**
- ✅ Running on: https://github-manager-d89575ed2bc3.herokuapp.com/
- ✅ Release: v9
- ✅ Status: Healthy
- ✅ Managing: 218 public repositories
- ✅ AI Provider: OpenAI (gpt-3.5-turbo)

### **Environment Variables:**
```bash
$ heroku config -a github-manager
AI_PROVIDER:           openai
FLASK_ENV:             production
GITHUB_TOKEN:          ghp_6E36...
GITHUB_WEBHOOK_SECRET: YOUR_ACTUAL_SECRET
OPENAI_API_KEY:        sk-proj-v9w4...
OPENAI_MODEL:          gpt-3.5-turbo
SYSTEM_PROMPT:         You are a helpful GitHub assistant...
```

### **Webhook Endpoint:**
```bash
$ curl -X POST https://github-manager-d89575ed2bc3.herokuapp.com/webhook
{"error":"Invalid signature"}  # ✅ Correct (401, not 405)
```

---

## 📝 Step-by-Step Instructions

### **Step 1: Get Your Actual Secret**

```bash
# View your actual webhook secret
grep GITHUB_WEBHOOK_SECRET .env
```

Copy the value after the `=` sign.

### **Step 2: Update Webhook in GitHub**

1. Open: https://github.com/AryanVBW/WIFIjam/settings/hooks
2. Click on your webhook (the one with wrong URL)
3. Update:
   - **Payload URL**: Add `/webhook` at the end
   - **Secret**: Paste your actual secret
   - **Events**: 
     - ❌ Uncheck "Pushes"
     - ✅ Check "Issues"
     - ✅ Check "Issue comments"
     - ✅ Check "Pull requests"
     - ✅ Check "Pull request reviews"
     - ✅ Check "Pull request review comments"
4. Click **"Update webhook"**

### **Step 3: Test the Webhook**

**Terminal 1: Watch Logs**
```bash
heroku logs --tail -a github-manager | grep -E "webhook|issue|comment"
```

**Terminal 2: Create Test Issue**
```bash
# Using GitHub CLI
gh issue create \
  --repo AryanVBW/WIFIjam \
  --title "Test Bot Response" \
  --body "Testing webhook integration. @bot hello!"
```

**Or manually:**
1. Go to: https://github.com/AryanVBW/WIFIjam/issues/new
2. Title: "Test Bot Response"
3. Body: "Testing webhook integration"
4. Click "Submit new issue"

**Expected Result:**
- ✅ Bot responds within 3 seconds
- ✅ Logs show: "Received issues event"
- ✅ Logs show: "Posted comment on issue"

### **Step 4: Bulk Setup (Choose One Method)**

#### **Method A: GitHub CLI (Faster)**

```bash
# Check if gh is installed
gh --version

# If not installed:
brew install gh jq

# Authenticate (if not already)
gh auth status || gh auth login

# Run setup script
./scripts/setup_webhooks_gh.sh
```

**Expected Output:**
```
🚀 GitHub Webhook Bulk Setup (using gh CLI)
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
[1/218] AryanVBW/WIFIjam... ⏭️  Already exists
[2/218] AryanVBW/repo2... ✅ Added
...
[218/218] AryanVBW/repo218... ✅ Added

============================================================
📊 Summary:
   ✅ Successfully added: 217
   ⏭️  Already existed: 1
   ❌ Errors: 0
   📦 Total repositories: 218

🎉 Webhook setup complete!
```

#### **Method B: Python Script**

```bash
# Check if PyGithub is installed
python -c "import github" 2>/dev/null && echo "✅ PyGithub installed" || pip install PyGithub

# Set environment variables from .env
export GITHUB_TOKEN="$(grep GITHUB_TOKEN .env | cut -d '=' -f2)"
export GITHUB_WEBHOOK_SECRET="$(grep GITHUB_WEBHOOK_SECRET .env | cut -d '=' -f2)"
export WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"

# Run setup
python scripts/setup_webhooks.py setup
```

**Expected Output:**
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
[1/218] AryanVBW/WIFIjam... ⏭️  Already exists
[2/218] AryanVBW/repo2... ✅ Added
...

============================================================
📊 Summary:
   ✅ Successfully added: 217
   ⏭️  Already existed: 1
   ❌ Errors: 0
   📦 Total repositories: 218

🎉 Webhook setup complete!
```

---

## ✅ Verification

### **Check Webhook Status:**

```bash
# List all webhooks
python scripts/setup_webhooks.py list

# Or check specific repo
gh api /repos/AryanVBW/WIFIjam/hooks | jq '.[] | {url: .config.url, events}'
```

### **Test Multiple Repos:**

```bash
# Create test issues in different repos
gh issue create --repo AryanVBW/repo1 --title "Test" --body "Testing bot"
gh issue create --repo AryanVBW/repo2 --title "Test" --body "Testing bot"
gh issue create --repo AryanVBW/repo3 --title "Test" --body "Testing bot"
```

### **Monitor Activity:**

```bash
# Watch logs for all webhook events
heroku logs --tail -a github-manager | grep -E "Received|Processing|Posted"
```

---

## 🎉 Success Indicators

You'll know it's working when:

✅ **Webhook Deliveries:**
- Status: 200 OK (not 405 or 401)
- Response: `{"status": "processed"}`

✅ **Bot Behavior:**
- Responds to new issues within 3 seconds
- Provides helpful, personalized responses
- Uses humble, respectful tone
- Analyzes user writing style

✅ **Heroku Logs:**
```
✅ Received issues event
✅ Processing issue #1 in AryanVBW/repo
✅ Analyzing user writing style
✅ Generating personalized response
✅ Posted comment on issue #1
```

✅ **GitHub Activity:**
- Bot comments appear on issues
- Comments are from your account (AryanVBW)
- No "I'm a bot" signatures
- Natural, helpful responses

---

## 🐛 Quick Troubleshooting

### **405 Error Still Occurring?**
```bash
# Check webhook URL
gh api /repos/AryanVBW/WIFIjam/hooks | jq '.[].config.url'
# Should end with /webhook
```

### **401 Unauthorized?**
```bash
# Verify secrets match
heroku config:get GITHUB_WEBHOOK_SECRET -a github-manager
# Compare with GitHub webhook secret
```

### **Bot Not Responding?**
```bash
# Check app status
heroku ps -a github-manager

# Check logs for errors
heroku logs --tail -a github-manager | grep ERROR

# Test health endpoint
curl https://github-manager-d89575ed2bc3.herokuapp.com/health | jq
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `QUICK_START.md` | This file - Quick setup guide |
| `405_ERROR_FIX_SUMMARY.md` | Complete problem analysis and fix |
| `WEBHOOK_VERIFICATION_GUIDE.md` | Detailed testing instructions |
| `WEBHOOK_SETUP_COMPARISON.md` | Compare setup methods |
| `GITHUB_APP_SETUP.md` | Create GitHub App (advanced) |
| `scripts/README.md` | Script usage documentation |

---

## 🚀 You're All Set!

After completing these steps, your GitHub Manager will:

✅ Manage all 218 public repositories  
✅ Respond to issues and pull requests automatically  
✅ Provide personalized, helpful responses  
✅ Use humble, respectful communication  
✅ Analyze user writing styles  
✅ Work 24/7 without manual intervention  

**Happy automating! 🎊**

