from models import User, db
from app import app

db.create_all()

User.query.delete()

# Add pets
whiskey = User(user_name='whisky-alpha', first_name='Whiskey', last_name="dog")
bowser = User(user_name='bowser-bravo', first_name='Bowser', last_name="dog")
spike = User(user_name='spike-sierra', first_name='Spike', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()