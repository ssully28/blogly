"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
# db.create_all()


@app.route('/')
def root_route():
    return redirect('/users')


@app.route('/users', methods=['GET', 'POST'])
def home_route():

    if request.method == 'POST':
        user_name = request.form.get('user-name')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        image_url = request.form.get('image-url')

        user = User(user_name=user_name, first_name=first_name,
                    last_name=last_name, image_url=image_url)

        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        users = User.query.all()
        return render_template('users.html', users=users)


@app.route('/users/new')
def add_user():
    return render_template('add_user.html')
