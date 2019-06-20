from flask import Flask
from views import hello_world
from flask_restful import Api

APP = Flask(__name__)
api = Api(APP)
api.add_resource(hello_world.HelloWorld, '/id')
