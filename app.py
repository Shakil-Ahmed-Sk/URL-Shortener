# Import necessary modules from Flask and extensions
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import string
import json
from config import Config  # Import configuration settings

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User model for database
class User(UserMixin, db.Model):
    # Define columns for User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    urls = db.relationship("URL", back_populates="user")

# Define URL model for database
class URL(db.Model):
    # Define columns for URL model
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, nullable=False)
    short_url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=True)
    click_count = db.Column(db.Integer, default=0)
    referrers = db.Column(db.Text, default='{}')
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="urls")

# Loader function to load user by ID for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to generate short URL based on ID
def generate_short_url(id):
    characters = string.ascii_letters + string.digits
    base = len(characters)
    short_url = ''
    while id > 0:
        val = id % base
        short_url = characters[val] + short_url
        id = id // base
    return short_url

# Function to insert URL into database and generate short URL
def insert_url(long_url, title=None):
    new_url = URL(long_url=long_url, short_url='', title=title, user_id=current_user.id)
    db.session.add(new_url)
    db.session.commit()
    short_url = generate_short_url(new_url.id)
    new_url.short_url = short_url
    db.session.commit()
    return new_url.id

# Function to get long URL from short URL
def get_long_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return url.long_url
    else:
        return None

# Route for home page where users can shorten URLs
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        title = request.form.get('title')
        id = insert_url(long_url, title)
        url = URL.query.get(id)
        return render_template('index.html', short_url=url.short_url)
    return render_template('index.html')

# Route for dashboard displaying analytics for user's shortened URLs
@app.route('/dashboard')
@login_required
def dashboard():
    user_urls = URL.query.filter_by(user_id=current_user.id).all()
    urls_with_analytics = [
        (url.long_url, url.short_url, url.title, url.click_count, json.loads(url.referrers) if url.referrers else {}, url.timestamp)
        for url in user_urls
    ]
    return render_template('dashboard.html', urls_with_analytics=urls_with_analytics)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Route for user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            phone_number=phone_number, 
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Signup successful.')
        return redirect(url_for('index'))
    return render_template('signup.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

# Route for user profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Route for redirecting short URLs to long URLs
@app.route('/<short_url>')
def redirect_short_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        url = URL.query.filter_by(short_url=short_url).first()
        url.click_count += 1
        referrer = request.referrer or 'direct'
        referrers = json.loads(url.referrers) if url.referrers else {}
        referrers[referrer] = referrers.get(referrer, 0) + 1
        url.referrers = json.dumps(referrers)
        db.session.commit()
        return redirect(long_url)
    else:
        return 'URL not found', 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
