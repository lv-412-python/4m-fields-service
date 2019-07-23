"""Config."""


class Config:
    """Implementation of Configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@db:5432/4m_fields'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
