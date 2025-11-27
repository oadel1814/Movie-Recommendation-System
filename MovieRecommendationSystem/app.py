from flask import Flask
from flask_login import LoginManager
from config import Config
from database.db import init_db,db
from database.models import User, Movie
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.user import user_bp
from recommender.engine import RecommendationEngine

# Initialize recommendation engine globally
recommendation_engine = None

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
            return f"{Config.TMDB_IMAGE_BASE_URL}{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"
    
    @app.template_filter('backdrop_url')
    def backdrop_url(backdrop_path):
        if backdrop_path:
            return f"{Config.TMDB_IMAGE_BASE_URL}{backdrop_path}"
        return "https://via.placeholder.com/1280x720?text=No+Backdrop"
    
    # Initialize recommendation engine after first request
    @app.before_request
    def initialize_recommendation_engine():
        global recommendation_engine
        if recommendation_engine is None:
            try:
                movies = Movie.query.all()
                if movies:
                    recommendation_engine = RecommendationEngine()
                    recommendation_engine.build(movies)
                    print("Recommendation engine initialized")
            except Exception as e:
                print(f"Error initializing recommendation engine: {e}")
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)