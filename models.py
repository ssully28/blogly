"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
