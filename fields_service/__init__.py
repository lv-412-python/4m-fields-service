"""Creates Flask_App and ands resources"""
# pylint: disable = R0401
from flask import Flask
from flask_restful import Api


APP = Flask(__name__)


from fields_service.views import fields_views  # pylint: disable=wrong-import-position


API = Api(APP)
API.add_resource(fields_views.FieldAPI, '/api/v1/field/<int:field_id>')
API.add_resource(fields_views.PostAPI, '/api/v1/field')
