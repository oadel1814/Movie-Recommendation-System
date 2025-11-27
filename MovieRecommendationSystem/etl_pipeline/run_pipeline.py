from .extract import fetch_movies
from .transform import transform_movies
from .load import load_movies

def run_etl(db_session, api_key=None):
    raw = fetch_movies(api_key=api_key)
    cleaned = transform_movies(raw)
    load_movies(db_session, cleaned)
