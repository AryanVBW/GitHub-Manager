# Quick Start Guide

Get GitHub Manager up and running in 10 minutes!

## 🚀 Prerequisites

- GitHub account with a repository
- Heroku account (free tier works)
- 10 minutes of your time

## ⚡ Quick Setup

### 1. Get Your Credentials (5 minutes)

**GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select: `repo`, `read:org`, `read:user`
4. Copy the token (starts with `ghp_`)

**AI API Key (choose one):**

**Option A - Gemini (Free):**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**Option B - OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

**Webhook Secret:**
```bash
# Generate a random secret
openssl rand -hex 32
```

### 2. Deploy to Heroku (3 minutes)

```bash
# Clone this repository
git clone https://github.com/yourusername/github-manager.git
cd github-manager

# Login to Heroku
heroku login

# Create app
heroku create my-github-bot

# Set environment variables
heroku config:set GITHUB_TOKEN="ghp_your_token_here"
heroku config:set GITHUB_REPO="owner/repo-name"
heroku config:set GITHUB_WEBHOOK_SECRET="your_secret_here"
heroku config:set AI_PROVIDER="gemini"
heroku config:set GEMINI_API_KEY="your_gemini_key_here"

# Deploy
git push heroku main

# Verify
heroku open
```

### 3. Configure GitHub Webhook (2 minutes)

1. Go to your GitHub repo → Settings → Webhooks → Add webhook
2. **Payload URL**: `https://your-app-name.herokuapp.com/webhook`
3. **Content type**: `application/json`
4. **Secret**: (paste your webhook secret)
5. **Events**: Select "Issue comments", "Issues", "Pull requests"
6. Click "Add webhook"

### 4. Test It! (1 minute)

1. Create an issue in your repository
2. Comment: "assign me"
3. Watch the bot assign it to you! 🎉

## ✅ Verification

Check that everything works:

```bash
# Check app status
curl https://your-app-name.herokuapp.com/health

# View logs
heroku logs --tail
```

You should see:
- ✅ Status: "healthy"
- ✅ GitHub: "connected"
- ✅ No errors in logs

## 🎯 What's Next?

Your bot is now:
- ✅ Monitoring your repository
- ✅ Responding to issue comments
- ✅ Handling assignment requests
- ✅ Answering questions with AI

### Optional Enhancements

**Add Email Notifications:**
```bash
heroku config:set RESEND_API_KEY="re_your_key"
heroku config:set OWNER_EMAIL="you@example.com"
```

**Adjust Log Level:**
```bash
heroku config:set LOG_LEVEL="DEBUG"
```

## 📖 Learn More

- **Full Setup Guide**: [SETUP.md](SETUP.md)
- **User Guide**: [README.md](README.md)
- **Technical Details**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Deployment Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## 🆘 Troubleshooting

**Bot not responding?**
```bash
# Check logs
heroku logs --tail

# Verify config
heroku config

# Restart app
heroku restart
```

**Webhook failing?**
- Check webhook secret matches
- Verify payload URL is correct
- Check GitHub webhook deliveries page

**AI not working?**
- Verify API key is correct
- Check provider quota/billing
- Review logs for errors

## 💡 Tips

1. **Test locally first**: Use `.env` file and run `python app.py`
2. **Monitor logs**: Keep `heroku logs --tail` running
3. **Start simple**: Test with one issue before going live
4. **Read the docs**: Check SETUP.md for detailed instructions

## 🎉 Success!

If you can:
- ✅ Comment "assign me" and get assigned
- ✅ Ask a question and get an AI response
- ✅ See activity in Heroku logs

Then congratulations! Your GitHub Manager is working perfectly! 🚀

---

**Need help?** Check [SETUP.md](SETUP.md) for detailed troubleshooting.

