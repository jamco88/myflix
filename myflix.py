from app import app, db, mongo
from app.models import User, Ratings

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Ratings': Ratings}