"""Creates resources."""
from flask import request, Response, jsonify
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError, fields
from sqlalchemy.exc import DataError, IntegrityError
from webargs.flaskparser import parser

from fields_service import APP
from fields_service.db import DB
from fields_service.models.choice import Choice
from fields_service.models.field import Field
from fields_service.serializers.field_schema import FieldSchema


class FieldResource(Resource):
    """Resources class."""
    def get(self, field_id=None):
        """Get route.
        :param field_id: int: id of requested field.
        :return json."""
        if not field_id:
            field_id = {'field_id': fields.List(fields.Int(validate=lambda val: val > 0))}
            try:
                fields_id = parser.parse(field_id, request)
            except HTTPException:
                return {"error": "Invalid url"}, status.HTTP_400_BAD_REQUEST
            titles = {}
            for f_id in fields_id['field_id']:
                field_title = Field.query.with_entities(Field.title).filter_by(id=f_id).first()
                if not field_title:
                    APP.logger.error('Field with id %s does not exist', f_id)
                    message = {"error": "Does not exist."}
                    resp = jsonify(message)
                    resp.status_code = status.HTTP_400_BAD_REQUEST
                    break
                titles[f_id] = field_title.title
            else:
                resp = jsonify(titles)
                resp.status_code = status.HTTP_200_OK
            return resp

        try:
            field = Field.query.get(field_id)
        except DataError as err:
            APP.logger.error(err.args)
            return {"error": "Invalid url."}, status.HTTP_404_NOT_FOUND
        if field is None:
            APP.logger.error('Field with id %s does not exist', field_id)
            return {"error": "Does not exist."}, status.HTTP_400_BAD_REQUEST
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            field.choices = choices
        field = FieldSchema().dump(obj=field).data
        return field, status.HTTP_200_OK

    def put(self, field_id):
        """put route.
        :param field_id: int: id of requested field.
        :return: int: status.
        """
        try:
            field = Field.query.get(field_id)
        except DataError as err:
            APP.logger.error(err.args)
            return {"error": "Invalid url."}, status.HTTP_404_NOT_FOUND
        if not field:
            APP.logger.error('Field with id %s does not exist', field_id)
            return {"error": "Does not exist."}, status.HTTP_400_BAD_REQUEST
        try:
            data = FieldSchema().load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST
        choices = data.pop('choices', None)
        for key, value in data.items():
            setattr(field, key, value)
        if field.has_choice:
            to_change = Choice.query.filter_by(field_id=field.id).all()
            for choice, change in zip(choices, to_change):
                change.title = choice['title']
        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            return {"Error": "Already exists."}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_200_OK)

    def delete(self, field_id):
        """delete route.
        :param field_id: int: id of requested field.
        :return: int: status.
        """
        try:
            field = Field.query.get(field_id)
        except DataError as err:
            APP.logger.error(err.args)
            return {"error": "Invalid url."}, status.HTTP_404_NOT_FOUND
        if field is None:
            APP.logger.error('Field with id %s does not exist', field_id)
            return {"error": "Does not exist."}, status.HTTP_400_BAD_REQUEST
        if field.has_choice:
            choices = Choice.query.filter_by(field_id=field.id).all()
            for choice in choices:
                DB.session.delete(choice)
        DB.session.delete(field)
        DB.session.commit()
        return Response(status=status.HTTP_200_OK)

    def post(self):
        """post route.
        :return: int: status."""
        try:
            data = FieldSchema().load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST
        choices = data.pop('choices', None)
        field = Field(**data)
        DB.session.add(field)
        DB.session.commit()
        if data['has_choice']:
            for choice in choices:
                choice = Choice(title=choice['title'], field_id=field.id)
                DB.session.add(choice)
        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            DB.session.remove()
            DB.session.delete(field)
            DB.session.commit()
            DB.session.rollback()
            return {"error": "Already exists."}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_200_OK)
