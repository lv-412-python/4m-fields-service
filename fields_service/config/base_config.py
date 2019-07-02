"""config"""


class Config:  # pylint: disable=too-few-public-methods
    """
        Implementation of Configuration class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = '3wffe3423@#Rr23krpo43o4t'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_fields'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
