# test_home.py
from test.test_base import BaseTestCase
import unittest
from flask import current_app, url_for

class TestIndexHtml(BaseTestCase):

    """Check if page exists and loads correctly"""
    def test_okStatus(self):
        with current_app.test_client(self) as tester:
            response = tester.get('/')
            self.assertTrue('200', response.status_code)

if __name__ == "__main__":
    unittest.main()
