from init import app
SECRET_KEY = '98765463ghjdfsyghb3467HUIYTI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'