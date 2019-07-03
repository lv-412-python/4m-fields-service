"""Field model."""
from sqlalchemy import Column, Integer, String, UniqueConstraint

from fields_service.db import DB


class Choice(DB.Model):
    """Class used to represent Choice model."""
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    field_id = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('title', 'field_id'), )
