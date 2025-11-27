import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl_pipeline.extract import fetch_popular_movies, fetch_top_rated_movies
from etl_pipeline.transform import transform_movies
from etl_pipeline.load import load_movies_to_db
from config import Config
from flask import Flask
from database.db import db, init_db

def run_etl_pipeline(pages=5):
    """Run the complete ETL pipeline"""
    print("="*50)
    print("Starting ETL Pipeline")
    print("="*50)
    
    # Initialize Flask app for database context
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Extract
    print("\n[1/3] EXTRACTING DATA FROM TMDB...")
    api_key = Config.TMDB_API_KEY
    
    if not api_key or api_key == 'your_tmdb_api_key_here':
        print("ERROR: Please set your TMDB API key in config.py or environment variable")
        return
    
    popular_movies = fetch_popular_movies(api_key, pages=pages)
    top_rated_movies = fetch_top_rated_movies(api_key, pages=3)
    
    all_movies = popular_movies + top_rated_movies
    print(f"Total movies extracted: {len(all_movies)}")
    
    # Transform
    print("\n[2/3] TRANSFORMING DATA...")
    transformed_df = transform_movies(all_movies)
    
    # Load
    print("\n[3/3] LOADING DATA TO DATABASE...")
    inserted, updated = load_movies_to_db(transformed_df, app)
    
    print("\n" + "="*50)
    print("ETL Pipeline Complete!")
    print(f"Total movies in database: {inserted + updated}")
    print("="*50)

if __name__ == '__main__':
    run_etl_pipeline(pages=10)