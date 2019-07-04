"""Creates resources"""
from flask_restful import Resource
from flask import request, Response
from sqlalchemy.exc import DataError, OperationalError
from fields_service.models.field import Field
from fields_service.models.choice import Choice
from fields_service.serializers.field_schema import FieldSchema
from fields_service.db import DB


class FieldAPI(Resource):
    """Resources class"""
    attrs = ['title', 'has_choice', 'is_multichoice', 'has_autocomplete']

    def get(self, field_id):  # pylint:disable=no-self-use
        """Get route
        :param field_id: int: id of requested field
        :return json"""
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"message": "Wrong input data"}, 400
        if not field:
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
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"message": "Wrong input data"}, 400
        if not field:
            return {"message": "Field does not exists"}, 400
        for attribute in self.attrs:
            setattr(field, attribute, request.json[attribute])
        if field.has_choice:
            choices = request.json['choices']
            to_change = Choice.query.filter_by(field_id=field.id).all()
            for choice, change in zip(choices, to_change):
                setattr(change, 'title', choice['title'])
        try:
            DB.session.commit()
        except OperationalError:
            return {"message": "DB connection failed"}, 500
        return Response(status=200)

    def delete(self, field_id):  # pylint:disable=no-self-use
        """delete route
        :param field_id: int: id of requested field
        :return: int: status
        """
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"message": "Wrong input data"}, 400
        if field is None:
            return {"message": "Field does not exists"}, 400
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            for choice in choices:
                DB.session.delete(choice)
        DB.session.delete(field)
        try:
            DB.session.commit()
        except OperationalError:
            return {"message": "DB connection failed"}, 500
        return Response(status=200)


class PostAPI(Resource):
    """Resources class"""
    attrs = ['title', 'has_choice', 'is_multichoice', 'has_autocomplete']

    def post(self):
        """post route
        :return: int: status"""
        fields = {attribute: request.json[attribute] for attribute in self.attrs}
        try:
            field = Field(**fields)
            check = Field.query.filter_by(**fields).first()
        except DataError:
            return {"message": "Wrong input data"}, 400
        if check:
            return {"message": "Field already exists"}, 400
        DB.session.add(field)
        try:
            DB.session.commit()
        except OperationalError:
            return {"message": "DB connection failed"}, 500
        field = Field.query.filter_by(**fields).first()
        if field.has_choice:
            choices = request.json['choices']
            for choice in choices:
                choice = Choice(title=choice['title'], field_id=field.id)
                DB.session.add(choice)
        try:
            DB.session.commit()
        except OperationalError:
            return {"message": "DB connection failed"}, 500
        return Response(status=200)

    def get(self):  # pylint:disable=no-self-use
        """Get route"""
        fields_id = request.json['fields']
        titles = {}
        for f_id in fields_id:
            try:
                field_title = Field.query.with_entities(Field.title).filter_by(id=f_id).first()
            except DataError:
                return {"message": "Wrong input data"}, 400
            titles[f_id] = field_title.title
        return titles
