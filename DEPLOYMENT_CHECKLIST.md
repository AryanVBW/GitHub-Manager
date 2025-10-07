# Deployment Checklist

Use this checklist to ensure a smooth deployment of GitHub Manager to Heroku.

## Pre-Deployment

### 1. GitHub Setup
- [ ] Created GitHub personal access token
- [ ] Token has correct permissions (see SETUP.md)
- [ ] Token saved securely
- [ ] Repository name noted (format: owner/repo)
- [ ] Generated webhook secret (32+ characters)

### 2. AI Provider Setup
- [ ] Chose AI provider (Gemini or OpenAI)
- [ ] Created API key for chosen provider
- [ ] API key saved securely
- [ ] Verified API key works (optional: test in provider's playground)

### 3. Email Setup (Optional)
- [ ] Decided if email notifications are needed
- [ ] If yes: Created Resend account
- [ ] If yes: Generated Resend API key
- [ ] If yes: Verified owner email address

### 4. Local Testing (Optional but Recommended)
- [ ] Cloned repository locally
- [ ] Created `.env` file from `.env.example`
- [ ] Filled in all environment variables
- [ ] Ran `python validate_config.py` successfully
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Tested locally: `python app.py`
- [ ] Verified health endpoint: `curl http://localhost:5000/health`

## Heroku Deployment

### 5. Heroku Account Setup
- [ ] Created Heroku account
- [ ] Installed Heroku CLI
- [ ] Logged in: `heroku login`

### 6. Create Heroku App
- [ ] Created new Heroku app: `heroku create app-name`
- [ ] Noted app URL: `https://app-name.herokuapp.com`

### 7. Configure Environment Variables
- [ ] Set GITHUB_TOKEN: `heroku config:set GITHUB_TOKEN="..."`
- [ ] Set GITHUB_REPO: `heroku config:set GITHUB_REPO="owner/repo"`
- [ ] Set GITHUB_WEBHOOK_SECRET: `heroku config:set GITHUB_WEBHOOK_SECRET="..."`
- [ ] Set AI_PROVIDER: `heroku config:set AI_PROVIDER="gemini"` or `"openai"`
- [ ] Set AI API key (GEMINI_API_KEY or OPENAI_API_KEY)
- [ ] Set email config (if using): RESEND_API_KEY and OWNER_EMAIL
- [ ] Verified all config: `heroku config`

### 8. Deploy Application
- [ ] Added Heroku remote: `heroku git:remote -a app-name`
- [ ] Pushed code: `git push heroku main`
- [ ] Checked logs: `heroku logs --tail`
- [ ] Verified no errors in logs
- [ ] Checked app status: `heroku ps`

### 9. Verify Deployment
- [ ] Opened app: `heroku open`
- [ ] Checked status endpoint: `curl https://app-name.herokuapp.com/`
- [ ] Checked health endpoint: `curl https://app-name.herokuapp.com/health`
- [ ] Verified response shows "status": "healthy"

## GitHub Webhook Setup

### 10. Configure Webhook
- [ ] Went to GitHub repo → Settings → Webhooks
- [ ] Clicked "Add webhook"
- [ ] Set Payload URL: `https://app-name.herokuapp.com/webhook`
- [ ] Set Content type: `application/json`
- [ ] Set Secret: (same as GITHUB_WEBHOOK_SECRET)
- [ ] Selected events:
  - [ ] Issue comments
  - [ ] Issues
  - [ ] Pull requests
  - [ ] Pull request reviews
  - [ ] Pull request review comments
- [ ] Ensured "Active" is checked
- [ ] Clicked "Add webhook"
- [ ] Verified green checkmark appears (successful ping)

## Testing

### 11. Test Issue Assignment
- [ ] Created test issue in repository
- [ ] Commented "assign me" on the issue
- [ ] Verified bot assigned the issue
- [ ] Verified bot posted confirmation comment
- [ ] Checked Heroku logs for activity

### 12. Test AI Responses
- [ ] Commented a question on an issue
- [ ] Verified bot responded with helpful answer
- [ ] Checked response quality and tone
- [ ] Verified response is humble and professional

### 13. Test Pull Request Features
- [ ] Created test pull request
- [ ] Verified bot posted welcome message
- [ ] Commented question on PR
- [ ] Verified bot responded
- [ ] Checked Heroku logs for PR activity

### 14. Test Email Notifications (If Configured)
- [ ] Checked email for issue assignment notification
- [ ] Checked email for PR activity notification
- [ ] Verified email formatting and links work
- [ ] Confirmed emails are professional and clear

## Monitoring Setup

### 15. Set Up Monitoring
- [ ] Bookmarked Heroku dashboard: `https://dashboard.heroku.com/apps/app-name`
- [ ] Bookmarked logs: `https://dashboard.heroku.com/apps/app-name/logs`
- [ ] Set up log drain (optional): `heroku logs --tail`
- [ ] Checked GitHub webhook deliveries page
- [ ] Bookmarked Resend dashboard (if using email)

### 16. Documentation
- [ ] Documented app URL for team
- [ ] Shared webhook setup with team (if applicable)
- [ ] Noted where credentials are stored
- [ ] Created runbook for common issues (optional)

## Post-Deployment

### 17. Security
- [ ] Verified tokens are not in git history
- [ ] Confirmed `.env` is in `.gitignore`
- [ ] Reviewed GitHub token permissions
- [ ] Set up token rotation schedule (recommended: every 90 days)

### 18. Maintenance Plan
- [ ] Scheduled regular log reviews
- [ ] Set up alerts for errors (optional)
- [ ] Planned dependency updates schedule
- [ ] Documented escalation process for issues

## Troubleshooting Checklist

If something isn't working:

- [ ] Checked Heroku logs: `heroku logs --tail`
- [ ] Verified all environment variables: `heroku config`
- [ ] Checked GitHub webhook deliveries
- [ ] Verified webhook secret matches
- [ ] Confirmed GitHub token has correct permissions
- [ ] Checked AI provider API key and quota
- [ ] Reviewed Resend dashboard (if using email)
- [ ] Restarted app: `heroku restart`
- [ ] Checked app status: `heroku ps`

## Success Criteria

Your deployment is successful when:

- ✅ Heroku app is running without errors
- ✅ Health endpoint returns "healthy" status
- ✅ GitHub webhook shows successful deliveries
- ✅ Bot responds to issue comments
- ✅ Bot handles assignment requests correctly
- ✅ Bot responds to PR comments
- ✅ Email notifications work (if configured)
- ✅ Logs show normal operation
- ✅ No rate limit issues
- ✅ Response times are acceptable

## Rollback Plan

If deployment fails:

1. Check logs: `heroku logs --tail`
2. Identify the issue
3. If critical, rollback: `heroku rollback`
4. Fix the issue locally
5. Test locally
6. Redeploy: `git push heroku main`

## Support

If you need help:

1. Review [SETUP.md](SETUP.md) for detailed instructions
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. Review Heroku logs for specific errors
4. Check GitHub webhook delivery status
5. Verify all environment variables are correct

---

**Congratulations!** 🎉

Once all items are checked, your GitHub Manager bot is fully deployed and operational!

