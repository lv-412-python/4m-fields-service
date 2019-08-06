"""Creates resources."""
from flask import request, Response
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
from fields_service.serializers.fields_id_schema import TitlesId


class FieldResource(Resource):
    """Resources class."""
    def get(self, field_id=None):
        """Get route.
        :param field_id: int: id of requested field.
        :return json."""
        if not field_id:
            args = {
                'field_id': fields.List(fields.Int(validate=lambda val: val > 0)),
                'owner': fields.List(fields.Int(validate=lambda value: value > 0))
            }
            try:
                args = parser.parse(args, request)
            except HTTPException:
                return {"error": "Invalid url"}, status.HTTP_400_BAD_REQUEST
            if not args.get('field_id', None):
                all_fields = Field.query.with_entities(Field.id, Field.title).\
                    filter(Field.owner.in_(args['owner'])).all()
                data = TitlesId(many=True).dump(obj=all_fields).data
                return (data, status.HTTP_200_OK) if data else \
                    ({"error": "Does not exist."}, status.HTTP_400_BAD_REQUEST)
            titles_ids = []
            for f_id in args['field_id']:
                element = Field.query.filter_by(id=f_id).first()
                if not element:
                    APP.logger.error('Field with id %s does not exist', f_id)
                    resp = {"error": "Does not exist."}
                    status_code = status.HTTP_400_BAD_REQUEST
                    break
                if element.has_choice:
                    choices = Choice.query.filter_by(field_id=f_id).all()
                    element.choices = choices
                titles_ids.append(element)
            else:
                resp = FieldSchema(many=True).dump(obj=titles_ids).data
                status_code = status.HTTP_200_OK
            return resp, status_code
        try:
            field = Field.query.get(field_id)
        except DataError as err:
            APP.logger.error(err.args)
            return {"error": "Invalid url."}, status.HTTP_400_BAD_REQUEST
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
            return {"error": "Invalid url."}, status.HTTP_400_BAD_REQUEST
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
        if not field.has_choice and field.is_multichoice:
            return {"error": "Field with type 'text' cannot be multichoice."}, \
                   status.HTTP_400_BAD_REQUEST
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
            return {"error": "Invalid url."}, status.HTTP_400_BAD_REQUEST
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
        if not field.has_choice and field.is_multichoice:
            return {"error": "Field with type 'text' cannot be multichoice."}, \
                   status.HTTP_400_BAD_REQUEST
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
