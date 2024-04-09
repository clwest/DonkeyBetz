import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_executor import Executor
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import click
from flask.cli import with_appcontext


from services.config import DevelopmentConfig, TestingConfig, ProductionConfig
from services.error_handlers import register_error_handlers
from services.auth import setup_jwt
from services.cors_config import configure_cors
from services.logging_config import root_logger as logger

from factory.limiter_factory import limiter
from factory.cache_factory import cache
from helpers.helper_functions import enable_pgvector_extension

load_dotenv()
# Initialize extensions without the app context
db = SQLAlchemy()

migrate = Migrate()
jwt = JWTManager()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    from backend.helpers.db_helpers import initialize_database

    initialize_database()
    click.echo("Initialized the database.")


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Seed the database."""
    from backend.helpers.db_helpers import seed_roles_and_permissions

    seed_roles_and_permissions()
    click.echo("Seeded the database.")


def create_app():
    app = Flask(__name__)
    env_config = os.getenv("FLASK_ENV")

    if env_config == "development":
        app.config.from_object(DevelopmentConfig)
    elif env_config == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    # Initialize extensions with the app context
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    configure_cors(app)
    # configure_logging(app)
    limiter.init_app(app)
    cache.init_app(app)
    register_error_handlers(app)
    setup_jwt(app)
    app.logger.handlers = logger.handlers
    app.executor = Executor(app)

    with app.app_context():
        enable_pgvector_extension()

    from routes.users import users_blp
    from routes.chatbot import chatbot_blp
    from routes.blogs import blog_blp
    from routes.crypto_news import crypto_news_blp
    from routes.process_data import process_data_blp

    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)

    # Register blueprints
    app.register_blueprint(blog_blp, url_prefix="/api/blog")
    app.register_blueprint(users_blp, url_prefix="/api/users")
    app.register_blueprint(chatbot_blp, url_prefix="/api/chatbot")
    app.register_blueprint(crypto_news_blp, url_prefix="/api/crypto-news")
    app.register_blueprint(process_data_blp, url_prefix="/api/process-data")

    return app
