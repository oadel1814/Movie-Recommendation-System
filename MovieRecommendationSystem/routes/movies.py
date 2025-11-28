from flask import Blueprint, render_template, request, jsonify
from database.models import Movie
from config import Config

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    genre = request.args.get('genre', '')
    sort_by = request.args.get('sort', 'popularity')
    
    query = Movie.query
    
    # Filter by genre
    if genre:
        query = query.filter(Movie.genres.like(f'%{genre}%'))
    
    # Sort
    if sort_by == 'rating':
        query = query.order_by(Movie.vote_average.desc(), Movie.vote_count.desc())
    elif sort_by == 'recent':
        query = query.order_by(Movie.release_date.desc())
    else:  # popularity
        query = query.order_by(Movie.popularity.desc())
    
    pagination = query.paginate(
        page=page,
        per_page=Config.MOVIES_PER_PAGE,
        error_out=False
    )
    
    # Get unique genres
    all_movies = Movie.query.all()
    genres_set = set()
    for movie in all_movies:
        if movie.genres:
            genres_set.update(movie.genres.split())
    genres = sorted(list(genres_set))
    
    return render_template('index.html',
                         movies=pagination.items,
                         pagination=pagination,
                         genres=genres,
                         current_genre=genre,
                         current_sort=sort_by)

@movies_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    # Get similar movies
    from app import get_recommendation_engine
    similar_movies = []
    recommendation_engine = get_recommendation_engine()
    if recommendation_engine and recommendation_engine.is_fitted:
        similar = recommendation_engine.get_similar_movies(movie_id, top_n=6)
        similar_movies = [m for m, score in similar]
    
    return render_template('movie_detail.html', movie=movie, similar_movies=similar_movies)

@movies_bp.route('/search')
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify([])
    
    movies = Movie.query.filter(
        Movie.title.ilike(f'%{query}%')
    ).order_by(Movie.popularity.desc()).limit(10).all()
    
    results = [{
        'id': m.id,
        'title': m.title,
        'year': m.release_date[:4] if m.release_date else '',
        'poster': m.poster_path,
        'rating': round(m.vote_average, 1) if m.vote_average else 0
    } for m in movies]
    
    return jsonify(results)