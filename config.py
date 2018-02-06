import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	#MONGOALCHEMY_DATABASE = 'MockMongo'
	MONGO_URI = 'mongodb://35.196.89.178:80/myflix'
#	MONGO_DBNAME = 'myflix'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

