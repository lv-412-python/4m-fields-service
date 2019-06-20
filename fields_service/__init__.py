"""Init fields service"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Configuration

APP = Flask(__name__)
APP.config.from_object(Configuration)
DB = SQLAlchemy(APP)
