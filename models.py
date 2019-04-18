"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import time

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_name = db.Column(db.String(25),
                          nullable=False,
                          unique=True)
    first_name = db.Column(db.String(25),
                 nullable=False)
    last_name = db.Column(db.String(25),
                 nullable=False)
    image_url = db.Column(db.String(),
                default='http://maestroselectronics.com/wp-content/uploads/bfi_thumb/blank-user-355ba8nijgtrgca9vdzuv4.jpg')

    def __repr__(self):
        return f"<User {self.id} {self.user_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ table of blog posts, each with title, content, creator, and created at """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100),
                          nullable=False,
                          unique=False)
    
    content = db.Column(db.Text,
                 nullable=False)
    
    date_created = db.Column(db.DateTime,
                 nullable=False,
                 default=datetime.utcnow)
    
    user_name = db.Column(db.String(25),
                        db.ForeignKey('users.user_name'))
    
    user = db.relationship('User')
