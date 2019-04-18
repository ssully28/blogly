from models import User, db, Post
from app import app

db.create_all()

User.query.delete()

# Add users
whiskey = User(user_name='whisky-alpha', first_name='Whiskey', last_name="dog")
bowser = User(user_name='bowser-bravo', first_name='Bowser', last_name="dog")
spike = User(user_name='spike-sierra', first_name='Spike', last_name="porcupine")
# Add posts
post1 = Post(title='post 1 title', content='HERE IS SOME CONTENT FOR POST 1', user_name='whisky-alpha')
post2 = Post(title='post 2 title', content='HERE IS SOME CONTENT FOR POST 2', user_name='bowser-bravo')
post3 = Post(title='post 3 title', content='HERE IS SOME CONTENT FOR POST 3', user_name='spike-sierra')

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# Commit--otherwise, this never gets saved!
db.session.commit()