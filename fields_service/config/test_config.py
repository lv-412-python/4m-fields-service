"""Testing config."""
from fields_service.config.base_config import Config


class TestingConfig(Config):
    """Testing config."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test_db'
    DEBUG = True
    TESTING = True
