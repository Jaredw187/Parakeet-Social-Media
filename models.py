# List of Imports.
from init import app, db

#######################################
# Need to define database models here #
#######################################


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(30))
    # NEED TO ADD PICTURE  avatar = ?
    # NO WE DON'T. Don't lie.
    photo = db.Column(db.BLOB)
    photo_type = db.Column(db.String(50))
    pw_hash = db.Column(db.String(64))


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    initiator = db.Column(db.Integer, db.ForeignKey('user.id'))
    respondent = db.Column(db.Integer, db.ForeignKey('user.id'))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(256)) # max message size is 256 per Ekstrand's requirements
    sender = db.Column(db.String(50))
    recipient = db.Column(db.String(50))
    time_stamp = db.Column(db.DATETIME)
    photo = db.Column(db.BLOB)
    photo_type = db.Column(db.String(50))

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50)) # the person being followed
    person_follow = db.Column(db.String(50)) # the person doing the following

db.create_all(app=app)