from db import DB


class Field(DB.Model):  # pylint: disable=too-few-public-methods
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    title = DB.Column(DB.String(100), nullable=False)
    has_choice = DB.Column(DB.Boolean, default=False)
    is_multichoice = DB.Column(DB.Boolean, default=False)
    has_autocomplete = DB.Column(DB.Boolean, default=False)
