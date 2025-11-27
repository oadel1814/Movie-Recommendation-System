from database.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    watchlist = db.relationship('Watchlist', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    overview = db.Column(db.Text)
    genres = db.Column(db.String(200))
    release_date = db.Column(db.String(20))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    popularity = db.Column(db.Float)
    poster_path = db.Column(db.String(200))
    backdrop_path = db.Column(db.String(200))
    original_language = db.Column(db.String(10))
    
    # For recommendation engine
    combined_features = db.Column(db.Text)
    
    watchlist_entries = db.relationship('Watchlist', backref='movie', lazy=True)
    
    def __repr__(self):
        return f'<Movie {self.title}>'

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False, index=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    watched = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)
    
    def __repr__(self):
        return f'<Watchlist User:{self.user_id} Movie:{self.movie_id}>'