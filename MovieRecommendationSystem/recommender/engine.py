from database.models import Movie, Watchlist
from recommender.preprocess import MoviePreprocessor
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationEngine:
    """Recommendation engine that provides similar movies and personalized recommendations."""
    
    def __init__(self, index=None, movies=None):
        self.movies = movies or []
        self._preprocessor = None
        self._is_fitted = False
        self._similarity_matrix = None
        
        # Initialize if movies are provided
        if self.movies:
            self._fit()
    
    def _fit(self):
        """Fit the preprocessor on movies."""
        if not self.movies:
            return
        
        try:
            self._preprocessor = MoviePreprocessor()
            self._preprocessor.fit(self.movies)
            self._similarity_matrix = self._preprocessor.compute_similarity_matrix()
            self._is_fitted = True
            print(f"Recommendation engine fitted with {len(self.movies)} movies")
        except Exception as e:
            print(f"Error fitting recommendation engine: {e}")
            self._is_fitted = False
    
    @property
    def is_fitted(self):
        """Check if the engine is ready."""
        return self._is_fitted and self._preprocessor is not None
    
    def get_similar_movies(self, movie_id, top_n=10):
        """Get similar movies based on content similarity.
        
        Args:
            movie_id: ID of the reference movie
            top_n: Number of similar movies to return
            
        Returns:
            List of tuples (movie, similarity_score)
        """
        if not self.is_fitted:
            return []
        
        try:
            # Get the index of the movie
            movie_idx = self._preprocessor.get_movie_index(movie_id)
            if movie_idx is None:
                return []
            
            # Get similarity scores
            similarity_scores = self._similarity_matrix[movie_idx]
            
            # Get top similar movies (excluding the movie itself)
            similar_indices = np.argsort(similarity_scores)[::-1][1:top_n+1]
            
            result = []
            for idx in similar_indices:
                movie = self._preprocessor.get_movie_by_index(int(idx))
                if movie:
                    score = float(similarity_scores[idx])
                    result.append((movie, score))
            
            return result
        except Exception as e:
            print(f"Error getting similar movies: {e}")
            return []
    
    def get_recommendations_for_user(self, user_id, top_n=10):
        """Get personalized recommendations for a user based on their watchlist.
        
        Args:
            user_id: ID of the user
            top_n: Number of recommendations to return
            
        Returns:
            List of tuples (movie, recommendation_score)
        """
        if not self.is_fitted:
            return []
        
        try:
            # Get user's watched movies (prioritize watched over just added)
            watched_watchlist = Watchlist.query.filter_by(user_id=user_id, watched=True).all()
            added_watchlist = Watchlist.query.filter_by(user_id=user_id).all()
            
            # Use watched movies if available, otherwise use added movies
            user_watchlist = watched_watchlist if watched_watchlist else added_watchlist
            
            if not user_watchlist:
                # Return popular movies if user has no watchlist
                popular_movies = sorted(self.movies, 
                        key=lambda x: (x.vote_count or 0, x.vote_average or 0), 
                        reverse=True)[:top_n]
                return [(m, float(m.popularity or 0)) for m in popular_movies]
            
            user_movie_ids = [item.movie_id for item in user_watchlist]
            
            # Aggregate similarity scores from all user's movies
            aggregated_scores = np.zeros(len(self.movies))
            
            for user_movie_id in user_movie_ids:
                similar_movies = self.get_similar_movies(user_movie_id, top_n=50)
                for similar_movie, score in similar_movies:
                    if similar_movie.id not in user_movie_ids:
                        movie_idx = self._preprocessor.get_movie_index(similar_movie.id)
                        if movie_idx is not None:
                            aggregated_scores[movie_idx] += score
            
            # Get top recommendations (with fallback to popularity if no similarities found)
            top_indices = np.argsort(aggregated_scores)[::-1][:top_n*2]
            
            result = []
            for idx in top_indices:
                if aggregated_scores[idx] > 0:
                    movie = self._preprocessor.get_movie_by_index(int(idx))
                    if movie:
                        score = float(aggregated_scores[idx])
                        result.append((movie, score))
                        if len(result) >= top_n:
                            break
            
            # If we don't have enough recommendations, fill with popular movies
            if len(result) < top_n:
                recommended_ids = {m.id for m, _ in result}
                popular_movies = [m for m in sorted(self.movies, 
                        key=lambda x: (x.vote_count or 0, x.vote_average or 0), 
                        reverse=True) if m.id not in recommended_ids and m.id not in user_movie_ids]
                
                for movie in popular_movies:
                    if len(result) >= top_n:
                        break
                    result.append((movie, float(movie.popularity or 0)))
            
            return result
        except Exception as e:
            print(f"Error getting user recommendations: {e}")
            import traceback
            traceback.print_exc()
            return []