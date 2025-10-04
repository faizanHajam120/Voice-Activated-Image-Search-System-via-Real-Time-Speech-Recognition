# Contributing to Voice-Activated Image Search System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Google Cloud Platform account (for testing)
- Docker (optional, for containerized development)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio.git
   cd Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🛠️ Development Workflow

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run linting
flake8 .
black --check .
```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write tests for new functionality
   - Update documentation if needed
   - Ensure all tests pass

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Commit Message Convention

Use conventional commits format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Examples:
```
feat: add voice command validation
fix: resolve audio buffer overflow issue
docs: update API documentation
```

## 🧪 Testing Guidelines

### Unit Tests
- Write tests for all new functions
- Aim for >80% code coverage
- Test edge cases and error conditions

### Integration Tests
- Test API endpoints
- Test voice recognition pipeline
- Test image search functionality

### Manual Testing
- Test with different audio inputs
- Verify search accuracy
- Check GUI responsiveness

## 🐛 Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Screenshots (if applicable)

## 💡 Feature Requests

For feature requests, please:
- Describe the feature clearly
- Explain the use case
- Consider implementation complexity
- Check for existing similar requests

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🏷️ Release Process

Releases are managed by maintainers:
1. Version bump in appropriate files
2. Update CHANGELOG.md
3. Create release tag
4. Deploy to production

## 📞 Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
