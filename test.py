
from app import app
from unittest import TestCase
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
connect_db(app)
db.create_all()
User.query.delete()

# Add test-users to blogly_test
whiskey = User(user_name='whisky-test', first_name='Whiskey', last_name="dog")
bowser = User(user_name='bowser-test', first_name='Bowser', last_name="dog")
spike = User(user_name='spike-test', first_name='Spike', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()



class FlaskTests(TestCase):


    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        """ test users are displayed on /users """

        with self.client:
            result = self.client.get('/users')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1 class="col-2">Users</h1>', result.data)

    def test_root(self):
        """ test root route redirects to /users """

        with self.client:
            result = self.client.get('/', follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1 class="col-2">Users</h1>', result.data)

    def test_add_form(self):
        """ test that add user form is accessible """

        with self.client:
            result = self.client.get('/users/new')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1 class="display-5 mt-4">Create a user</h1>', result.data)

    def test_user_profile(self):
        """ test that user profile is accessible """

        with self.client:
            result = self.client.get('/users/whisky-test')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h1 class="display-4">\n            whisky-test\n        </h1>', result.data)

    def test_add_user(self):
        """ testing post request to add user to database """

        with self.client:
            result = self.client.post('/users', data={
                "user-name": "cool-guy-johnny-B",
                "first-name": "johnny",
                "last-name": "bravo",
                "image-url": "https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/06/25/14/cat-lizard.jpg"
            }, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h5 class="card-title">cool-guy-johnny-B</h5>',
                                        result.data)
    
    def test_delete_user(self):
        """ testing post request to delete user from database """

        with self.client:
            result = self.client.post('/users/bowser-test/delete',
                                        follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertNotIn(b'bowser-test', result.data)
