"""
Package: service

Creates and configures the Flask app, sets up logging, and initializes the database.
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers
from service.models import init_db

# Create Flask app
app = Flask(__name__)

# Load Configurations
app.config.from_object(config)

# Set up logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  P R O D U C T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Import routes AFTER app creation
from service import routes  # noqa: E402

# Initialize database
try:
    init_db(app)
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
