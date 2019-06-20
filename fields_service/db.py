from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from . import APP


class Configuration:  # pylint: disable=too-few-public-methods
    """
    Implementation of Configuration class.
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


APP.config.from_object(Configuration)
DB = SQLAlchemy(APP)


migrate = Migrate(APP, DB)
