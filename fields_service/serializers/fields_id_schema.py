"""Creates schema for serialization Field titles with id."""
from marshmallow import Schema, fields


class TitlesId(Schema):
    """Implementation of Forms schema."""
    id = fields.Integer()
    title = fields.String()

    class Meta:
        """Meta class."""
        strict = True
