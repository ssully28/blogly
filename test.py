
from app import app
from unittest import TestCase

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        with self.client:
            result = self.client.get('/users')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1>Users</h1>', result.data)

    def test_root(self):
        with self.client:
            result = self.client.get('/', follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1>Users</h1>', result.data)

    def test_add_form(self):
        with self.client:
            result = self.client.get('/users/new')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1>Create a user</h1>', result.data)
