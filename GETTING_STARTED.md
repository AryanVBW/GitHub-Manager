# Getting Started with GitHub Manager

Welcome! This guide will help you understand and deploy your GitHub Manager bot.

## 🎯 What is GitHub Manager?

GitHub Manager is an AI-powered bot that:
- **Automatically assigns issues** to the most engaged contributors
- **Responds to questions** on issues and pull requests using AI
- **Sends email notifications** about important repository activity (optional)
- **Runs continuously** on Heroku without manual intervention

## 🤔 Why Use GitHub Manager?

### For Repository Maintainers
- ✅ Reduce manual issue triage
- ✅ Provide instant responses to contributors
- ✅ Fair and transparent issue assignment
- ✅ Stay informed with email notifications
- ✅ Professional, consistent communication

### For Contributors
- ✅ Quick issue assignment process
- ✅ Get answers to questions immediately
- ✅ Clear communication from the bot
- ✅ Fair assignment based on engagement

## 📖 How It Works

### Issue Assignment Flow

```
1. Multiple users comment "assign me" on an issue
   ↓
2. Bot analyzes:
   - How many times each user commented on the issue
   - Who requested assignment first
   ↓
3. Bot assigns to the most engaged user
   ↓
4. Bot sends:
   - Confirmation to assigned user
   - Polite decline to others
   ↓
5. Owner receives email notification (if configured)
```

### AI Response Flow

```
1. User asks a question on issue/PR
   ↓
2. Bot analyzes:
   - Issue/PR title and description
   - Labels and current state
   - Question context
   ↓
3. Bot generates helpful response using AI
   ↓
4. Bot posts response as comment
   ↓
5. Owner receives notification for important questions
```

## 🚀 Quick Start Options

### Option 1: Super Quick (10 minutes)
Follow [QUICKSTART.md](QUICKSTART.md) for the fastest setup.

### Option 2: Detailed Setup (30 minutes)
Follow [SETUP.md](SETUP.md) for comprehensive instructions.

### Option 3: Local Testing First (45 minutes)
1. Clone the repository
2. Copy `.env.example` to `.env`
3. Fill in your credentials
4. Run `python validate_config.py`
5. Run `python test_local.py`
6. Deploy to Heroku

## 📋 What You'll Need

### Required
- ✅ GitHub personal access token
- ✅ GitHub repository to manage
- ✅ Heroku account (free tier works)
- ✅ AI API key (Gemini or OpenAI)

### Optional
- ⭕ Resend account for email notifications
- ⭕ Local Python environment for testing

## 🎓 Understanding the Bot

### Bot Personality
The bot is designed to be:
- **Humble**: Never arrogant or boastful
- **Professional**: Clear and respectful
- **Helpful**: Provides actionable information
- **Friendly**: Warm and supportive
- **Concise**: Brief and to-the-point

### What the Bot Can Do
- ✅ Read issues and pull requests
- ✅ Comment on issues and pull requests
- ✅ Assign issues to users
- ✅ Respond to questions with AI
- ✅ Send email notifications

### What the Bot Cannot Do
- ❌ Delete your repository
- ❌ Force push to branches
- ❌ Delete branches
- ❌ Modify repository settings
- ❌ Access other repositories
- ❌ Execute arbitrary code

## 🔒 Security & Privacy

### Data Handling
- **No persistent storage**: Bot doesn't store any data
- **No data collection**: Bot doesn't collect user information
- **Stateless operation**: Each request is independent
- **Secure credentials**: All secrets in environment variables

### GitHub Permissions
The bot only needs:
- Read access to issues and PRs
- Write access to comments
- Write access to issue assignments

These permissions are carefully selected to prevent:
- Repository deletion
- Branch deletion
- Force pushing
- Settings modification

## 📚 Documentation Guide

### For Users
- **README.md**: Overview and features
- **QUICKSTART.md**: 10-minute setup
- **This file**: Getting started guide

### For Deployment
- **SETUP.md**: Detailed setup instructions
- **DEPLOYMENT_CHECKLIST.md**: Step-by-step checklist
- **.env.example**: Configuration template

### For Developers
- **ARCHITECTURE.md**: Technical documentation
- **CONTRIBUTING.md**: Development guidelines
- **PROJECT_SUMMARY.md**: Project overview

### For Testing
- **validate_config.py**: Configuration validator
- **test_local.py**: Local testing suite

## 🎯 Deployment Paths

### Path 1: Direct to Heroku (Fastest)
```bash
heroku create
heroku config:set GITHUB_TOKEN="..."
heroku config:set GITHUB_REPO="owner/repo"
# ... set other variables
git push heroku main
```

### Path 2: Test Locally First (Recommended)
```bash
cp .env.example .env
# Edit .env with your credentials
python validate_config.py
python test_local.py
# If tests pass, deploy to Heroku
```

### Path 3: Fork and Customize
```bash
# Fork the repository
git clone https://github.com/yourusername/github-manager.git
# Make your customizations
# Test locally
# Deploy to Heroku
```

## 🧪 Testing Your Bot

### Test Issue Assignment
1. Create a test issue
2. Comment "assign me"
3. Verify bot assigns and responds
4. Check Heroku logs

### Test AI Responses
1. Comment a question on any issue
2. Verify bot responds helpfully
3. Check response quality
4. Review logs

### Test Email Notifications (if configured)
1. Check your email inbox
2. Verify notification received
3. Check email formatting
4. Test links work

## 🔍 Monitoring Your Bot

### Heroku Dashboard
- View app status
- Check dyno usage
- Review logs
- Monitor errors

### GitHub Webhooks
- Check webhook deliveries
- Review success/failure rate
- Redeliver failed webhooks
- Monitor response times

### Email Dashboard (if using Resend)
- View sent emails
- Check delivery status
- Review bounce rate
- Monitor quota usage

## 🆘 Common Issues

### Bot Not Responding
**Symptoms**: No comments from bot
**Solutions**:
1. Check Heroku logs: `heroku logs --tail`
2. Verify webhook is configured
3. Check webhook secret matches
4. Verify GitHub token permissions

### AI Responses Failing
**Symptoms**: Bot doesn't respond to questions
**Solutions**:
1. Check AI API key is correct
2. Verify provider quota
3. Review logs for errors
4. Try alternative AI provider

### Email Not Sending
**Symptoms**: No email notifications
**Solutions**:
1. Verify Resend API key
2. Check owner email is set
3. Review Resend dashboard
4. Remember: Email is optional

### Rate Limit Issues
**Symptoms**: "Rate limit exceeded" errors
**Solutions**:
1. Bot automatically handles this
2. Wait for rate limit reset
3. Check logs for timing
4. Consider GitHub plan upgrade

## 💡 Best Practices

### Configuration
- ✅ Use strong webhook secrets (32+ characters)
- ✅ Rotate tokens every 90 days
- ✅ Keep credentials secure
- ✅ Use environment variables
- ✅ Never commit secrets

### Monitoring
- ✅ Check logs regularly
- ✅ Monitor webhook deliveries
- ✅ Review email notifications
- ✅ Track bot performance
- ✅ Set up alerts for errors

### Maintenance
- ✅ Update dependencies monthly
- ✅ Review bot responses
- ✅ Adjust AI prompts if needed
- ✅ Monitor API quotas
- ✅ Keep documentation updated

## 🎓 Learning Resources

### Included in This Project
- Configuration validator
- Local testing suite
- Example environment file
- Comprehensive documentation
- Deployment checklist

### External Resources
- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/python-support)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🚀 Next Steps

1. **Choose your path**: Quick start or detailed setup?
2. **Gather credentials**: GitHub token, AI key, webhook secret
3. **Deploy to Heroku**: Follow chosen guide
4. **Configure webhook**: Connect GitHub to your app
5. **Test thoroughly**: Verify all features work
6. **Monitor and maintain**: Keep an eye on logs

## 🎉 Success Criteria

You'll know your bot is working when:
- ✅ Health endpoint returns "healthy"
- ✅ Bot responds to "assign me" comments
- ✅ Bot answers questions on issues/PRs
- ✅ Webhook deliveries show success
- ✅ Logs show normal operation
- ✅ Email notifications arrive (if configured)

## 📞 Getting Help

If you need assistance:

1. **Check documentation**: README, SETUP, ARCHITECTURE
2. **Review logs**: `heroku logs --tail`
3. **Validate config**: `python validate_config.py`
4. **Test locally**: `python test_local.py`
5. **Check webhook**: GitHub webhook deliveries page
6. **Review checklist**: DEPLOYMENT_CHECKLIST.md

## 🙏 Final Notes

- This bot is designed to be helpful, not intrusive
- It respects your repository and contributors
- It's fully open source and customizable
- It follows GitHub's best practices
- It's built with security in mind

**Ready to get started?** Choose your path and dive in! 🚀

---

**Quick Links:**
- [Quick Start](QUICKSTART.md) - 10 minutes
- [Detailed Setup](SETUP.md) - 30 minutes
- [Architecture](ARCHITECTURE.md) - Technical details
- [Contributing](CONTRIBUTING.md) - Development guide

