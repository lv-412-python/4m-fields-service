"""Production config."""
from fields_service.config.base_config import Config


class ProductionConfig(Config):
    """Production config."""
    DEBUG = False
