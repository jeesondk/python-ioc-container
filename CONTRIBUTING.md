# Contributing to Python IoC
Thank you for contributing!

Feel free to open an issue for questions or discussions.

## Questions?

- Expected vs actual behavior
- Minimal code to reproduce the issue
- Operating system
- Python version
When reporting issues, please include:

## Reporting Issues

- Aim for 100% test coverage
- Keep functions small and focused
- Write docstrings for all public functions/classes
- Use type hints
- Follow PEP 8 guidelines

## Code Style

- Keep PRs focused on a single feature/fix
- Ensure all CI checks pass
- Update documentation as needed
- Include tests for new features
- Write clear, descriptive commit messages

## Pull Request Guidelines

6. Create a Pull Request

   ```
   git push origin feature/your-feature-name
   ```bash
5. Push to your fork:

   ```
   git commit -m "Add your descriptive commit message"
   ```bash
4. Commit your changes:

3. Add tests for new functionality

   - Docstrings are added/updated
   - Type hints are included
   - No linting errors
   - Code is formatted with black
   - All tests pass
2. Make your changes and ensure:

   ```
   git checkout -b feature/your-feature-name
   ```bash
1. Create a new branch:

### Making Changes

```
mypy python_ioc
```bash
Type check with mypy:

```
flake8 python_ioc tests
```bash
Lint code with flake8:

```
black python_ioc tests
```bash
Format code with black:

### Code Quality

```
pytest --cov=python_ioc --cov-report=html
```bash
Run tests with coverage:

```
pytest
```bash
Run all tests:

### Running Tests

## Development Workflow

   ```
   pip install -e ".[dev]"
   ```bash
4. Install development dependencies:

   ```
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   python -m venv .venv
   ```bash
3. Create a virtual environment:

   ```
   cd python-ioc
   git clone https://github.com/yourusername/python-ioc.git
   ```bash
2. Clone your fork:
1. Fork the repository

## Development Setup

Thank you for considering contributing to Python IoC! This document outlines the process for contributing to this project.


