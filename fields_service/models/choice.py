from db import DB


class Choice(DB.Model):  # pylint: disable=too-few-public-methods
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    title = DB.Column(DB.String(200), nullable=False)
    field_id = DB.Column(DB.Integer, nullable=False)
