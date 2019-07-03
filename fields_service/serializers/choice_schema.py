"""Creates schema for serialization Choice model"""
from marshmallow import Schema
from fields_service.models.choice import Choice  # pylint: disable=import-error


class ChoiceSchema(Schema):
    """Class for Choice model serialization"""
    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""
        model = Choice
        fields = ("id", "title", "field_id")
