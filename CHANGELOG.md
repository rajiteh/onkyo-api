# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-15

### 🎉 Major Modernization Release

#### Added
- **Modern Dependencies**: Upgraded to latest versions
  - Flask 3.1.0+ (from legacy versions)
  - Connexion 3.1.0+ with OpenAPI 3.0 support
  - Python 3.10+ support (Python 2.7 → 3.12)
- **Development Tools**
  - pytest for comprehensive testing
  - black for code formatting
  - ruff for fast linting
  - mypy for type checking
  - GitHub Actions CI/CD workflow
- **Docker Improvements**
  - Multi-stage builds for smaller images
  - Non-root user for security
  - Health checks
  - docker-compose.yml for easy deployment
- **Configuration Management**
  - Environment-based configuration with python-dotenv
  - .env.example template
  - Configurable host, port, and debug settings
- **Documentation**
  - Comprehensive README with examples
  - Interactive Swagger UI
  - API documentation at /api/v1/ui/
  - Code documentation and type hints
- **Testing**
  - Unit tests for API endpoints
  - Unit tests for onkyo module
  - Test coverage reporting
- **Developer Experience**
  - Makefile with common commands
  - uv for fast dependency management
  - .python-version for version pinning
  - Comprehensive .gitignore
  - MIT License

#### Changed
- **Breaking**: Migrated from Python 2.7 to Python 3.10+
- **Breaking**: Switched from pip to uv for dependency management
- **Breaking**: Migrated from Swagger 2.0 to OpenAPI 3.0
- Improved error handling in onkyo.py with detailed logging
- Better application structure with factory pattern
- Enhanced Docker security with non-root containers
- Updated all dependency versions to latest

#### Removed
- Python 2.7 support and legacy dependencies
- requirements.txt (replaced by pyproject.toml)
- Legacy connexion.App usage (now connexion.FlaskApp)

### Migration Guide

To upgrade from the old version:

1. **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Install dependencies**: `uv pip install -e .`
3. **Update environment**: Copy `.env.example` to `.env` and configure
4. **Run tests**: `make test`
5. **Start application**: `make run` or `docker-compose up`

## [0.1.0] - Legacy

### Initial Release
- Basic Python 2.7 implementation
- Connexion-based API
- Docker support
- Basic Onkyo receiver control
