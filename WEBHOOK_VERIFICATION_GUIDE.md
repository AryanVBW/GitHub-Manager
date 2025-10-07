# Webhook Verification & Testing Guide

## ✅ Current Status

### **Heroku Configuration:**
- ✅ `GITHUB_WEBHOOK_SECRET` updated to: `YOUR_WEBHOOK_SECRET_HERE`
- ✅ App restarted successfully (v9)
- ✅ Webhook endpoint `/webhook` is accepting POST requests
- ✅ Signature verification is working (returns 401 for invalid signatures)

### **What You Need to Do:**

1. **Update the webhook in GitHub repository: AryanVBW/WIFIjam**
2. **Test the webhook**
3. **Bulk setup for all 218 repositories**

---

## 1. 🔧 Update Webhook in GitHub (Manual Method)

### **Step-by-Step Instructions:**

#### **A. Navigate to Webhook Settings**

1. Go to: **https://github.com/AryanVBW/WIFIjam/settings/hooks**
2. You should see your existing webhook
3. Click on the webhook URL to edit it

#### **B. Update Configuration**

**Change these fields:**

| Field | Current (Wrong) | Correct Value |
|-------|----------------|---------------|
| **Payload URL** | `https://github-manager-d89575ed2bc3.herokuapp.com/` | `https://github-manager-d89575ed2bc3.herokuapp.com/webhook` |
| **Secret** | `your_webhook_secret_here` | `YOUR_WEBHOOK_SECRET_HERE` |
| **Events** | `["push"]` | See below ⬇️ |

**Events Configuration:**

1. Select: **"Let me select individual events"**
2. **Uncheck:**
   - ❌ Pushes
3. **Check:**
   - ✅ Issues
   - ✅ Issue comments
   - ✅ Pull requests
   - ✅ Pull request reviews
   - ✅ Pull request review comments

**Other Settings:**
- Content type: `application/json`
- SSL verification: ✅ Enable SSL verification
- Active: ✅ Checked

#### **C. Save Changes**

Click **"Update webhook"** at the bottom

---

## 2. 🧪 Test the Webhook

### **Method 1: GitHub's Built-in Test**

1. After updating the webhook, scroll down to **"Recent Deliveries"**
2. Find the most recent ping event
3. Click **"Redeliver"** button
4. Check the response:
   - ✅ **Success**: Status code 200, green checkmark
   - ❌ **Failure**: Status code 405 or other error

### **Method 2: Create a Test Issue**

1. Go to: **https://github.com/AryanVBW/WIFIjam/issues/new**
2. Create a test issue:
   ```
   Title: Test GitHub Manager Bot
   Body: @bot hello! This is a test to verify the webhook is working.
   ```
3. Click **"Submit new issue"**
4. Wait 2-3 seconds
5. Check if the bot responds with a comment

### **Method 3: Check Heroku Logs**

Open a terminal and run:

```bash
heroku logs --tail -a github-manager
```

**What to look for:**

✅ **Success indicators:**
```
2025-10-08 ... - src.webhook_handler - INFO - Received issues event
2025-10-08 ... - src.issue_manager - INFO - Processing issue #1 in AryanVBW/WIFIjam
2025-10-08 ... - src.ai_service - INFO - Generating response for issue
2025-10-08 ... - src.issue_manager - INFO - Posted comment on issue #1
```

❌ **Error indicators:**
```
2025-10-08 ... - app - WARNING - Webhook signature verification failed
2025-10-08 ... - app - ERROR - Error processing webhook: ...
```

---

## 3. 📊 Verify Webhook Deliveries in GitHub

### **Check Delivery Status:**

1. Go to: **https://github.com/AryanVBW/WIFIjam/settings/hooks**
2. Click on your webhook
3. Scroll to **"Recent Deliveries"**
4. Click on any delivery to see details:

**Successful Delivery:**
```
✅ Response: 200 OK
Headers:
  X-GitHub-Event: issues
  X-GitHub-Delivery: abc123...
Response Body:
  {"status": "processed"}
```

**Failed Delivery (405 Error):**
```
❌ Response: 405 Method Not Allowed
This means the URL is still wrong (missing /webhook)
```

**Failed Delivery (401 Error):**
```
❌ Response: 401 Unauthorized
{"error": "Invalid signature"}
This means the secret doesn't match
```

---

## 4. 🚀 Bulk Setup for All 218 Repositories

Now that you've verified the webhook works on one repository, let's set it up for all your repositories.

### **Option A: Using Python Script (Recommended)**

#### **Step 1: Set Environment Variables**

```bash
export GITHUB_TOKEN="ghp_YOUR_GITHUB_TOKEN_HERE"
export GITHUB_WEBHOOK_SECRET="YOUR_WEBHOOK_SECRET_HERE"
export WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"
```

#### **Step 2: Run the Setup Script**

```bash
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
[3/218] AryanVBW/repo3... ✅ Added
...

============================================================
📊 Summary:
   ✅ Successfully added: 217
   ⏭️  Already existed: 1
   ❌ Errors: 0
   📦 Total repositories: 218

🎉 Webhook setup complete!
```

### **Option B: Using GitHub CLI (gh)**

If you prefer using GitHub CLI:

#### **Step 1: Install GitHub CLI** (if not already installed)

```bash
# macOS
brew install gh

# Or download from: https://cli.github.com/
```

#### **Step 2: Authenticate**

```bash
gh auth login
```

#### **Step 3: Create Webhook Script**

I'll create a bash script using `gh`:

```bash
#!/bin/bash
# File: scripts/setup_webhooks_gh.sh

WEBHOOK_URL="https://github-manager-d89575ed2bc3.herokuapp.com/webhook"
WEBHOOK_SECRET="YOUR_WEBHOOK_SECRET_HERE"

# Get all public repositories
repos=$(gh repo list --json name,owner --limit 1000 --visibility public | jq -r '.[] | "\(.owner.login)/\(.name)"')

echo "Found $(echo "$repos" | wc -l) repositories"
echo "Setting up webhooks..."

for repo in $repos; do
    echo "Processing $repo..."
    
    # Create webhook
    gh api \
        -X POST \
        "/repos/$repo/hooks" \
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
        2>/dev/null && echo "  ✅ Added" || echo "  ⏭️  Already exists or error"
done

echo "Done!"
```

#### **Step 4: Run the Script**

```bash
chmod +x scripts/setup_webhooks_gh.sh
./scripts/setup_webhooks_gh.sh
```

---

## 5. 📈 Monitoring & Verification

### **Real-Time Log Monitoring**

Keep this running in a terminal:

```bash
heroku logs --tail -a github-manager | grep -E "webhook|issue|pull_request"
```

### **Check Webhook Statistics**

After setup, verify webhooks are working:

```bash
# List webhooks (Python script)
python scripts/setup_webhooks.py list

# Or check a specific repository
gh api /repos/AryanVBW/WIFIjam/hooks
```

### **Test Multiple Repositories**

Create test issues in different repositories to verify:

```bash
# Create test issue using gh CLI
gh issue create \
    --repo AryanVBW/WIFIjam \
    --title "Test Bot Response" \
    --body "Testing the GitHub Manager bot webhook integration"
```

---

## 6. 🐛 Troubleshooting

### **Problem: Still getting 405 errors**

**Solution:**
- Double-check the webhook URL ends with `/webhook`
- Verify you clicked "Update webhook" to save changes

### **Problem: Getting 401 Unauthorized**

**Solution:**
```bash
# Verify secret matches on Heroku
heroku config:get GITHUB_WEBHOOK_SECRET -a github-manager

# Should output: YOUR_WEBHOOK_SECRET_HERE
```

### **Problem: Bot not responding to issues**

**Check:**
1. Webhook events include "Issues" and "Issue comments"
2. Heroku app is running: `heroku ps -a github-manager`
3. Check logs for errors: `heroku logs --tail -a github-manager`
4. Verify AI service is initialized (check health endpoint)

### **Problem: Bulk setup script fails**

**Common causes:**
- Token doesn't have `repo` scope
- Rate limit exceeded (wait 5 minutes)
- Repository is archived or you don't have admin access

---

## 7. ✅ Success Checklist

- [ ] Updated webhook URL to include `/webhook` path
- [ ] Changed events from "push" to issues/PRs
- [ ] Updated webhook secret to match Heroku
- [ ] Tested webhook with ping event (200 OK response)
- [ ] Created test issue and bot responded
- [ ] Ran bulk setup script for all repositories
- [ ] Verified webhooks in multiple repositories
- [ ] Monitored Heroku logs for successful processing

---

## 8. 📞 Next Steps

Once webhooks are set up:

1. **Monitor for 24 hours** to ensure stability
2. **Check webhook delivery success rate** in GitHub settings
3. **Review bot responses** for quality and accuracy
4. **Adjust SYSTEM_PROMPT** if needed to improve responses
5. **Consider creating a GitHub App** for easier distribution

---

## 🎉 Expected Outcome

After completing these steps:

✅ All 218 repositories have working webhooks  
✅ Bot responds to issues and PRs automatically  
✅ No more 405 errors  
✅ Webhook deliveries show 200 OK status  
✅ Heroku logs show successful event processing  
✅ Users receive helpful, personalized responses  

**Your GitHub Manager v2.0 is now fully operational! 🚀**

