import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl_pipeline.extract import (
    fetch_popular_movies, 
    fetch_top_rated_movies,
    fetch_movies_from_kaggle,
    fetch_movies_from_csv
)
from etl_pipeline.transform import transform_movies
from etl_pipeline.load import load_movies_to_db
from config import Config
from flask import Flask
from database.db import db, init_db

def run_etl_pipeline(source='tmdb', pages=5, **kwargs):
    """
    Run the complete ETL pipeline from different data sources.
    
    Parameters:
    -----------
    source : str
        Data source: 'tmdb', 'kaggle', or 'csv'
    pages : int
        Number of pages to fetch (for TMDB API)
    **kwargs : dict
        Additional arguments:
        - For 'kaggle': dataset_name, csv_file_name
        - For 'csv': csv_path
    
    Examples:
    ---------
    # From TMDB API
    run_etl_pipeline(source='tmdb', pages=10)
    
    # From Kaggle dataset
    run_etl_pipeline(
        source='kaggle',
        dataset_name='tmdb-movie-metadata',
        csv_file_name='tmdb_5000_movies.csv'
    )
    
    # From local CSV file
    run_etl_pipeline(source='csv', csv_path='movies.csv')
    """
    print("="*50)
    print("Starting ETL Pipeline")
    print(f"Data Source: {source.upper()}")
    print("="*50)
    
    # Initialize Flask app for database context
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Extract
    print(f"\n[1/3] EXTRACTING DATA FROM {source.upper()}...")
    all_movies = []
    
    if source.lower() == 'tmdb':
        api_key = Config.TMDB_API_KEY
        
        if not api_key or api_key == 'your_tmdb_api_key_here':
            print("ERROR: Please set your TMDB API key in config.py or environment variable")
            return
        
        popular_movies = fetch_popular_movies(api_key, pages=pages)
        top_rated_movies = fetch_top_rated_movies(api_key, pages=3)
        all_movies = popular_movies + top_rated_movies
    
    elif source.lower() == 'kaggle':
        dataset_name = kwargs.get('dataset_name', 'tmdb-movie-metadata')
        csv_file_name = kwargs.get('csv_file_name', 'tmdb_5000_movies.csv')
        all_movies = fetch_movies_from_kaggle(dataset_name, csv_file_name)
    
    elif source.lower() == 'csv':
        csv_path = kwargs.get('csv_path', 'movies.csv')
        all_movies = fetch_movies_from_csv(csv_path)
    
    else:
        print(f"ERROR: Unknown source '{source}'. Use 'tmdb', 'kaggle', or 'csv'")
        return
    
    if not all_movies:
        print("ERROR: No movies extracted. Check your data source configuration.")
        return
    
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
    # TMDB 5000 Movie Dataset - High Quality Real Data
    # Uncomment the desired source:
    
    # Option 1: TMDB API (requires TMDB_API_KEY environment variable)
    # run_etl_pipeline(source='tmdb', pages=10)
    
    # Option 2: TMDB 5000 Dataset (RECOMMENDED - Real TMDB data with 5000 movies)
    run_etl_pipeline(source='csv', csv_path='tmdb_5000_movies.csv')
    
    # Option 3: Large local CSV file with 600+ generated movies
    # run_etl_pipeline(source='csv', csv_path='large_movies.csv')
    
    # Option 4: Kaggle dataset - 5000+ movies (requires setup_kaggle.py first)
    # run_etl_pipeline(
    #     source='kaggle',
    #     dataset_name='tmdb/tmdb-movie-metadata',
    #     csv_file_name='tmdb_5000_movies.csv'
    # )