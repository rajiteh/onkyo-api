# 🎵 Onkyo API

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, production-ready RESTful API for controlling network-enabled Onkyo receivers via the EISCP protocol. Built with Flask, Connexion, and OpenAPI 3.0.

## ✨ Features

- 🚀 **Modern Python**: Built with Python 3.10+ and latest dependencies
- 📡 **RESTful API**: Clean OpenAPI 3.0 specification
- 📚 **Interactive Documentation**: Built-in Swagger UI
- 🐳 **Docker Ready**: Multi-stage optimized Docker builds
- 🧪 **Tested**: Comprehensive test suite with pytest
- 🔒 **Secure**: Non-root Docker containers, environment-based configuration
- ⚡ **Fast**: Uses [uv](https://github.com/astral-sh/uv) for blazing-fast dependency management

## 📋 Requirements

- **Python**: 3.10 or higher
- **uv**: Modern Python package installer (recommended)
- **Docker**: For containerized deployment (optional)
- **Onkyo Receiver**: Network-enabled Onkyo/Integra receiver

## 🚀 Quick Start

### Installation with uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/rajiteh/onkyo-api.git
cd onkyo-api

# Create virtual environment and install dependencies
uv sync

# Or install with dev dependencies
uv sync --all-extras
```

### Installation with pip

```bash
git clone https://github.com/rajiteh/onkyo-api.git
cd onkyo-api
pip install -e .
```

### Using Docker

```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or build and run manually
docker build -t onkyo-api .
docker run -d -p 8000:8000 --net=host --name onkyo-api onkyo-api
```

## 🏃 Running the Application

### Locally

```bash
# Simple start (if using uv)
uv run python main.py

# Or if installed with pip
python main.py

# Or using make
make run

# With custom configuration
HOST=0.0.0.0 PORT=8080 DEBUG=true uv run python main.py
```

### With Docker Compose

```bash
docker-compose up -d
```

### Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Available configuration options:

```env
HOST=0.0.0.0        # Server host
PORT=8000           # Server port
DEBUG=false         # Debug mode
LOG_LEVEL=INFO      # Logging level
```

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/v1/ui/
- **OpenAPI Spec**: http://localhost:8000/api/v1/openapi.json
- **Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## 🎯 Usage Examples

### Basic Commands

```bash
# Turn on the receiver
curl http://localhost:8000/api/v1/onkyo/power=on

# Turn off the receiver
curl http://localhost:8000/api/v1/onkyo/power=off

# Set volume to 20
curl http://localhost:8000/api/v1/onkyo/volume=20

# Get current power status (query command)
curl http://localhost:8000/api/v1/onkyo/power=query
```

### Response Format

All API responses return JSON with a `success` field:

#### Successful Query Response
```json
{
  "success": true,
  "receiver": "TX-NR7100",
  "command": "master-volume",
  "value": "125",
  "raw": "TX-NR7100: master-volume = 125"
}
```

#### Successful Non-Query Response
```json
{
  "success": true,
  "message": "Command sent successfully"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Command failed with exit code 1",
  "exit_code": 1,
  "stderr": "error details here"
}
```

**Query vs Non-Query Commands:**
- **Query commands** (e.g., `power=query`, `volume=query`) return the current state
- **Non-query commands** (e.g., `power=on`, `volume=25`) set a value and confirm execution

### Targeting Specific Receivers

You can specify a receiver by hostname or IP address using the `host` and `port` query parameters:

```bash
# Target a specific receiver by IP
curl "http://localhost:8000/api/v1/onkyo/power=on?host=192.168.1.100"

# Target a specific receiver by hostname
curl "http://localhost:8000/api/v1/onkyo/volume=25?host=onkyo.local"

# Specify both host and port (default port is 60128)
curl "http://localhost:8000/api/v1/onkyo/power=on?host=192.168.1.100&port=60128"
```
 
## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies using uv
uv sync

# Or with make
make dev-install
```

### Available Make Commands

```bash
make help          # Show available commands
make install       # Install production dependencies
make dev-install   # Install development dependencies
make run           # Run the development server
make test          # Run tests with coverage
make format        # Format code with black
make lint          # Lint code with ruff and mypy
make clean         # Clean build artifacts
make docker-build  # Build Docker image
make docker-run    # Run Docker container
```

### Running Tests

```bash
# Run all tests with uv
uv run pytest

# Or use make
make test

# With coverage report
uv run pytest --cov=. --cov-report=html
```

### Code Quality

```bash
# Format code
uv run black .
# Or: make format

# Lint code
uv run ruff check .
uv run mypy . --ignore-missing-imports
# Or: make lint
```

## 📦 Dependencies

### Core Dependencies

- **Flask** 3.1.0+ - Modern web framework
- **Connexion** 3.1.0+ - OpenAPI-first REST framework
- **onkyo-eiscp** 1.2.7+ - Onkyo receiver control library
- **python-dotenv** 1.0.0+ - Environment configuration

### Development Dependencies

- **pytest** 8.3.0+ - Testing framework
- **black** 24.10.0+ - Code formatter
- **ruff** 0.7.0+ - Fast Python linter
- **mypy** 1.13.0+ - Static type checker

## 🏗️ Project Structure

```
onkyo-api/
├── main.py              # Application entry point
├── onkyo.py             # Onkyo command execution module
├── swagger.yml          # OpenAPI 3.0 specification
├── pyproject.toml       # Project dependencies and config
├── Dockerfile           # Multi-stage Docker build
├── docker-compose.yml   # Docker Compose configuration
├── Makefile             # Development commands
├── tests/               # Test suite
│   ├── test_api.py      # API endpoint tests
│   └── test_onkyo.py    # Onkyo module tests
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Troubleshooting

### Receiver Not Found

Ensure your Onkyo receiver is:
- Connected to the same network
- Has network control enabled in settings
- Firewall allows communication on the EISCP port (60128)

### Docker Network Issues

Use `--net=host` to allow Docker container to discover receivers on your local network:

```bash
docker run -d -p 8000:8000 --net=host onkyo-api
```

### Command Not Found

If you get "onkyo command not found" errors, ensure `onkyo-eiscp` is properly installed:

```bash
uv pip install onkyo-eiscp
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [onkyo-eiscp](https://github.com/miracle2k/onkyo-eiscp) - Python library for Onkyo EISCP protocol
- [Connexion](https://github.com/spec-first/connexion) - OpenAPI-first REST framework
- [Flask](https://flask.palletsprojects.com/) - Web framework

## 📚 Additional Resources

- [Onkyo EISCP Protocol Documentation](https://github.com/miracle2k/onkyo-eiscp)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

Made with ❤️ for the Onkyo community