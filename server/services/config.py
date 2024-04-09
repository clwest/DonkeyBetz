import os
from dotenv import load_dotenv


load_dotenv()

class Config(object):
    """Base config, uses staging database server."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """Uses production database server."""
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URL')

class DevelopmentConfig(Config):
    """Uses a development database server."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

class TestingConfig(Config):
    """Uses a testing database server."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URL')
