"""
Onkyo API Server
A modern RESTful API for controlling network-enabled Onkyo receivers.
"""

import os
import warnings
from pathlib import Path

# Filter out SyntaxWarnings from dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning)

import connexion
from dotenv import load_dotenv
from flask import jsonify

# Load environment variables
load_dotenv()

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


def create_app():
    """Create and configure the Connexion application."""
    # Create Connexion app with OpenAPI 3.x support
    app = connexion.FlaskApp(
        __name__,
        specification_dir=Path(__file__).parent,
    )

    # Add OpenAPI specification
    app.add_api(
        "swagger.yml",
        arguments={"title": "Onkyo API"},
        pythonic_params=True,
    )

    # Get the underlying Flask app
    flask_app = app.app

    # Add custom routes
    @flask_app.route("/")
    def index():
        """Root endpoint - redirect to API docs."""
        return jsonify(
            {
                "name": "Onkyo API",
                "version": "1.0.0",
                "documentation": "/api/v1/ui/",
                "openapi_spec": "/api/v1/openapi.json",
            }
        )

    @flask_app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200

    return app


def main():
    """Run the application."""
    app = create_app()
    app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
