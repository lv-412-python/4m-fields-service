"""Field model"""
from sqlalchemy import Column, Integer, String
from fields_service.db import DB


class Choice(DB.Model):  # pylint: disable=too-few-public-methods
    """Class used to represent Choice model"""
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    field_id = Column(Integer, nullable=False)

    def __repr__(self):
        return 'Choice(id={}, title={}, field_id={})'.format(self.id, self.title, self.field_id)
