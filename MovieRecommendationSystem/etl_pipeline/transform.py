import pandas as pd
import re

def clean_text(text):
    """Clean text data"""
    if not text:
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def extract_genres(genre_list):
    """Extract genre names from genre objects"""
    if isinstance(genre_list, list):
        return ' '.join([g['name'] for g in genre_list if 'name' in g])
    return ""

def transform_movies(raw_movies):
    """Transform raw movie data into clean format"""
    transformed = []
    
    for movie in raw_movies:
        try:
            genres = ""
            if 'genres' in movie:
                genres = extract_genres(movie['genres'])
            elif 'genre_ids' in movie:
                # Map genre IDs to names
                genre_map = {
                    28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy',
                    80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family',
                    14: 'Fantasy', 36: 'History', 27: 'Horror', 10402: 'Music',
                    9648: 'Mystery', 10749: 'Romance', 878: 'Science Fiction',
                    10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western'
                }
                genres = ' '.join([genre_map.get(gid, '') for gid in movie.get('genre_ids', [])])
            
            overview = clean_text(movie.get('overview', ''))
            title = clean_text(movie.get('title', ''))
            genres_clean = clean_text(genres)
            
            # Combine features for recommendation
            combined = f"{title} {overview} {genres_clean} {genres_clean}"
            
            transformed_movie = {
                'tmdb_id': movie.get('id'),
                'title': movie.get('title', 'Unknown'),
                'overview': movie.get('overview', ''),
                'genres': genres,
                'release_date': movie.get('release_date', ''),
                'vote_average': movie.get('vote_average', 0.0),
                'vote_count': movie.get('vote_count', 0),
                'popularity': movie.get('popularity', 0.0),
                'poster_path': movie.get('poster_path', ''),
                'backdrop_path': movie.get('backdrop_path', ''),
                'original_language': movie.get('original_language', 'en'),
                'combined_features': combined
            }
            transformed.append(transformed_movie)
        except Exception as e:
            print(f"Error transforming movie {movie.get('id', 'unknown')}: {e}")
            continue
    
    df = pd.DataFrame(transformed)
    df = df.drop_duplicates(subset=['tmdb_id'])
    df = df[df['vote_count'] > 10]  # Filter out movies with very few votes
    
    print(f"Transformed {len(df)} movies")
    return df