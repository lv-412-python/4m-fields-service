"""Creates resources."""
from flask import request, Response
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import DataError, IntegrityError

from fields_service.db import DB
from fields_service.models.choice import Choice
from fields_service.models.field import Field
from fields_service.serializers.field_schema import FieldSchema


OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404


class FieldResource(Resource):
    """Resources class."""
    def get(self, field_id):
        """Get route.
        :param field_id: int: id of requested field.
        :return json."""
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"error": "Invalid url."}, NOT_FOUND
        if field is None:
            return {"error": "Does not exist."}, BAD_REQUEST
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            field.choices = choices
        field = FieldSchema().dump(obj=field).data
        return field, OK

    def put(self, field_id):
        """put route.
        :param field_id: int: id of requested field.
        :return: int: status.
        """
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"error": "Invalid url."}, NOT_FOUND
        if not field:
            return {"error": "Does not exist."}, BAD_REQUEST
        try:
            data = FieldSchema().load(request.json).data
        except ValidationError as err:
            return err.messages, BAD_REQUEST
        choices = data.pop('choices', None)
        for key, value in data.items():
            setattr(field, key, value)
        if field.has_choice:
            to_change = Choice.query.filter_by(field_id=field.id).all()
            for choice, change in zip(choices, to_change):
                change.title = choice['title']
        try:
            DB.session.commit()
        except IntegrityError:
            return {"Error": "Already exists."}, BAD_REQUEST
        return Response(status=OK)

    def delete(self, field_id):
        """delete route.
        :param field_id: int: id of requested field.
        :return: int: status.
        """
        try:
            field = Field.query.get(field_id)
        except DataError:
            return {"error": "Invalid url."}, NOT_FOUND
        if field is None:
            return {"error": "Does not exist."}, BAD_REQUEST
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            for choice in choices:
                DB.session.delete(choice)
        DB.session.delete(field)
        DB.session.commit()
        return Response(status=OK)


class PostResource(Resource):
    """Resources class."""

    def post(self):
        """post route.
        :return: int: status."""

        try:
            data = FieldSchema().load(request.json).data
        except ValidationError as err:
            return err.messages, BAD_REQUEST
        choices = data.pop('choices', None)
        field = Field(**data)
        DB.session.add(field)
        DB.session.commit()
        if data['has_choice']:
            field = Field.query.filter_by(**data).order_by(Field.id.desc()).first()
            for choice in choices:
                choice = Choice(title=choice['title'], field_id=field.id)
                DB.session.add(choice)
        try:
            DB.session.commit()
        except IntegrityError:
            DB.session.remove()
            DB.session.delete(field)
            DB.session.commit()
            DB.session.rollback()
            return {"error": "Already exists."}, BAD_REQUEST
        return Response(status=OK)

    def get(self):
        """Get route."""
        fields_id = request.json['fields']
        titles = {}
        for f_id in fields_id:
            try:
                field_title = Field.query.with_entities(Field.title).filter_by(id=f_id).first()
            except DataError:
                return {"message": "Wrong input data"}, BAD_REQUEST
            titles[f_id] = field_title.title
        return titles
