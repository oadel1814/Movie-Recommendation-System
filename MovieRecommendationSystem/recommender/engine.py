from database.models import Movie, Watchlist
from recommender.preprocess import MoviePreprocessor

def recommend(movie_id, top_k=10, index=None):
    """Return similar movies using an index or a list of movies (lazy-build)."""
    # no index provided
    if index is None:
        return []
    
    # if index already provides find_similar(), use it
    try:
        if hasattr(index, "find_similar"):
            return index.find_similar(movie_id, top_k=top_k)
    except Exception:
        return []
    
    # if index is a raw list of movies, build a preprocessor lazily
    try:
        from recommender.preprocess import MoviePreprocessor
    except Exception:
        return []
    
    try:
        if isinstance(index, list):
            pre = MoviePreprocessor()
            pre.build_index(index)
            return pre.find_similar(movie_id, top_k=top_k)
    except Exception:
        return []
    return []
 
class RecommendationEngine:
    """Wrapper that accepts a preprocessor, a list of movies, or a pre-built index."""
    def __init__(self, index=None, movies=None):
        self.index = index
        self.movies = movies
        self._preprocessor = None
        
    def _ensure_index(self):
        if self._preprocessor is not None:
            return
        if self.index is not None and hasattr(self.index, "find_similar"):
            self._preprocessor = self.index
            return
        if not self.movies:
            return
        try:
            from recommender.preprocess import MoviePreprocessor
        except Exception:
            return
        self._preprocessor = MoviePreprocessor()
        self._preprocessor.build_index(self.movies)
        
    def recommend(self, movie_id, top_k=10):
        self._ensure_index()
        if self._preprocessor is None:
            return []
        return self._preprocessor.find_similar(movie_id, top_k=top_k)