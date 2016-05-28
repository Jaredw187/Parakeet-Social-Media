# List of Imports
from init import app, db
import flask
import os
import base64
import bcrypt
import models
import string
import io
from markupsafe import Markup
import markdown



# Define global name of site.
# I am going to use a Parakeet as the basis for the logo for this project. The thinking being
# that "Twitter" is based off of a bird too, so I'm going to follow suit, hence "Para-keet".
site_title = "Para-keet"


# Create a CSRF Token before the user visits the site.
@app.before_request
def setup_csrf():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = base64.b64encode(os.urandom(32)).decode('ascii')


# Create / Check if a verified user is accessing the site.
@app.before_request
def setup_user():
    # Figure out if we have an authorized user, and look them up.
    # This runs for every request, so we don't have to duplicate code.
    if 'auth_user' in flask.session:
        user = models.User.query.get(flask.session['auth_user'])
        if user is None:
            # old bad cookie, no good
            del flask.session['auth_user']
        # Save the user in flask.g, which is a set of globals for this request.
        flask.g.user = user


@app.route('/')
def index():
    # Name the page being displayed.
    page_title = 'Home'

    # display latest 20 messages from users followers
    # 1) get his followers
    # 2) get the message
    # 3) take care of the rest in jinja.
    if 'auth_user' in flask.session:
        i_follow = models.Follow.query.filter_by(person_follow=flask.g.user.login).all()
        messages = models.Message.query.order_by(models.Message.time_stamp.desc()).all()
    else:
        messages = models.Message.query.order_by(models.Message.time_stamp.desc()).all()
        i_follow = None

    users = models.User.query.all()

    myList = []
    message_content = []
    myList.append(messages)

    for msg in messages:
        myList.append(msg.message)
        my_content = Markup(markdown.markdown(msg.message))
        message_content.append(my_content)



    # Create a response that will be returned when a user visits the homepage.
    return flask.make_response(flask.render_template('index.html', page_title=page_title, site_title=site_title,
                                                     csrf_token=flask.session['csrf_token'],
                                                     messages=messages, count='', i_follow=i_follow,
                                                     users=users, content=message_content))


@app.route('/login')
def login_form():
    # GET request to /login - send the login form
    page_title = "Login"
    return flask.render_template('login.html', page_title=page_title, site_title=site_title)


@app.route('/login', methods=['POST'])
def handle_login():
    page_title = "Login"
    # POST request to /login - check user
    login = flask.request.form['user']
    password = flask.request.form['password']
    # try to find user
    user = models.User.query.filter_by(login=login).first()
    if user is not None:
        # hash the password the user gave us
        # for verifying, we use their real hash as the salt
        pw_hash = bcrypt.hashpw(password.encode('utf8'), user.pw_hash)
        # is it good?
        if pw_hash == user.pw_hash:
            # yay!
            flask.session['auth_user'] = user.id
            # And redirect to '/', since this is a successful POST
            return flask.redirect(flask.url_for('view_user', user=login))

    # if we got this far, either username or password is no good
    # For an error in POST, we'll just re-show the form with an error message
    return flask.render_template('login.html', state='bad', page_title=page_title, site_title=site_title)


@app.route('/u/<string:user>')
def view_user(user):
    if not 'auth_user' in flask.session:
        return flask.redirect(flask.url_for('index'))

    page_title = "{}'s Profile".format(string.capwords(user))
    user_profile = models.User.query.filter_by(login=user).first()
    # get all this dewds followers
    followers = models.Follow.query.filter_by(user=user).all()
    # search for a relationship between current user & profile that we're viewing
    is_follower = models.Follow.query.filter_by(person_follow=flask.g.user.login, user=user_profile.login).first()
    # query the messages unique the the owner of the profile!
    messages = models.Message.query.filter(models.Message.sender == user).order_by(
                                               models.Message.time_stamp.desc()).all()
    myList = []
    message_content = []
    myList.append(messages)

    for msg in messages:
        myList.append(msg.message)
        my_content = Markup(markdown.markdown(msg.message))
        message_content.append(my_content)

    # or_(models.Message.sender == user,
    #     models.Message.recipient == user)

    if is_follower is not None:
        # we have a relationship
        user_is_follower = True
    else:
        # no relationship.. poor guy.
        user_is_follower = False

    if user is not None:
        return flask.render_template('profile.html', page_title=page_title, site_title=site_title,
                                     location=user_profile.location, bio=user_profile.bio, user=user,
                                     photo=user_profile.photo, followers=followers, user_is_follower=user_is_follower,
                                     count=1, messages=messages, content=message_content, content_count=0)
    else:
        print("ERROR TRIED TO VIEW USER PROFILE: USER NOT FOUND")
        print("ID: ", id)
        return flask.redirect(404)


@app.route('/create_new_user')
def create_user_form():
    # GET request to create a new user send to form
    page_title = "Create User"
    return flask.render_template('create_user.html', page_title=page_title, site_title=site_title)


@app.route('/edit_user/<string:user>')
def edit_user(user):
    page_title = "Edit Profile"
    current_user = models.User.query.filter_by(login=user).first()
    if user is not None:
        location = current_user.location
        bio = current_user.bio
        photo = current_user.photo
        return flask.render_template('edit.html', location=location, bio=bio, user=user, page_title=page_title,
                                     site_title=site_title, current_user=current_user)
    else:
        print("ERROR TRIED TO ACCESS USER EDITOR: USER NOT FOUND")
        print("ID: ", id)
        return flask.redirect(404)


# Create Login Handler
@app.route('/create_new_user', methods=['POST'])
def create_user():
    login = flask.request.form['user']

    password = flask.request.form['password']
    bio = flask.request.form['bio']
    location = flask.request.form['location']
    file = flask.request.files['image']
    login_title = "Login"

    # check for invalid characters
    invalid_characters = set('-+=_\'\":;,./<>?!@#$%^&*()`~ ')
    if any((c in invalid_characters)for c in login):
        found = True
    else:
        found = False

    # render the template for invalid character
    if found:
        return flask.render_template('create_user.html', state='invalid-character', page_title=login_title,
                                     site_title=site_title)
    # do the passwords match?
    if password != flask.request.form['confirm']:
        return flask.render_template('create_user.html', state='password-mismatch', page_title=login_title,
                                     site_title=site_title)
    # is the login ok?
    if len(login) > 20:
        return flask.render_template('create_user.html', state='bad-username', page_title=login_title,
                                     site_title=site_title)
    # search for existing user
    existing = models.User.query.filter_by(login=login).first()
    if existing is not None:
        # username already used
        return flask.render_template('create_user.html', state='username-used', page_title=login_title,
                                     site_title=site_title)
    if file:
        if not file.content_type.startswith('image/'):
            flask.abort(400)

    # create user
    user = models.User()
    user.bio = bio
    user.location = location
    user.login = login
    # we'll need to add the picture here most likely
    # hash password
    user.pw_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(15))
    user.photo_type = file.content_type

    # get image data
    photo_data = io.BytesIO()
    file.save(photo_data)
    user.photo = photo_data.getvalue()

    # save user
    db.session.add(user)
    db.session.commit()

    flask.session['auth_user'] = user.id
    return flask.redirect(flask.url_for('view_user', user=login))


@app.route("/update_user_info/<string:user>", methods=['POST'])
def update_user_info(user):

    bio = flask.request.form['updated_bio']
    location = flask.request.form['updated_location']
    print("!")
    file = flask.request.files['image']

    # check that we think the file is an image file, granted a file exists
    if file:
        if not file.mimetype.startswith('image/'):
            # oops
            flask.abort(400)
    print("!")
    # query the user
    current_user = models.User.query.filter_by(login=user).first()

    current_user.bio = bio
    current_user.location = location

    current_user.photo_type = file.mimetype

    # get image data
    photo_data = io.BytesIO()
    file.save(photo_data)
    current_user.photo = photo_data.getvalue()

    db.session.commit()

    return flask.redirect(flask.url_for('view_user', user=user))


@app.route('/view_all_users')
def view_all():
    page_title = "All Users"
    users = models.User.query.all()
    return flask.render_template("view_all.html", users=users, page_title=page_title, site_title=site_title)


@app.route('/post_message/<string:user>', methods=['POST'])
def post_message(user):
    file = flask.request.files['image']

    # check that we think the file is an image file, granted a file exists
    if file:
        if not file.mimetype.startswith('image/'):
            # oops
            flask.abort(400)
    message = flask.request.form['post-text']

    message_content = Markup(markdown.markdown(message, output_format='html5'))


    new_message = models.Message()
    new_message.message = message_content
    new_message.sender = flask.g.user.login
    new_message.recipient = user
    new_message.time_stamp = db.func.now()
    new_message.photo_type = file.mimetype

    photo_data = io.BytesIO()
    file.save(photo_data)
    new_message.photo = photo_data.getvalue()

    # if photo_data is None then no photo
    # need to display just message
    print("sender:", new_message.sender)
    print("recipient:", new_message.recipient)

    db.session.add(new_message)
    db.session.commit()

    return flask.redirect(flask.url_for('view_user', user=user))


# a URL handler to return the photo data for a message
@app.route('/post/<int:message_id>/photo')
def post_photo(message_id):
    post = models.Message.query.get_or_404(message_id)
    if post is not None:
        return post.photo
    else:
        flask.abort(403)


# a URL handler to return the photo data for a user
@app.route('/post/<string:login>/photo_for_user')
def post_user_photo(login):
    user_photo = models.User.query.filter_by(login=login).first()
    if user_photo is not None:
        print("user::::", user_photo.login)
        return user_photo.photo
    else:
        return flask.abort(403)


@app.route('/logout')
def handle_logout():
    # user wants to say goodbye, just forget about them
    del flask.session['auth_user']
    # redirect to specified source URL, or / if none is present
    return flask.redirect(flask.request.args.get('url', '/'))
