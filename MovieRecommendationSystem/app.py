from flask import Flask, g
from flask_login import LoginManager
from config import Config
from database.db import init_db,db
from database.models import User, Movie
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.user import user_bp
from recommender.engine import RecommendationEngine

def get_recommendation_engine():
    """Get the recommendation engine, initializing if needed."""
    if 'recommendation_engine' not in g:
        try:
            movies = Movie.query.all()
            if movies:
                g.recommendation_engine = RecommendationEngine(movies=movies)
            else:
                g.recommendation_engine = None
        except Exception as e:
            print(f"Error getting recommendation engine: {e}")
            g.recommendation_engine = None
    return g.recommendation_engine

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(user_bp)
    
    # Template filters
    @app.template_filter('poster_url')
    def poster_url(poster_path):
        if poster_path:
            # If it's already a full URL, return as is
            if poster_path.startswith('http'):
                return poster_path
            # Otherwise, prepend the TMDB base URL
            return f"{Config.TMDB_IMAGE_BASE_URL}{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"
    
    @app.template_filter('backdrop_url')
    def backdrop_url(backdrop_path):
        if backdrop_path:
            # If it's already a full URL, return as is
            if backdrop_path.startswith('http'):
                return backdrop_path
            # Otherwise, prepend the TMDB base URL
            return f"{Config.TMDB_IMAGE_BASE_URL}{backdrop_path}"
        return "https://via.placeholder.com/1280x720?text=No+Backdrop"
    
    # Make recommendation engine available in templates
    @app.context_processor
    def inject_recommendation_engine():
        return {'get_recommendation_engine': get_recommendation_engine}
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)