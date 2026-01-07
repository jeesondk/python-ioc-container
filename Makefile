# Makefile for python-ioc

.PHONY: install install-dev test coverage lint format type-check clean build upload help

help:
	@echo "Available commands:"
	@echo "  install       Install the package"
	@echo "  install-dev   Install the package with development dependencies"
	@echo "  test          Run tests"
	@echo "  coverage      Run tests with coverage report"
	@echo "  lint          Run linting checks"
	@echo "  format        Format code with black"
	@echo "  type-check    Run type checking with mypy"
	@echo "  clean         Remove build artifacts"
	@echo "  build         Build the package"
	@echo "  upload        Upload to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

coverage:
	pytest --cov=python_ioc --cov-report=term-missing --cov-report=html

lint:
	flake8 python_ioc tests

format:
	black python_ioc tests

type-check:
	mypy python_ioc

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

