"""Connects to database"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from fields_service.config.dev_config import DevelopmentConfig
from fields_service import APP


APP.config.from_object(DevelopmentConfig)
DB = SQLAlchemy(APP)


migrate = Migrate(APP, DB)  # pylint: disable=invalid-name
