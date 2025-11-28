from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MoviePreprocessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        self.movie_indices = {}
        self.movies = []
    
    def fit(self, movies):
        """Fit the TF-IDF vectorizer on movie features"""
        self.movies = movies
        
        # Create combined features list
        features = [movie.combined_features or '' for movie in movies]
        
        # Build TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(features)
        
        # Create movie ID to index mapping
        self.movie_indices = {movie.id: idx for idx, movie in enumerate(movies)}
        
        print(f"Preprocessor fitted on {len(movies)} movies")
        print(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        
        return self
    
    def compute_similarity_matrix(self):
        """Compute cosine similarity matrix"""
        if self.tfidf_matrix is None:
            raise ValueError("Must call fit() before computing similarity")
        
        similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        return similarity_matrix
    
    def get_movie_index(self, movie_id):
        """Get the index of a movie by its database ID"""
        return self.movie_indices.get(movie_id)
    
    def get_movie_by_index(self, index):
        """Get movie object by its index"""
        if 0 <= index < len(self.movies):
            return self.movies[index]
        return None
    
    def find_similar(self, movie_id, top_k=10):
        """Find similar movies using cosine similarity.
        
        Args:
            movie_id: ID of the reference movie
            top_k: Number of similar movies to return
            
        Returns:
            List of movie objects (excluding the reference movie)
        """
        if self.tfidf_matrix is None:
            return []
        
        movie_idx = self.get_movie_index(movie_id)
        if movie_idx is None:
            return []
        
        # Compute similarity
        similarity_matrix = self.compute_similarity_matrix()
        similarity_scores = similarity_matrix[movie_idx]
        
        # Get top similar movies (excluding the movie itself)
        similar_indices = np.argsort(similarity_scores)[::-1][1:top_k+1]
        
        result = []
        for idx in similar_indices:
            movie = self.get_movie_by_index(int(idx))
            if movie:
                result.append(movie)
        
        return result
    
    def build_index(self, movies):
        """Legacy method for compatibility - same as fit"""
        return self.fit(movies)