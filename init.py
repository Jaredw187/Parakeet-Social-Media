# List of Imports.
import flask
import flask_sqlalchemy
from flask_socketio import SocketIO

# Make an app out of our flask application.
app = flask.Flask(__name__)

# Define our configuration file.
app.config.from_pyfile('settings.py')

# Define our database using SQL Alchemy.
db = flask_sqlalchemy.SQLAlchemy(app)

# make dem sockets.
socketio = SocketIO(app)

recip_sockets = {}
