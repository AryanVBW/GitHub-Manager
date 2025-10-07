# GitHub Manager 🤖

A production-grade, AI-powered GitHub bot that automatically manages issues and pull requests in your repository. Built with Python and designed to run continuously on Heroku/AWS or any VPS.

## 🌟 Features

### Intelligent Issue Assignment
- **Automatic Assignment**: When multiple users request to work on an issue, the bot intelligently assigns it based on:
  - User engagement (number of comments on the issue)
  - First-come-first-served (when engagement is equal)
- **Professional Communication**: Sends confirmation to the assigned user and polite decline messages to others
- **Smart Detection**: Recognizes various assignment request phrases like "assign me", "I want to work on this", etc.

### AI-Powered Responses
- **Issue Comments**: Responds to all issue comments with helpful, context-aware answers
- **Pull Request Comments**: Answers questions on pull requests with relevant information
- **Multiple AI Providers**: Supports both Google Gemini and OpenAI GPT
- **Context-Aware**: Considers issue/PR details, labels, and description when generating responses

### Email Notifications (Optional)
- **Issue Assignments**: Notifies repository owner when issues are assigned
- **PR Activity**: Alerts on new pull requests, questions, and merges
- **Error Alerts**: Sends notifications when errors occur
- **Fully Optional**: Application works perfectly without email configuration

### Production-Ready
- **Rate Limit Handling**: Automatically manages GitHub API rate limits
- **Error Recovery**: Comprehensive error handling with retry logic
- **Logging**: Detailed colored console logging for monitoring
- **Webhook Security**: Verifies GitHub webhook signatures
- **Graceful Degradation**: Continues working even if optional features fail

## 🎯 How It Works

### For Issue Assignment

1. **User Comments**: Multiple users comment on an issue requesting assignment
   ```
   "Can I work on this?"
   "Assign me please"
   "I want to work on this issue"
   ```

2. **Bot Analyzes**: The bot analyzes:
   - How many times each user has commented on the issue
   - Who requested assignment first

3. **Bot Assigns**: The bot assigns the issue to the most engaged user

4. **Bot Responds**: 
   - Sends a confirmation message to the assigned user
   - Sends polite decline messages to other users

### For General Comments

1. **User Comments**: A user asks a question or makes a comment on an issue or PR

2. **Bot Responds**: The bot generates a helpful, professional response using AI

3. **Context-Aware**: The response considers:
   - Issue/PR title and description
   - Labels and current state
   - Previous conversation context

## 💬 Interacting with the Bot

### Requesting Issue Assignment

Use any of these phrases in a comment:
- "assign me"
- "I want to work on this"
- "Can I work on this?"
- "I would like to work on this"
- "Please assign me"
- "I can work on this"
- "Let me work on this"

### Asking Questions

Simply comment on any issue or pull request with your question. The bot will:
- Analyze your question
- Consider the context
- Provide a helpful, professional response

### Expected Behavior

**On Issues:**
- Bot responds to all comments (except its own)
- Bot handles assignment requests intelligently
- Bot provides helpful answers to questions

**On Pull Requests:**
- Bot welcomes new PRs
- Bot answers questions about the PR
- Bot congratulates on merges
- Bot notifies owner of important activity

## 🤝 Bot Communication Style

The bot is designed to be:
- **Humble**: Never boastful or arrogant
- **Professional**: Clear and respectful communication
- **Helpful**: Provides actionable information
- **Friendly**: Warm and supportive tone
- **Concise**: Brief and to-the-point responses

## 📊 Repository Support

The bot works with various repository structures:
- Main repositories
- Repositories with dev branches
- Repositories with feature branches
- Multiple branch workflows
- Fork-based workflows

## 🔒 Security & Permissions

The bot requires minimal GitHub permissions:
- Read access to issues and pull requests
- Write access to issue comments
- Write access to issue assignments

**Important**: The bot cannot and will not:
- Delete repositories
- Force push to branches
- Delete branches
- Modify repository settings
- Access private data outside the configured repository

## 📈 Monitoring

The bot provides several endpoints for monitoring:

- **`/`**: Basic status check
- **`/health`**: Detailed health information
- **`/webhook`**: GitHub webhook endpoint (POST only)

## 🆘 Support

If the bot isn't responding as expected:

1. Check that the issue/PR is in the configured repository
2. Ensure your comment doesn't come from a bot account
3. Verify the bot has proper permissions
4. Check the Heroku/AWS or any VPS logs for any errors

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API wrapper
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Google Gemini](https://ai.google.dev/) / [OpenAI](https://openai.com/) - AI providers
- [Resend](https://resend.com/) - Email service

---

For setup and deployment instructions, see [SETUP.md](SETUP.md).

For technical documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

# GitHub-Manager
