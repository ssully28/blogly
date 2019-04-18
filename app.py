"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


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
        if image_url == "":
            image_url = None
        user = User(user_name=user_name, first_name=first_name,
                    last_name=last_name, image_url=image_url)

        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        users = User.query.order_by('last_name').all()
        return render_template('users.html', users=users)


@app.route('/posts')
def posts():
    # posts = Post.query.order_by('date_created').all()
    posts = db.session.query(Post.title,
                                Post.content,
                                Post.date_created,
                                User.user_name,
                                Post.id).join(User).all()

    return render_template('posts.html', posts=posts)


@app.route('/posts/<post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).one_or_none()
    if post == None:
        return redirect ('/')
    else:
        return render_template('show_post.html', post=post)


@app.route('/users/new')
def add_user():
    return render_template('add_user.html')


@app.route('/users/<user_name>')
def user_profile(user_name):
    user = User.query.filter_by(user_name=user_name).one_or_none()
    user_posts = Post.query.filter_by(user_name = user_name).all()
    if user == None:
        return redirect('/')
    else:
        return render_template('profile.html',
                            user=user, posts=user_posts)


@app.route('/users/<user_name>/edit', methods=["GET", "POST"])
def edit_user(user_name):
    user = User.query.filter_by(user_name=user_name).one_or_none()

    if request.method == "POST":
        user.first_name = request.form.get('first-name')
        user.last_name = request.form.get('last-name')
        user.image_url = request.form.get('image-url')
        if user.image_url == "":
            user.image_url = "http://maestroselectronics.com/wp-content/uploads/bfi_thumb/blank-user-355ba8nijgtrgca9vdzuv4.jpg"

        # user = User(user_name=user_name, first_name=first_name,
        #             last_name=last_name, image_url=image_url)

        db.session.commit()

        return redirect(f'/users/{user_name}')
    else:
        return render_template('edit_user.html', user=user)


@app.route('/users/<user_name>/delete', methods=["POST"])
def delete_user(user_name):
    user = User.query.filter_by(user_name=user_name).one_or_none()
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_name>/posts', methods=["POST"])
def add_post(user_name):
    title = request.form.get('post-title')
    content = request.form.get('post-content')
    post = Post(title=title, content=content, user_name=user_name)

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_name}')


@app.route('/users/<user_name>/posts/new')
def submit_post_form(user_name):
    return render_template('create_post.html', user_name=user_name)
