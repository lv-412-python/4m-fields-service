"""Creates schema for serialization Choice model."""
from marshmallow import Schema, fields


class ChoiceSchema(Schema):
    """Class for Choice model serialization."""
    id = fields.Integer()
    title = fields.Str(required=True, error_messages={"required": "title is required."})
    field_id = fields.Integer()

    class Meta:
        """Meta class."""
        strict = True
