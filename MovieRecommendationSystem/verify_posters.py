from database.models import Movie
from app import create_app

app = create_app()

with app.app_context():
    movie_count = Movie.query.count()
    print(f'Total movies in database: {movie_count}')
    
    print('\nSample movies with poster paths:')
    movies = Movie.query.limit(10).all()
    for movie in movies:
        poster_preview = movie.poster_path[:80] if movie.poster_path else "EMPTY"
        print(f'  {movie.title}:')
        print(f'    {poster_preview}...\n')
