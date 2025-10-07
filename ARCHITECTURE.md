# Architecture Documentation

This document provides technical details about the GitHub Manager application architecture, code organization, and implementation details.

## 🆕 Version 2.0 Features

This version introduces major architectural improvements:

1. **Multi-Repository Support**: Manages all public repositories automatically
2. **User Style Analysis**: Analyzes each user's writing style for personalized responses
3. **Personalized AI Responses**: Generates unique responses tailored to each user
4. **Customizable System Prompts**: Allows personality customization via environment variables
5. **AI Model Selection**: Supports multiple AI models with configurable selection
6. **Natural Identity**: Replies as the authenticated user, not as a bot

## 📁 Directory Structure

```
github-manager/
├── app.py                      # Main Flask application entry point
├── Procfile                    # Heroku process configuration
├── runtime.txt                 # Python version specification
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
│
├── src/                       # Source code directory
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration management
│   ├── logger.py             # Logging configuration
│   ├── github_client.py      # GitHub API client
│   ├── ai_service.py         # AI service abstraction
│   ├── email_service.py      # Email notification service
│   ├── issue_manager.py      # Issue management logic
│   ├── pr_manager.py         # Pull request management logic
│   └── webhook_handler.py    # Webhook event processing
│
├── README.md                  # User documentation
├── SETUP.md                   # Setup and deployment guide
└── ARCHITECTURE.md            # This file
```

## 🏗️ System Architecture

### High-Level Overview (Version 2.0)

```
Multiple GitHub Repositories
       ↓ (webhooks with repo info)
   Heroku/AWS/VPS App
       ↓
   Flask Server
       ↓
Webhook Handler (extracts repo from payload)
       ↓
┌──────┴──────┐
│             │
Issue Manager  PR Manager
│             │
│  ┌──────────┴──────────┐
│  │                     │
│  User Style Analyzer   Personalized Response Generator
│  │                     │
│  └──────────┬──────────┘
│             │
└──────┬──────┘
       ↓
┌──────┴──────┬──────────┬──────────┐
│             │          │          │
GitHub API    AI API     Email API  User Cache
(multi-repo)  (custom    (optional) (style data)
              prompts)
```

### Component Interaction Flow (Version 2.0)

1. **GitHub** sends webhook events from any repository to the Flask server
2. **Webhook Handler** verifies signature, extracts repository info, and routes events
3. **GitHub Client** retrieves the specific repository from cache or API
4. **Issue/PR Managers** process events and make decisions
5. **User Analyzer** fetches user's comment history and analyzes writing style
6. **AI Service** generates personalized responses using:
   - Custom system prompt (from environment)
   - User's writing style analysis
   - Full context (issue/PR details)
   - Selected AI model (Gemini or OpenAI)
7. **GitHub Client** posts response as the authenticated user
8. **Email Service** sends notifications (optional)

### Multi-Repository Architecture

```
GitHub Client
    ↓
┌───┴────────────────────────────┐
│  Authenticated User            │
│  ├── Repository Cache          │
│  │   ├── repo1 (cached)        │
│  │   ├── repo2 (cached)        │
│  │   └── repo3 (cached)        │
│  └── Public Repos Discovery    │
└────────────────────────────────┘
         ↓
Webhook Event (contains repo info)
         ↓
Repository Lookup (from cache or API)
         ↓
Process Event for Specific Repository
```

### User Style Analysis Architecture

```
User Comments on Issue/PR
         ↓
Fetch User's Comment History (last 10 comments)
         ↓
┌────────┴────────────────────────┐
│  User Style Analyzer            │
│  ├── Calculate avg length       │
│  ├── Detect tone (casual/formal)│
│  ├── Measure formality level    │
│  ├── Count emoji usage          │
│  └── Analyze sentence structure │
└────────┬────────────────────────┘
         ↓
User Style Profile
         ↓
Build Personalized Context
         ↓
AI Service (with custom system prompt)
         ↓
Personalized Response (matches user's style)
```

## 🔧 Core Components

### 1. Flask Application (`app.py`)

**Purpose**: Main application entry point and HTTP server

**Responsibilities**:
- Initialize all services on startup
- Provide health check endpoints
- Handle webhook POST requests
- Manage error responses
- Coordinate service lifecycle

**Key Endpoints**:
- `GET /` - Basic status check
- `GET /health` - Detailed health information
- `POST /webhook` - GitHub webhook receiver

**Error Handling**:
- Validates configuration on startup
- Catches and logs all exceptions
- Sends error notifications via email
- Returns appropriate HTTP status codes

### 2. Configuration Management (`src/config.py`)

**Purpose**: Centralized configuration and validation

**Features** (Version 2.0):
- Loads environment variables
- Validates required configuration
- Provides helper methods for config access
- Checks optional feature availability
- **NEW**: Validates AI model selection
- **NEW**: Supports custom system prompts
- **NEW**: Removed single repository requirement

**Configuration Categories**:
- GitHub settings (token, webhook secret) - **NO LONGER REQUIRES REPO**
- AI provider settings (Gemini or OpenAI)
- **NEW**: AI model selection (GEMINI_MODEL, OPENAI_MODEL)
- **NEW**: Custom system prompt (SYSTEM_PROMPT)
- Email settings (optional)
- Application settings (logging, port)

**Validation**:
- Ensures all required variables are set
- Validates AI provider selection
- Checks AI API key availability
- **NEW**: Validates AI model names against supported models
- **REMOVED**: Repository format validation (no longer needed)

**Supported AI Models**:
- **Gemini**: `gemini-pro`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **OpenAI**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-4o-mini`

### 3. GitHub Client (`src/github_client.py`)

**Purpose**: GitHub API interaction with rate limiting and multi-repository support

**Key Features** (Version 2.0):
- PyGithub wrapper with enhanced error handling
- Automatic rate limit checking and waiting
- **NEW**: Multi-repository management
- **NEW**: Repository caching for performance
- **NEW**: Authenticated user management
- **NEW**: User comment history retrieval
- Issue and PR retrieval (now accepts repository parameter)
- Comment management
- Issue assignment

**Multi-Repository Support**:
- Authenticates as user (not repository-specific)
- Discovers all public repositories on startup
- Caches repository objects to avoid repeated API calls
- Accepts repository parameter for all operations
- Supports organization repositories

**Repository Caching**:
```python
_repositories_cache: Dict[str, Repository] = {}
# Caches repositories by full_name (owner/repo)
# Reduces API calls and improves performance
```

**User Comment History**:
- Fetches user's recent comments from a repository
- Used for writing style analysis
- Configurable limit (default: 10 comments)
- Searches recent issues for user activity

**Rate Limiting Strategy**:
- Checks rate limit before each API call
- Automatically waits if limit is near exhaustion
- Logs rate limit status for monitoring
- Uses exponential backoff for retries

**Error Handling**:
- Catches GitHub API exceptions
- Logs detailed error information
- Returns None for failed operations
- Continues operation despite individual failures

### 4. AI Service (`src/ai_service.py`)

**Purpose**: AI provider abstraction, user style analysis, and personalized response generation

**Architecture** (Version 2.0):
```
AIService (main interface)
    ↓
┌───┴────────────────┐
│                    │
UserAnalyzer         AIProvider (abstract base)
(style analysis)          ↓
                    ┌─────┴─────┐
                    │           │
                  Gemini      OpenAI
                  (with       (with
                   model)      model)
```

**NEW: UserAnalyzer Class**:
- **Purpose**: Analyzes user writing style for personalization
- **Methods**:
  - `analyze_writing_style(user_comments)`: Analyzes comment patterns
  - `build_personalized_context(user_style, context)`: Creates tailored context

**Writing Style Analysis**:
```python
{
    "avg_length": 150,  # Average comment length
    "tone": "casual",   # casual, formal, or technical
    "formality": 0.3,   # 0.0 (very casual) to 1.0 (very formal)
    "uses_emojis": True,  # Whether user uses emojis
    "avg_sentences": 3    # Average sentences per comment
}
```

**Style Detection Heuristics**:
- **Tone**: Detected by keyword patterns
  - Casual: "hey", "yeah", "cool", "awesome"
  - Formal: "regarding", "therefore", "furthermore"
  - Technical: "function", "class", "variable", "API"
- **Formality**: Calculated from:
  - Contractions usage (don't, can't, etc.)
  - Greeting patterns
  - Sentence structure
- **Emoji Usage**: Regex pattern matching
- **Length**: Average characters per comment

**Provider Selection**:
- Configured via `AI_PROVIDER` environment variable
- Supports "gemini" or "openai"
- **NEW**: Model selection via `GEMINI_MODEL` or `OPENAI_MODEL`
- Initialized once at startup
- Fails fast if provider unavailable

**Response Generation** (Version 2.0):
- **NEW**: Accepts optional user_comments for personalization
- Analyzes user's writing style if comments provided
- Builds personalized context based on user style
- Uses custom system prompt from environment
- Includes system instructions for tone
- Implements retry logic with exponential backoff
- Returns None on failure (graceful degradation)

**Prompt Engineering** (Version 2.0):
- **NEW**: Customizable system prompt via `SYSTEM_PROMPT` environment variable
- Default emphasizes humility and professionalism
- **NEW**: Personalized context includes user style preferences
- Context includes issue/PR details
- Responses kept concise and actionable
- Tone is friendly and supportive
- **NEW**: Adapts to each user's communication style

**Personalization Example**:
```python
# User A (casual, uses emojis)
user_a_style = {"tone": "casual", "uses_emojis": True}
response_a = "Hey! That's a great question! 🎉 Here's what you can do..."

# User B (formal, technical)
user_b_style = {"tone": "formal", "formality": 0.8}
response_b = "Thank you for your inquiry. Regarding your question, the recommended approach is..."
```

### 5. Email Service (`src/email_service.py`)

**Purpose**: Optional email notifications via Resend

**Design Philosophy**:
- Fully optional - app works without it
- Fails gracefully if not configured
- Logs warnings instead of errors
- Never blocks main workflow

**Notification Types**:
- Issue assignments
- PR activity (new, questions, merges)
- Application errors

**Email Templates**:
- HTML and plain text versions
- Professional styling
- Clickable links to GitHub
- Timestamp information

### 6. Issue Manager (`src/issue_manager.py`)

**Purpose**: Intelligent issue assignment and response

**Assignment Algorithm**:
```python
1. Detect assignment requests in comments
2. Collect all users who requested assignment
3. For each user:
   - Count total comments on the issue
   - Record time of assignment request
4. Sort by:
   - Comment count (descending)
   - Request time (ascending)
5. Select top user
6. Assign issue
7. Send confirmation to selected user
8. Send polite declines to others
```

**Assignment Request Detection**:
- Uses regex patterns for flexibility
- Case-insensitive matching
- Supports multiple phrase variations
- Examples: "assign me", "I want to work on this", etc.

**Response Generation**:
- Generates context from issue details
- Calls AI service for responses
- Adds responses as comments
- Handles failures gracefully

### 7. PR Manager (`src/pr_manager.py`)

**Purpose**: Pull request monitoring and responses

**Event Handling**:
- PR opened: Welcome message
- PR comment: AI-generated response
- Review requested: Email notification
- PR merged: Congratulations message

**Question Detection**:
- Checks for question marks
- Identifies question words
- Triggers email notifications for questions

**Context Generation**:
- Includes PR title and description
- Adds branch information
- Includes file change statistics
- Adds mergeable state

### 8. Webhook Handler (`src/webhook_handler.py`)

**Purpose**: Process and route GitHub webhook events

**Security**:
- Verifies HMAC-SHA256 signature
- Uses constant-time comparison
- Rejects invalid signatures
- Logs security events

**Event Routing**:
```
Webhook Event
    ↓
Verify Signature
    ↓
Route by Event Type
    ↓
┌────┴────┬────────┐
│         │        │
Issues  Comments  PRs
```

**Supported Events**:
- `issue_comment` - Comments on issues/PRs
- `issues` - Issue events (logged only)
- `pull_request` - PR events (opened, merged, etc.)

**Event Processing**:
- Extracts relevant data from payload
- Retrieves full objects from GitHub API
- Delegates to appropriate manager
- Returns success/failure status

## 🔄 Data Flow Examples

### Issue Assignment Flow

```
1. User comments "assign me" on issue
   ↓
2. GitHub sends issue_comment webhook
   ↓
3. Webhook handler verifies signature
   ↓
4. Handler routes to issue manager
   ↓
5. Issue manager detects assignment request
   ↓
6. Manager analyzes all candidates
   ↓
7. Manager selects best candidate
   ↓
8. GitHub client assigns issue
   ↓
9. Manager generates confirmation message
   ↓
10. GitHub client posts comment
    ↓
11. Manager generates decline messages
    ↓
12. GitHub client posts decline comments
    ↓
13. Email service sends notification
```

### AI Response Flow

```
1. User comments question on issue
   ↓
2. GitHub sends issue_comment webhook
   ↓
3. Webhook handler routes to issue manager
   ↓
4. Issue manager generates context
   ↓
5. AI service builds prompt
   ↓
6. AI provider generates response
   ↓
7. AI service returns response
   ↓
8. Issue manager receives response
   ↓
9. GitHub client posts comment
```

## 🛡️ Error Handling Strategy

### Layered Error Handling

1. **Component Level**: Each component catches its own exceptions
2. **Service Level**: Services handle provider-specific errors
3. **Application Level**: Flask handles HTTP-level errors
4. **Notification Level**: Critical errors trigger email alerts

### Graceful Degradation

- **Email Disabled**: App continues without notifications
- **AI Failure**: Logs error, doesn't crash
- **GitHub API Error**: Retries with backoff
- **Rate Limit**: Waits and retries automatically

### Retry Logic

```python
for attempt in range(max_retries):
    try:
        result = operation()
        return result
    except Exception as e:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
        else:
            log_error(e)
            return None
```

## 📊 Logging Strategy

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Error messages (operation failures)
- **CRITICAL**: Critical errors (system failures)

### Colored Output

- DEBUG: Cyan
- INFO: Green
- WARNING: Yellow
- ERROR: Red
- CRITICAL: Red on white background

### Log Content

- Timestamp
- Logger name (module)
- Log level
- Message

### What Gets Logged

- Service initialization
- Configuration validation
- API calls and responses
- Event processing
- Errors and exceptions
- Rate limit status
- Assignment decisions

## 🔐 Security Considerations

### Webhook Security

- HMAC-SHA256 signature verification
- Constant-time comparison to prevent timing attacks
- Rejects unsigned requests
- Logs security events

### Token Security

- Tokens stored in environment variables
- Never logged or exposed
- Minimal required permissions
- Supports token rotation

### API Security

- Rate limit handling prevents abuse
- Input validation on all data
- No execution of user-provided code
- Sanitized error messages

## 🚀 Deployment Architecture

### Heroku Configuration

```
Heroku App
├── Web Dyno (gunicorn)
│   ├── Workers: 1
│   ├── Timeout: 120s
│   └── Port: Dynamic ($PORT)
│
├── Environment Variables
│   ├── GitHub credentials
│   ├── AI API keys
│   └── Optional email config
│
└── Logging
    └── stdout/stderr to Heroku logs
```

### Process Management

- **Gunicorn**: Production WSGI server
- **Workers**: 1 (sufficient for webhook processing)
- **Timeout**: 120 seconds (handles long AI requests)
- **Binding**: 0.0.0.0:$PORT (Heroku dynamic port)

### Scaling Considerations

- **Vertical**: Increase dyno size for more memory/CPU
- **Horizontal**: Add more dynos (requires session management)
- **Rate Limits**: GitHub API limits apply per token
- **AI Limits**: Provider-specific rate limits

## 🧪 Testing Strategy

### Manual Testing

1. Create test issue
2. Comment with assignment request
3. Verify assignment and responses
4. Check email notifications
5. Review logs

### Monitoring

- Heroku logs for errors
- GitHub webhook delivery status
- Email delivery status (Resend dashboard)
- Rate limit usage

### Health Checks

- `/health` endpoint for monitoring
- Checks GitHub connection
- Reports service status
- Returns JSON with details

## 📈 Performance Considerations

### API Efficiency

- Batch operations where possible
- Cache repository information
- Minimize API calls
- Use pagination for large datasets

### Response Time

- Webhook responses within seconds
- AI responses may take 2-5 seconds
- Rate limit waits can add delays
- Timeout set to 120 seconds

### Resource Usage

- Memory: ~100-200 MB
- CPU: Low (event-driven)
- Network: Moderate (API calls)
- Storage: None (stateless)

## 🔮 Future Enhancements

Potential improvements:

1. **Database**: Store assignment history
2. **Analytics**: Track bot performance
3. **Custom Rules**: Configurable assignment logic
4. **Multi-Repo**: Support multiple repositories
5. **Slash Commands**: GitHub slash command support
6. **Testing**: Automated test suite
7. **Metrics**: Prometheus/Grafana integration
8. **Caching**: Redis for rate limit coordination

---

This architecture is designed for reliability, maintainability, and extensibility while keeping the codebase simple and understandable.

