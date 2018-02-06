from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap
#from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo  

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#mdb = MongoAlchemy(app)
mongo = PyMongo(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models