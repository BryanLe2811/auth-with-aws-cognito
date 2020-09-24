import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_testing import TestCase
from app import create_app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()