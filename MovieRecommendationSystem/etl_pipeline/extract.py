import requests
import time
from config import Config

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