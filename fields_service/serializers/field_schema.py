"""Creates schema for serialization Field model"""
from marshmallow import Schema, fields
from fields_service.models.field import Field  # pylint: disable=import-error
from fields_service.serializers.choice_schema import ChoiceSchema  # pylint: disable=import-error


class FieldSchema(Schema):
    """Class for Field model serialization"""
    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""
        model = Field
        fields = ("id", "title", "has_choice", "is_multichoice", "has_autocomplete", "choices")
    choices = fields.Nested(ChoiceSchema, many=True)
