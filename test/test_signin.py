# test_signin.py
from test.test_base import BaseTestCase
import unittest
from flask import current_app, url_for


class TestIndexHtml(BaseTestCase):

    """Check if page exists and loads correctly"""
    def test_okStatus(self):
        with current_app.test_client(self) as tester:
            response = tester.get('/signin')
            self.assertTrue('200', response.status_code)

    """Test for Signin Fields"""
    def test_signinForm(self):
        with current_app.test_client(self) as tester:
            response = tester.get('/signin')

            self.assertTrue('username' in response.get_data(as_text=True))
            self.assertTrue('password' in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
