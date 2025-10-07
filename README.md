# GitHub Manager 🤖

A production-grade, AI-powered GitHub assistant that automatically manages issues and pull requests across **all your public repositories**. Built with Python and designed to run continuously on Heroku/AWS or any VPS.

## ✨ What Makes This Special

### 🎭 Replies as YOU, Not as a Bot
Unlike traditional GitHub bots that create a separate bot account, this manager **replies as the authenticated user** (you). Your responses appear natural and personal, without any "I'm a bot" signatures.

### 🧠 Personalized Responses for Each User
The bot analyzes each user's writing style and generates **unique, tailored responses** based on:
- **Tone**: Formal vs casual communication style
- **Length**: Brief vs detailed response preferences
- **Emoji Usage**: Matches user's emoji patterns
- **Technical Level**: Adapts to user's expertise

### 🌐 Multi-Repository Management
Automatically discovers and manages **ALL your public repositories** - no need to configure each one individually. One deployment, unlimited repositories.

### 🎨 Customizable Personality
Define your bot's personality with a custom system prompt. Be formal, casual, technical, friendly, or anything in between.

## 🌟 Core Features

### Intelligent Issue Assignment
- **Engagement-Based Assignment**: When multiple users request to work on an issue, assigns based on:
  - User engagement (number of comments on the issue)
  - First-come-first-served (when engagement is equal)
- **Professional Communication**: Sends confirmation to the assigned user and polite decline messages to others
- **Smart Detection**: Recognizes various assignment request phrases like "assign me", "I want to work on this", etc.

### AI-Powered Personalized Responses
- **User Style Analysis**: Analyzes each user's comment history to understand their communication style
- **Personalized Replies**: Generates responses that match each user's tone, length, and formality
- **Context-Aware**: Considers issue/PR details, labels, description, and conversation history
- **Multiple AI Providers**: Supports both Google Gemini (free) and OpenAI GPT
- **Model Selection**: Choose from multiple models (GPT-4, GPT-3.5, Gemini Pro, etc.)

### Multi-Repository Support
- **Automatic Discovery**: Finds and manages all your public repositories automatically
- **No Configuration Needed**: No need to specify repository names
- **Organization Support**: Works with personal and organization repositories
- **Scalable**: Handles unlimited repositories with a single deployment

### Customizable System Prompt
- **Define Personality**: Customize how the bot communicates
- **Flexible Tone**: Be formal, casual, technical, friendly, or educational
- **Easy Configuration**: Set via environment variable
- **Examples Provided**: Multiple prompt templates included

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
- **Security Focused**: Minimal GitHub permissions, no risk of repository deletion

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

4. **Bot Responds** (as you, not as a bot):
   - Sends a confirmation message to the assigned user
   - Sends polite decline messages to other users

### For Personalized AI Responses

1. **User Comments**: A user asks a question or makes a comment on an issue or PR

2. **Bot Analyzes User Style**:
   - Fetches user's recent comment history (last 10 comments)
   - Analyzes writing style:
     - Average comment length
     - Tone (casual, formal, technical)
     - Formality level
     - Emoji usage patterns
     - Sentence structure

3. **Bot Generates Personalized Response**:
   - Uses AI (Gemini or OpenAI) with custom system prompt
   - Tailors response to match user's communication style
   - Considers full context:
     - Issue/PR title and description
     - Labels and current state
     - Previous conversation context
     - User's writing preferences

4. **Bot Responds** (as you, not as a bot):
   - Posts response that matches user's style
   - Each user gets a unique, personalized response
   - No "I'm a bot" signatures or identifiers

### Multi-Repository Management

1. **Automatic Discovery**: On startup, the bot:
   - Authenticates with your GitHub token
   - Discovers all your public repositories
   - Caches repository information

2. **Webhook Handling**: When a webhook is received:
   - Extracts repository information from payload
   - Retrieves the specific repository
   - Processes the event (issue comment, PR, etc.)

3. **Works Everywhere**:
   - No need to configure individual repositories
   - Add webhooks to any repository you want managed
   - Bot automatically handles events from all repositories

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
- Analyze your writing style from your comment history
- Generate a response that matches your communication preferences
- Consider the full context of the issue/PR
- Provide a helpful, personalized response

### Expected Behavior

**On Issues:**
- Bot responds to all comments (except its own)
- Bot handles assignment requests intelligently
- Bot provides personalized answers to each user
- Responses appear as comments from the authenticated user (you)

**On Pull Requests:**
- Bot welcomes new PRs (as you, not as a bot)
- Bot answers questions about the PR with personalized responses
- Bot congratulates on merges
- Bot notifies owner of important activity (if email configured)

**Across All Repositories:**
- Bot automatically manages all your public repositories
- No need to configure each repository individually
- Consistent behavior across all repos

## 🎨 Customization Examples

### System Prompt Examples

**Default (Humble and Professional):**
```
You are a helpful, humble, and professional GitHub assistant. Your responses should be concise, respectful, and actionable. Always maintain a friendly and supportive tone. Keep responses brief and to the point.
```

**Technical and Detailed:**
```
You are a technical GitHub assistant. Provide detailed, precise responses with code examples when relevant. Use formal language and technical terminology. Focus on accuracy and completeness.
```

**Casual and Friendly:**
```
You are a friendly GitHub helper. Keep things casual and approachable. Use simple language and be encouraging. Feel free to use emojis when appropriate. Make contributors feel welcome!
```

**Brief and Direct:**
```
You are a concise GitHub assistant. Give brief, direct answers. No fluff. Get straight to the point. Use bullet points when possible.
```

### AI Model Selection

**For High Volume (Free):**
- Use `gemini-pro` or `gemini-1.5-flash`
- Fast responses, good quality
- No cost

**For Best Quality:**
- Use `gpt-4` or `gpt-4-turbo`
- Excellent reasoning and context understanding
- Higher cost

**For Balance:**
- Use `gpt-3.5-turbo` or `gpt-4o-mini`
- Good quality, reasonable cost
- Fast responses

## 🤝 Communication Style

The bot is designed to be:
- **Humble**: Never boastful or arrogant
- **Personalized**: Adapts to each user's communication style
- **Natural**: Replies as you, not as a separate bot account
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
