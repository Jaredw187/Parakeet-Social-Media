# List of Imports.
import flask
from init import app, db
import models

# This file contains ALL of the Javascript being used in
# the project. Including their @app.routes.


@app.route('/api/follow', methods=['POST'])
def follower():
    # receive values from javascript
    follower = flask.request.form['follower']
    user = flask.request.form['user']

    # check to see if auth user / csrf token are valid
    if 'auth_user' not in flask.session:
        flask.abort(403)
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        flask.abort(400)

    has_relation = models.Follow.query.filter_by(person_follow=follower, user=user).first()
    # if the realation exists.. we don't want another.
    if has_relation is not None:
        return flask.jsonify({'result': 'already-followed'})
    # if it doesn't.. we should probably make one.
    else:
        follow_relation = models.Follow()
        follow_relation.user = user
        follow_relation.person_follow = follower

        db.session.add(follow_relation)
        db.session.commit()

    return flask.jsonify({'result': 'ok'})


@app.route('/api/unfollow', methods=['POST'])
def unfollow():
    # receive values from javascript
    follower = flask.request.form['follower']
    user = flask.request.form['user']

    # check to see if auth user / csrf token are valid
    if 'auth_user' not in flask.session:
        flask.abort(403)
    if flask.request.form['_csrf_token'] != flask.session['csrf_token']:
        flask.abort(400)

    print(follower, "attempted to unfollow ", user)
    has_relation = models.Follow.query.filter_by(person_follow=follower, user=user).first()

    # if we have a relationship.. delete it.
    if has_relation is not None:
        print("el-deleto realtionship")
        db.session.delete(has_relation)
        db.session.commit()

    else:
        print("realationship didn't exist.. so were gonna do nothing..")
        return flask.jsonify({'result': 'nothing-done'})

    return flask.jsonify({'result': 'ok'})
