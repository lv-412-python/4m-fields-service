"""Testing resources."""
from unittest import main

from flask_testing import TestCase

from fields_service import APP
from fields_service.config.test_config import TestingConfig
from fields_service.db import DB
from fields_service.models.choice import Choice
from fields_service.models.field import Field


def create_app(config_obj):
    """
    Creates testing app.
    param: config_obj: object with configuration.
    :return: flask app.
    """
    app = APP
    app.config.from_object(config_obj)
    return app


class MyTestCase(TestCase):

    """Tests for get, put, delete resources."""

    def create_app(self):
        """:returns flask app."""
        return create_app(TestingConfig)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        field = Field(has_autocomplete=True, has_choice=True,
                      title="edu", is_multichoice=True)
        DB.session.add(field)
        DB.session.commit()
        field = Field.query.filter_by(has_autocomplete=True, has_choice=True,
                                      title="edu", is_multichoice=True).first()
        self.field_id = field.id
        choice1 = Choice(title="LNU", field_id=self.field_id)
        choice2 = Choice(title="LP", field_id=self.field_id)
        DB.session.add(choice1)
        DB.session.add(choice2)
        DB.session.commit()
        id1 = Choice.query.filter_by(field_id=self.field_id, title="LNU").first()
        self.choice_id1 = id1.id
        id2 = Choice.query.filter_by(field_id=self.field_id, title="LP").first()
        self.choice_id2 = id2.id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/field/{}'.format(self.field_id))
            check = {
                "has_autocomplete": True,
                "has_choice": True,
                "title": "edu",
                "is_multichoice": True,
                "id": self.field_id,
                "choices": [
                    {
                        "id": self.choice_id1,
                        "title": "LNU",
                        "field_id": self.field_id
                    },
                    {
                        "id": self.choice_id2,
                        "title": "LP",
                        "field_id": self.field_id
                    }
                ]
            }
            self.assertEqual(response.json, check)

    def test_put(self):
        """Tests put resource."""
        with self.create_app().test_client() as client:
            new = {
                "has_autocomplete": True,
                "has_choice": True,
                "title": "edu",
                "is_multichoice": False,
                "choices": [
                    {
                        "title": "LNU"
                    },
                    {
                        "title": "LP"
                    }
                ]
            }
            client.put('/field/{}'.format(self.field_id), json=new)
            field = Field.query.filter_by(id=self.field_id).first()
            self.assertEqual(field.is_multichoice, False)

    def test_delete(self):
        """Tests delete resource."""
        with self.create_app().test_client() as client:
            response = client.delete('/field/{}'.format(self.field_id))
            field = Field.query.filter_by(id=self.field_id).first()
            choice1 = Choice.query.filter_by(id=self.choice_id1).first()
            choice2 = Choice.query.filter_by(id=self.choice_id2).first()
            self.assertEqual(field, None)
            self.assertEqual(choice1, None)
            self.assertEqual(choice2, None)
            self.assertEqual(response.status_code, 200)


class PostTest(TestCase):

    """Tests for post resource."""

    def create_app(self):
        """:returns flask app."""
        return create_app(TestingConfig)

    def setUp(self):
        """Creates tables."""
        DB.create_all()

    def test_post_success(self):
        """Tests post resource success."""
        with self.create_app().test_client() as client:
            response = client.post('/field',
                                   json={"has_autocomplete": True, "has_choice": False,
                                         "title": "edu", "is_multichoice": True})
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()


class GetTitlesTest(TestCase):

    """Tests for post resource."""

    def create_app(self):
        """:returns flask app."""
        return create_app(TestingConfig)

    def setUp(self):
        """Creates tables."""
        DB.create_all()
        field1 = Field(has_autocomplete=True, has_choice=False,
                       title="edu", is_multichoice=True)
        field2 = Field(has_autocomplete=True, has_choice=False,
                       title="name", is_multichoice=True)
        DB.session.add(field1)
        DB.session.add(field2)
        DB.session.commit()

    def test_get(self):
        """Tests PostAPI get method."""
        with self.create_app().test_client() as client:
            response = client.get('/field?field_id=1&field_id=2',)
            check = {"1": "edu", "2": "name"}
            self.assertEqual(response.json, check)

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()


if __name__ == '__main__':
    main()
