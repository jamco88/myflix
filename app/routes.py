from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, mongo
from app.forms import LoginForm, RegistrationForm, ReviewForm
from app.models import User, Ratings
from bson.objectid import ObjectId
import csv

@app.route('/')
@app.route('/index')
@login_required
def index():
    mockfilms = [
	{
		'oid' : '5a0daaafaa70db3d0a1c5e1a',
		'filmname' : 'Big Buck Bunny',
		'image' : 'https://goo.gl/K3QtXN',
		'video' : 'http://35.227.70.148',
		'reviewurl' : 'http://127.0.0.1:5000/review/5a0daaafaa70db3d0a1c5e1a'
	},
	{
		'oid' : '5a0daaafaa70db3d0a1c5e1e',
		'filmname' : 'Starting Erlang',
		'image' : 'https://image.tmdb.org/t/p/w640/gaTzTIxT5Cio3eeoOXX5zixn89V.jpg',
		'video' : 'http://www.youtube.com/watch?v=6maL6gq6qME&t=0m20s',
		'reviewurl' : 'http://127.0.0.1:5000/review/5a0daaafaa70db3d0a1c5e1e'
	},
	{
		'oid' : '5a0daaafaa70db3d0a1c5e1d',
		'filmname' : 'Running cassandra on a pc',
		'image' : 'https://image.tmdb.org/t/p/w640/90T7b2LIrL07ndYQBmSm09yqVEH.jpg',
		'video': 'https://www.youtube.com/watch?v=I4NFIBaHnl4',
		'reviewurl' : 'http://127.0.0.1:5000/review/5a0daaafaa70db3d0a1c5e1d' 
	},
	{
		'oid' : '5a0daaafaa70db3d0a1c5e1c',
		'filmname' : 'Installing and starting cassandra on a mac',
		'image' : 'https://image.tmdb.org/t/p/w640/x4jEa65IzQu5MRbIyBtucd11B8e.jpg',
		'video' : 'https://www.youtube.com/watch?v=dqOjaiFP6gQ',
		'reviewurl' : 'http://127.0.0.1:5000/review/5a0daaafaa70db3d0a1c5e1c'
	},
	{
		'oid' : '5a0daaafaa70db3d0a1c5e1b',
		'filmname' : 'Cloning a project into netbeans',
		'image' : 'http://4.bp.blogspot.com/-x2p09_WXnz0/TzPp9j0T4-I/AAAAAAAABCk/Z0UaGNZtXZI/s1600/Rashomon.jpg',
		'video' : 'https://www.youtube.com/watch?v=ankoam7pqck',
		'reviewurl' : 'http://127.0.0.1:5000/review/5a0daaafaa70db3d0a1c5e1b'
	}		
	]	
    return render_template('index.html', title='Home Page', mockfilms=mockfilms)

@app.route('/review/<ID>', methods = ['GET', 'POST'])
@login_required
def review(ID):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Ratings(User_id = current_user.id, Score_given = form.score.data, Film_id = ID)
        db.session.add(review)
        db.session.commit()
        f = open('ratings.csv', 'w')
        out = csv.writer(f)
        out.writerow(['User_id', 'Film_id', 'Score_given'])
        for item in Ratings.query.all():
        	out.writerow([item.User_id, item.Film_id, item.Score_given])
        f.close()
        flash('Review DB updated - Thanks for your review!')
        return redirect(url_for('index'))
    return render_template('review.html', title='Review Page', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


##@app.route('/recommended for you!')
#@login_required
#	def recommendedforyou():
#		if 

#creates a route for the info page for each video. This will pass in the film
#'s entry so that the description, category etc are available to use in the info template html.'
@app.route('/info/<ID>')
def info(ID):
	searchid = ObjectId(ID)
	videos = mongo.db.videos
	record = videos.find_one_or_404({'_id': searchid})
	film = record['video']['Name']
	category = record['video']['category']
	return render_template('info.html', film=film, category=category)

#http://127.0.0.1:5000/info/5a0daaafaa70db3d0a1c5e1a


