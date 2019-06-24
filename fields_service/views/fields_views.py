"""Creates resources"""
from flask_restful import Resource
from flask import request, Response
from fields_service.models.field import Field
from fields_service.models.choice import Choice
from fields_service.serializers.field_schema import FieldSchema
from fields_service.db import DB


#pylint: disable = R0201
#pylint: disable = E1101
class FieldAPI(Resource):
    """Resources class"""
    attrs = ['title', 'has_choice', 'is_multichoice', 'has_autocomplete']

    def get(self, field_id):
        """Get route
        :param field_id: int: id of requested field
        :return json"""
        field = Field.query.get(field_id)
        if field is None:
            return {"message": "Field does not exists"}, 400
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            field.choices = choices
        field = FieldSchema().dump(obj=field).data
        return field, 200

    def put(self, field_id):
        """put route
        :param field_id: int: id of requested field
        :return: int: status
        """
        field = Field.query.get(field_id)
        if field is None:
            return {"message": "Field does not exists"}, 400
        for attribute in self.attrs:
            setattr(field, attribute, request.json[attribute])
        if field.has_choice:
            choices = request.json['choices']
            to_change = Choice.query.filter_by(field_id=field.id).all()
            for choice, change in zip(choices, to_change):
                setattr(change, 'title', choice['title'])
        DB.session.commit()
        return Response(status=200)

    def delete(self, field_id):
        """delete route
        :param field_id: int: id of requested field
        :return: int: status
        """
        field = Field.query.get(field_id)
        if field is None:
            return {"message": "Field does not exists"}, 400
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            for choice in choices:
                DB.session.delete(choice)
        DB.session.delete(field)
        DB.session.commit()
        return Response(status=200)


class PostAPI(Resource):
    """Resources class"""
    attrs = ['title', 'has_choice', 'is_multichoice', 'has_autocomplete']

    def post(self):
        """post route
        :return: int: status"""
        fields = {attribute: request.json[attribute] for attribute in self.attrs}
        field = Field(**fields)
        check = Field.query.filter_by(**fields).first()
        if check:
            return {"message": "Field already exists"}, 400
        DB.session.add(field)
        DB.session.commit()
        field = Field.query.filter_by(**fields).first()
        if field.has_choice:
            choices = request.json['choices']
            for choice in choices:
                choice = Choice(title=choice['title'], field_id=field.id)
                DB.session.add(choice)
        DB.session.commit()
        return Response(status=200)

    def get(self):
        """Get route"""
        fields_id = request.json['fields']
        titles = {}
        for f_id in fields_id:
            field_title = Field.query.with_entities(Field.title).filter_by(id=f_id).first()
            titles[f_id] = field_title.title
        return titles
