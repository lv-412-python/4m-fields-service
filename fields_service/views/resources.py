"""API routes"""
from fields_service import API
from .fields_views import FieldResource


API.add_resource(FieldResource, '/field', '/field/<field_id>')
