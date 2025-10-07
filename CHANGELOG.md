# Changelog

All notable changes to the GitHub Manager project are documented in this file.

## [2.0.0] - 2024-01-XX - Major Feature Release

### 🎉 Major New Features

#### 1. Multi-Repository Support
- **Automatic Discovery**: Bot now automatically discovers and manages ALL your public repositories
- **No Configuration Needed**: Removed `GITHUB_REPO` environment variable requirement
- **Scalable**: Handles unlimited repositories with a single deployment
- **Organization Support**: Works with personal and organization repositories
- **Repository Caching**: Caches repository objects for improved performance

#### 2. Personalized AI Responses
- **User Style Analysis**: Analyzes each user's writing style from their comment history
- **Tailored Responses**: Generates unique responses matching each user's:
  - Tone (casual, formal, technical)
  - Formality level
  - Comment length preferences
  - Emoji usage patterns
- **Context-Aware**: Considers full conversation context and user preferences
- **Separate Responses**: Each user gets a personalized response, not generic replies

#### 3. Natural Bot Identity
- **Replies as You**: Bot responds as the authenticated user, not as a separate bot account
- **No Bot Signatures**: Removed all "I'm a bot" identifiers and signatures
- **Professional Tone**: Maintains humble, professional communication
- **Natural Interaction**: Responses appear as natural human replies

#### 4. Customizable System Prompt
- **Environment Variable**: New `SYSTEM_PROMPT` variable for personality customization
- **Flexible Personality**: Define bot as formal, casual, technical, friendly, or educational
- **Default Provided**: Sensible default if not customized
- **Examples Included**: Multiple prompt templates in documentation

#### 5. AI Model Selection
- **Gemini Models**: Choose from `gemini-pro`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **OpenAI Models**: Choose from `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-4o-mini`
- **Environment Variables**: `GEMINI_MODEL` and `OPENAI_MODEL` for configuration
- **Model Validation**: Validates model names against supported models
- **Cost Optimization**: Choose models based on quality/cost tradeoffs

### 🔧 Technical Improvements

#### GitHub Client (`src/github_client.py`)
- Added `get_repository()` method for retrieving specific repositories
- Added `get_all_public_repositories()` method for discovering all public repos
- Added `get_user_comment_history()` method for fetching user's recent comments
- Added `get_user_info()` method for authenticated user information
- Updated all methods to accept repository parameter instead of using single repo
- Implemented repository caching with `_repositories_cache` dictionary
- Changed initialization from repository-specific to user-specific

#### AI Service (`src/ai_service.py`)
- Added `UserAnalyzer` class with static methods:
  - `analyze_writing_style()`: Analyzes user comment patterns
  - `build_personalized_context()`: Creates personalized context for AI
- Updated `generate_issue_response()` to accept optional `user_comments` parameter
- Updated `generate_pr_response()` to accept optional `user_comments` parameter
- Integrated user style analysis into response generation
- Updated providers to use configurable models from environment variables
- Updated system prompt to use `Config.SYSTEM_PROMPT` instead of hardcoded value

#### Configuration (`src/config.py`)
- **Removed**: `GITHUB_REPO` requirement (breaking change)
- **Added**: `OPENAI_MODEL` with default "gpt-3.5-turbo"
- **Added**: `GEMINI_MODEL` with default "gemini-pro"
- **Added**: `SYSTEM_PROMPT` with customizable default
- **Added**: AI model validation for both providers
- **Added**: Helper methods `get_valid_openai_models()` and `get_valid_gemini_models()`
- **Removed**: `get_repo_owner_and_name()` method (no longer needed)

#### Issue Manager (`src/issue_manager.py`)
- Updated `handle_comment()` to fetch user comment history
- Integrated `UserAnalyzer` for personalized responses
- Updated confirmation and decline messages to remove bot identity
- Removed emoji from automated messages for more professional tone
- Added personalized AI response generation per user

#### PR Manager (`src/pr_manager.py`)
- Updated `handle_comment()` to fetch user comment history
- Integrated `UserAnalyzer` for personalized PR responses
- Updated welcome messages to remove bot identity
- Updated congratulations messages to be more natural
- Added personalized AI response generation per user

#### Webhook Handler (`src/webhook_handler.py`)
- Updated `handle_issue_comment()` to extract repository from payload
- Updated `handle_pull_request()` to extract repository from payload
- Added repository retrieval using `github.get_repository()`
- Updated all event handlers to work with any repository

#### Main Application (`app.py`)
- Updated initialization to authenticate as user instead of repository
- Updated health check to show authenticated user and repository count
- Updated status endpoint to show multi-repo features
- Added version bump to 2.0.0
- Added feature flags to health check response

### 📚 Documentation Updates

#### SETUP.md
- **Enhanced Token Documentation**: Comprehensive guide with:
  - Clear instructions to use Classic Personal Access Token (not Fine-grained)
  - Detailed permission requirements with explanations
  - Security warnings about permissions to avoid
  - Permission scope table with risk levels
  - Token rotation and monitoring guidelines
  - Quick checklist for verification
- **Updated Environment Variables**: Added new variables:
  - `GEMINI_MODEL` and `OPENAI_MODEL` with options
  - `SYSTEM_PROMPT` with customization examples
  - Removed `GITHUB_REPO` requirement
- **Added Model Selection Guide**: Tables comparing:
  - Gemini models (speed, quality, cost)
  - OpenAI models (speed, quality, cost)
- **Added System Prompt Examples**: Multiple personality templates
- **Updated Webhook Configuration**: Multi-repository setup instructions
- **Enhanced Testing Section**: Tests for new features

#### README.md
- **Updated Feature List**: Highlighted new capabilities
- **Added "What Makes This Special" Section**: Key differentiators
- **Updated How It Works**: Explained personalization and multi-repo
- **Added Customization Examples**: System prompts and model selection
- **Updated Communication Style**: Emphasized personalization

#### ARCHITECTURE.md
- **Added Version 2.0 Features Section**: Overview of major changes
- **Updated System Architecture Diagrams**: Multi-repo and user analysis flows
- **Enhanced Component Documentation**: Detailed new features
- **Added User Style Analysis Architecture**: Flow diagrams
- **Updated All Component Descriptions**: Version 2.0 changes

#### .env.example
- Removed `GITHUB_REPO` variable
- Added `GEMINI_MODEL` with default
- Added `OPENAI_MODEL` with default
- Added `SYSTEM_PROMPT` with explanation

### 🔄 Breaking Changes

1. **GITHUB_REPO Removed**: The `GITHUB_REPO` environment variable is no longer required or used. The bot now manages all public repositories automatically.

2. **GitHub Client API Changes**: All methods now require a `Repository` parameter:
   - `get_issue(repo, issue_number)` instead of `get_issue(issue_number)`
   - `get_pull_request(repo, pr_number)` instead of `get_pull_request(pr_number)`

3. **Response Format**: Responses now appear as comments from the authenticated user, not from a bot account.

### 🐛 Bug Fixes

- Fixed issue where bot would respond to its own comments
- Improved error handling for repository retrieval
- Enhanced rate limiting for multi-repository scenarios

### 🔒 Security Improvements

- Clarified minimal GitHub token permissions required
- Added warnings about dangerous permissions to avoid
- Documented token rotation best practices
- Added security checklist to documentation

### 📦 Dependencies

No changes to dependencies in this release.

### 🚀 Migration Guide

#### From Version 1.x to 2.0

1. **Remove GITHUB_REPO**: Delete the `GITHUB_REPO` environment variable from your deployment
   ```bash
   heroku config:unset GITHUB_REPO
   ```

2. **Add New Variables** (Optional):
   ```bash
   # Optional: Customize AI model
   heroku config:set GEMINI_MODEL="gemini-1.5-pro"
   # or
   heroku config:set OPENAI_MODEL="gpt-4o-mini"
   
   # Optional: Customize bot personality
   heroku config:set SYSTEM_PROMPT="Your custom prompt here"
   ```

3. **Update Webhooks**: If you want to manage multiple repositories:
   - Add webhooks to each repository you want managed
   - Or set up organization-wide webhook (recommended)

4. **Verify Token Permissions**: Ensure your GitHub token has:
   - `public_repo` permission
   - `read:user` permission
   - `read:org` permission (if managing org repos)

5. **Deploy**: Push the new version to your deployment platform

6. **Test**: Verify multi-repository support and personalized responses

### 📝 Notes

- All existing functionality remains intact
- Email notifications continue to work as before
- Webhook signature verification unchanged
- Rate limiting improved for multi-repository scenarios

### 🙏 Acknowledgments

This major release brings significant improvements to make the GitHub Manager more intelligent, scalable, and user-friendly. The personalized response feature ensures each contributor gets a tailored experience, while multi-repository support makes the bot truly scalable.

---

## [1.0.0] - Initial Release

### Features
- Intelligent issue assignment based on user engagement
- AI-powered responses using Gemini or OpenAI
- Optional email notifications via Resend
- Production-ready error handling and logging
- Webhook security with signature verification
- Rate limit management for GitHub API
- Support for single repository management


