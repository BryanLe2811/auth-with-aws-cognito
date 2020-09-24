import unittest
from app import db
from app.models import User
from test.test_base import BaseTestCase


class ModelCase(BaseTestCase):

    # Test to create new database and be able to query it
    def test_User(self):
        user = User(username="testname", useremail="testname@gmail.com")
        db.session.add(user)
        db.session.commit()
        user1 = User.query.filter_by(username="testname").first()
        self.assertEqual(user.id, user1.id)


if __name__ == '__main__':
    unittest.main()
