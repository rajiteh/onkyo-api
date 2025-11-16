.PHONY: help install dev-install run test format lint clean docker-build docker-run

help:
	@echo "Onkyo API - Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make run          - Run the development server"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	uv sync --no-dev

dev-install:
	uv sync

run:
	uv run python main.py

test:
	uv run pytest

format:
	uv run black .

lint:
	uv run ruff check .
	uv run mypy . --ignore-missing-imports

clean:
	rm -rf __pycache__ .pytest_cache .coverage .mypy_cache
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .venv .uv

docker-build:
	docker build -t onkyo-api:latest .

docker-run: docker-build
	docker run -it --rm -p 8000:8000 --name onkyo-api onkyo-api:latest
