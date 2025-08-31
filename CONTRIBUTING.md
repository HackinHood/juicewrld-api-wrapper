# Contributing to Juice WRLD API Wrapper

Thank you for your interest in contributing to the Juice WRLD API Wrapper! This document provides guidelines and information for contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following the guidelines below
5. **Test your changes** thoroughly
6. **Submit a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/hackinhood/juicewrld-api-wrapper.git
cd juicewrld-api-wrapper

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Code Style

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for public methods
- Keep functions **focused and single-purpose**
- Use **descriptive variable names**

## Testing

Run tests before submitting your changes:

```bash
# Run all tests
python -m pytest test_wrapper.py -v

# Run with coverage
python -m pytest test_wrapper.py --cov=juicewrld_api_wrapper
```

## Pull Request Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what the PR does and why
- **Tests**: Include tests for new functionality
- **Documentation**: Update docs if adding new features
- **Breaking Changes**: Clearly mark any breaking changes

## Issue Reporting

When reporting issues, please include:

- **Python version**
- **Operating system**
- **Error messages** (full traceback)
- **Steps to reproduce**
- **Expected vs actual behavior**

## Code of Conduct

- Be respectful and inclusive
- Focus on the code and technical aspects
- Help others learn and improve
- Follow GitHub's community guidelines

## Questions?

Feel free to open an issue for questions or discussions about the project.
