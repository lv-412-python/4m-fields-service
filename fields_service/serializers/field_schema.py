"""Creates schema for serialization Field model."""
from marshmallow import Schema, fields

from fields_service.serializers.choice_schema import ChoiceSchema


class FieldSchema(Schema):
    """Class for Field model serialization."""
    id = fields.Integer()
    title = fields.String(required=True, error_messages={"required": "title is required."})
    has_choice = fields.Boolean(required=True,
                                error_messages={"required": "has_choice is required."})
    is_multichoice = fields.Boolean(required=True,
                                    error_messages={"required": "is_multichoice is required."})
    has_autocomplete = fields.Boolean(required=True,
                                      error_messages={"required": "has_autocomplete is required."})
    choices = fields.Nested(ChoiceSchema, many=True)

    class Meta:
        """Meta class."""
        strict = True
