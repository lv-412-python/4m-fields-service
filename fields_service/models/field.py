"""Field model"""
from sqlalchemy import Column, Integer, String, Boolean
from fields_service.db import DB


class Field(DB.Model):  # pylint: disable=too-few-public-methods
    """Class used to represent Field model"""
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    has_choice = Column(Boolean, default=False)
    is_multichoice = Column(Boolean, default=False)
    has_autocomplete = Column(Boolean, default=False)
