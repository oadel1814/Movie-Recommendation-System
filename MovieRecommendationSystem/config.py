import os

# expose module-level settings so imports like `from config import SQLALCHEMY_DATABASE_URI` work
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///movies.db")

class Config:
    # -----------------------
    # Flask Configuration
    # -----------------------
    # Secret key for sessions, forms, etc.
    SECRET_KEY = SECRET_KEY

    # -----------------------
    # Database Configuration
    # -----------------------
    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    # -----------------------
    # TMDB API Configuration
    # -----------------------
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or 'your_tmdb_api_key_here'
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

    # -----------------------
    # Pagination Configuration
    # -----------------------
    MOVIES_PER_PAGE = 20

    # -----------------------
    # Recommendations Configuration
    # -----------------------
    TOP_N_RECOMMENDATIONS = 10

# Optional: separate config classes for different environments
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # In production, SECRET_KEY should be set via environment variable
