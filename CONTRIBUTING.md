# Contributing to GitHub Manager

Thank you for your interest in contributing to GitHub Manager! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title**: Describe the bug briefly
2. **Description**: Detailed explanation of the issue
3. **Steps to reproduce**: How to recreate the bug
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**: 
   - Python version
   - Heroku or local
   - AI provider (Gemini/OpenAI)
7. **Logs**: Relevant log output (remove sensitive data)

### Suggesting Features

For feature requests, create an issue with:

1. **Clear title**: Describe the feature
2. **Use case**: Why is this feature needed?
3. **Proposed solution**: How should it work?
4. **Alternatives**: Other approaches considered
5. **Additional context**: Screenshots, examples, etc.

### Pull Requests

We welcome pull requests! Here's the process:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Create a pull request**

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def process_issue(issue: Issue, comment: IssueComment) -> bool:
    """
    Process a new comment on an issue.
    
    Args:
        issue: GitHub issue object
        comment: Comment object to process
    
    Returns:
        True if processed successfully, False otherwise
    """
    # Implementation here
    pass
```

### Error Handling

- Always use try-except blocks for external API calls
- Log errors with appropriate level (ERROR, WARNING)
- Return None or False on failure (don't raise)
- Provide helpful error messages

Example:
```python
try:
    result = api_call()
    logger.info("Operation successful")
    return result
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return None
```

### Logging

- Use appropriate log levels:
  - DEBUG: Detailed debugging information
  - INFO: General informational messages
  - WARNING: Warning messages (non-critical)
  - ERROR: Error messages (operation failures)
  - CRITICAL: Critical errors (system failures)

- Include context in log messages:
```python
logger.info(f"Processing issue #{issue.number}")
logger.error(f"Failed to assign issue #{issue.number}: {error}")
```

### Testing

Before submitting a PR:

1. **Test locally**:
   ```bash
   python app.py
   ```

2. **Validate configuration**:
   ```bash
   python validate_config.py
   ```

3. **Test with real GitHub events** (if possible)

4. **Check logs for errors**

5. **Verify all features work**:
   - Issue assignment
   - AI responses
   - Email notifications (if configured)
   - Webhook handling

### Documentation

- Update README.md if adding user-facing features
- Update SETUP.md if changing configuration
- Update ARCHITECTURE.md if changing structure
- Add inline comments for complex logic
- Update docstrings when changing functions

## 🏗️ Project Structure

When adding new features, follow the existing structure:

```
src/
├── config.py          # Configuration management
├── logger.py          # Logging setup
├── github_client.py   # GitHub API interactions
├── ai_service.py      # AI provider abstraction
├── email_service.py   # Email notifications
├── issue_manager.py   # Issue management logic
├── pr_manager.py      # PR management logic
└── webhook_handler.py # Webhook processing
```

### Adding a New Feature

1. **Identify the right module**: Where does this feature belong?
2. **Create new module if needed**: For major features
3. **Update dependencies**: Add to requirements.txt if needed
4. **Add configuration**: Update config.py if needed
5. **Add error handling**: Follow existing patterns
6. **Add logging**: Log important events
7. **Update documentation**: README, SETUP, or ARCHITECTURE
8. **Test thoroughly**: Ensure it works end-to-end

## 🔍 Code Review Process

Pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Code quality**: Is it clean and maintainable?
3. **Error handling**: Are errors handled properly?
4. **Logging**: Are important events logged?
5. **Documentation**: Is it documented?
6. **Testing**: Has it been tested?
7. **Style**: Does it follow project conventions?

## 🐛 Debugging Tips

### Local Development

1. **Use .env file**: Copy .env.example to .env
2. **Set LOG_LEVEL=DEBUG**: For detailed logs
3. **Test with ngrok**: Expose local server to GitHub webhooks
   ```bash
   ngrok http 5000
   ```
4. **Use GitHub webhook redelivery**: Test specific events

### Common Issues

**Bot not responding:**
- Check Heroku logs
- Verify webhook secret
- Check GitHub token permissions
- Verify AI API key

**Rate limit errors:**
- Wait for rate limit reset
- Check rate limit status in logs
- Consider caching if needed

**AI responses failing:**
- Check AI provider API key
- Verify provider quota
- Check logs for specific errors

## 📚 Resources

- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Google Gemini API](https://ai.google.dev/docs)
- [OpenAI API](https://platform.openai.com/docs)

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **Testing**: Automated test suite
2. **Performance**: Optimization and caching
3. **Features**: New assignment algorithms
4. **Documentation**: Tutorials and examples
5. **Monitoring**: Metrics and dashboards
6. **Multi-repo**: Support for multiple repositories

## 💡 Ideas for Contributions

- Add support for more AI providers (Claude, etc.)
- Implement assignment history tracking
- Add custom assignment rules configuration
- Create dashboard for bot statistics
- Add support for GitHub Actions integration
- Implement slash commands
- Add support for GitHub Discussions
- Create automated test suite
- Add Prometheus metrics
- Implement caching layer

## ❓ Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Review the documentation (README, SETUP, ARCHITECTURE)
3. Create an issue with your question
4. Be specific and provide context

## 🙏 Thank You!

Every contribution helps make GitHub Manager better. Whether it's:

- Reporting a bug
- Suggesting a feature
- Improving documentation
- Submitting code
- Helping others

Your contribution is valued and appreciated! 🎉

---

**Happy Contributing!** 🚀

