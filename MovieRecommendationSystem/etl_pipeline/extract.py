import requests
import time
import pandas as pd
import os
import json
from config import Config

# ==================== TMDB API Methods ====================

def fetch_popular_movies(api_key, pages=5):
    """Fetch popular movies from TMDB API"""
    movies = []
    base_url = f"{Config.TMDB_BASE_URL}/movie/popular"
    
    for page in range(1, pages + 1):
        try:
            print(f"Fetching page {page}...")
            response = requests.get(base_url, params={
                'api_key': api_key,
                'page': page,
                'language': 'en-US'
            })
            response.raise_for_status()
            data = response.json()
            movies.extend(data.get('results', []))
            time.sleep(0.25)  # Rate limiting
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
    
    print(f"Extracted {len(movies)} movies from TMDB")
    return movies

def fetch_movie_details(api_key, movie_id):
    """Fetch detailed information for a specific movie"""
    url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}"
    try:
        response = requests.get(url, params={
            'api_key': api_key,
            'language': 'en-US',
            'append_to_response': 'credits'
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching details for movie {movie_id}: {e}")
        return None

def fetch_top_rated_movies(api_key, pages=3):
    """Fetch top-rated movies from TMDB API"""
    movies = []
    base_url = f"{Config.TMDB_BASE_URL}/movie/top_rated"
    
    for page in range(1, pages + 1):
        try:
            response = requests.get(base_url, params={
                'api_key': api_key,
                'page': page,
                'language': 'en-US'
            })
            response.raise_for_status()
            data = response.json()
            movies.extend(data.get('results', []))
            time.sleep(0.25)
        except Exception as e:
            print(f"Error fetching top rated page {page}: {e}")
            break
    
    return movies

# ==================== Kaggle Dataset Methods ====================

def fetch_movies_from_kaggle(dataset_name, csv_file_name):
    """
    Fetch movies from a Kaggle dataset CSV file.
    
    Prerequisites:
    1. Install kaggle: pip install kaggle
    2. Download kaggle.json from https://www.kaggle.com/settings/account
    3. Place kaggle.json in ~/.kaggle/kaggle.json
    4. Run: kaggle datasets download -d {dataset_name}
    
    Popular movie datasets:
    - 'tmdb-movie-metadata' (tmdb_5000_movies.csv)
    - 'the-movies-dataset' (movies_metadata.csv)
    - 'rotten-tomatoes-movies' (movies.csv)
    """
    try:
        import kaggle
    except ImportError:
        print("ERROR: kaggle library not installed. Install it with: pip install kaggle")
        return []
    
    try:
        # Download dataset if not already present
        dataset_path = f"./{dataset_name.split('/')[-1]}"
        if not os.path.exists(dataset_path):
            print(f"Downloading dataset: {dataset_name}...")
            kaggle.api.dataset_download_files(dataset_name, path='.', unzip=True)
        
        # Load CSV file
        csv_path = os.path.join(dataset_path, csv_file_name) if os.path.isdir(dataset_path) else csv_file_name
        if not os.path.exists(csv_path):
            csv_path = csv_file_name  # Try in current directory
        
        print(f"Loading movies from: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Convert DataFrame to list of dictionaries (similar to TMDB format)
        movies = []
        for _, row in df.iterrows():
            movie = {
                'id': row.get('id') or row.get('movie_id') or row.get('index', len(movies)),
                'title': row.get('title') or row.get('original_title') or 'Unknown',
                'overview': row.get('overview') or row.get('description') or '',
                'genres': row.get('genres') or '',
                'release_date': row.get('release_date') or row.get('release_year') or '',
                'vote_average': float(row.get('vote_average') or row.get('rating') or 0),
                'vote_count': int(row.get('vote_count') or row.get('votes') or 0),
                'popularity': float(row.get('popularity') or 0),
                'poster_path': row.get('poster_path') or '',
                'backdrop_path': row.get('backdrop_path') or '',
                'original_language': row.get('original_language') or row.get('language') or 'en',
            }
            movies.append(movie)
        
        print(f"Extracted {len(movies)} movies from Kaggle dataset")
        return movies
    
    except Exception as e:
        print(f"Error fetching from Kaggle: {e}")
        print("Make sure kaggle.json is installed and dataset is available")
        return []

def fetch_movies_from_csv(csv_path):
    """
    Fetch movies from a local CSV file.
    
    CSV should have columns like:
    - id, title, overview, genres, release_date, vote_average, vote_count, 
      popularity, poster_path, backdrop_path, original_language
    
    Handles both formats:
    - With poster_path/backdrop_path (generated datasets)
    - Without (TMDB 5000 dataset)
    """
    try:
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV file not found: {csv_path}")
            return []
        
        print(f"Loading movies from: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Convert DataFrame to list of dictionaries
        movies = []
        for idx, row in df.iterrows():
            movie_id = row.get('id') or row.get('movie_id') or len(movies)
            title = row.get('title') or row.get('original_title') or 'Unknown'
            
            # Handle poster_path - can be a full URL or a path
            poster_path = row.get('poster_path') or ''
            
            # If no poster_path, generate one using TMDB API pattern or DummyImage
            if not poster_path or pd.isna(poster_path):
                # Use TMDB image API with a default poster
                # Color varies by genre
                colors = ['FF6B6B', 'FFA07A', 'FFD700', 'ADFF2F', '3CB371', '00CED1', '1E90FF', '9370DB', 'FF69B4']
                color = colors[idx % len(colors)]
                poster_path = f"https://dummyimage.com/500x750/{color}/FFFFFF.jpg?text={title.replace(' ', '+')[:30]}"
            
            # If poster_path is just a path (starts with /), prepend TMDB base URL
            if isinstance(poster_path, str) and poster_path.startswith('/'):
                poster_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            
            # Handle backdrop_path similarly
            backdrop_path = row.get('backdrop_path') or ''
            if not backdrop_path or pd.isna(backdrop_path):
                colors = ['FF6B6B', 'FFA07A', 'FFD700', 'ADFF2F', '3CB371', '00CED1', '1E90FF', '9370DB', 'FF69B4']
                color = colors[idx % len(colors)]
                backdrop_path = f"https://dummyimage.com/1280x720/{color}/FFFFFF.jpg?text={title.replace(' ', '+')[:30]}"
            elif isinstance(backdrop_path, str) and backdrop_path.startswith('/'):
                backdrop_path = f"https://image.tmdb.org/t/p/w1280{backdrop_path}"
            
            # Parse genres - handle JSON format
            genres = ''
            raw_genres = row.get('genres') or ''
            if raw_genres and not pd.isna(raw_genres):
                try:
                    if isinstance(raw_genres, str):
                        if raw_genres.startswith('['):
                            # JSON format: [{"id": 28, "name": "Action"}...]
                            genre_list = json.loads(raw_genres)
                            genres = ' '.join([g.get('name', '') for g in genre_list if 'name' in g])
                        else:
                            # Simple string format
                            genres = raw_genres
                except:
                    genres = str(raw_genres)
            
            movie = {
                'id': movie_id,
                'title': title,
                'overview': row.get('overview') or row.get('description') or '',
                'genres': genres,
                'release_date': row.get('release_date') or row.get('release_year') or '',
                'vote_average': float(row.get('vote_average') or row.get('rating') or 0),
                'vote_count': int(row.get('vote_count') or row.get('votes') or 0),
                'popularity': float(row.get('popularity') or 0),
                'poster_path': poster_path,
                'backdrop_path': backdrop_path,
                'original_language': row.get('original_language') or row.get('language') or 'en',
            }
            movies.append(movie)
        
        print(f"Extracted {len(movies)} movies from CSV")
        return movies
    
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []