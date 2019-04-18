
from app import app
from unittest import TestCase
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
connect_db(app)

db.create_all()

Post.query.delete()
User.query.delete()

# Add test-users to blogly_test
whiskey = User(user_name='whisky-test', first_name='Whiskey', last_name="dog")
bowser = User(user_name='bowser-test', first_name='Bowser', last_name="dog")
spike = User(user_name='spike-test', first_name='Spike', last_name="porcupine")

# Add test posts to test-db
post1 = Post(title='test 1 title', content='''Normally, both your asses would be dead as fucking fried chicken, but you happen to pull this shit while I''m in a transitional period so I don''t wanna kill you, I wanna help you. But I can''t give you this case, it don''t belong to me. Besides, I''ve already been through too much shit this morning over this case to hand it over to your dumb ass.
''', user_name='whisky-test')
post2 = Post(title='test 2 title', content='''Now that we know who you are, I know who I am. I''m not a mistake! It all makes sense! In a comic, you know how you can tell who the arch-villain''s going to be? He''s the exact opposite of the hero. And most times they''re friends, like you and me! I should''ve known way back when... You know why, David? Because of the kids. They called me Mr Glass.'''
, user_name='bowser-test')
post3 = Post(title='test 3 title', content='''The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of darkness, for he is truly his brother''s keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who would attempt to poison and destroy My brothers. And you will know My name is the Lord when I lay My vengeance upon thee.
''', user_name='spike-test')
post4 = Post(title='test edit before', content='content edit before', user_name='spike-test')

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

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
            result = self.client.post('/users/cool-guy-johnny-B/delete',
                                        follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertNotIn(b'cool-guy-johnny-B', result.data)

    def test_posts_page(self):
        """ testing test posts show up on the page """

        with self.client:
            result = self.client.get('/posts')
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'<h5 class="card-title title-preview">test 1 title</h5>', result.data)

    def test_create_post(self):
        """ testing blog post creation """
        with self.client:
            result = self.client.post('/users/spike-test/posts', data={
                "post-title": "autotest title",
                "post-content": "autotest content for blog post testing"
            }, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'autotest title', result.data)

    def test_edit_post(self):
        """Testing blog edit """
        with self.client:
            result = self.client.post('/posts/8/edit', data={
                "post-title": "UPDATED Title",
                "post-content": "UPDATED Content"
            }, follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'UPDATED Title', result.data)
            self.assertIn(b'UPDATED Content', result.data)
    