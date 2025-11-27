# extract.py
import requests

def fetch_movies(api_key, page=1):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}"
    response = requests.get(url)
    return response.json()["results"]
