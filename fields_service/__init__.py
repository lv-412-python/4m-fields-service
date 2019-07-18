"""Creates Flask_App and ands resources"""
# pylint: disable = cyclic-import
from flask import Flask
from flask_restful import Api
from flask_cors import CORS


APP = Flask(__name__)
API = Api(APP, catch_all_404s=True)
CORS(APP)

from fields_service.views import resources  # pylint: disable=wrong-import-position
