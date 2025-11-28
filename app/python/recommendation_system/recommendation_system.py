#!/usr/bin/env python3
"""
Movie Recommendation System - Solution Implementation

Description: Comprehensive recommendation engine implementing content-based
filtering, collaborative filtering, and hybrid approaches for movie recommendations.

Time Complexity: O(n × m) where n = number of movies, m = number of users
Space Complexity: O(n × m) for rating matrix, O(n × f) for feature matrix

Dependencies: Standard library (math, collections, typing)
Optional: numpy (for efficient vector operations)
Author: chronosnehal
Date: 2025-01-27
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from collections import defaultdict
from math import sqrt
import logging
import time

# Try to import optional dependencies
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MovieRecommendationSystem:
    """
    Movie recommendation system with content-based and collaborative filtering.
    
    This class provides methods for generating movie recommendations using
    multiple filtering approaches: content-based, collaborative, and hybrid.
    
    Attributes:
        movies: Dictionary mapping movie_id to movie data
        ratings: List of rating dictionaries
        user_ratings: Dictionary mapping user_id to {movie_id: rating}
        movie_ratings: Dictionary mapping movie_id to {user_id: rating}
        user_profiles: Dictionary mapping user_id to user profile data
    """
    
    def __init__(self):
        """
        Initialize recommendation system.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.movies: Dict[int, Dict[str, Any]] = {}
        self.ratings: List[Dict[str, Any]] = []
        self.user_ratings: Dict[int, Dict[int, float]] = defaultdict(dict)
        self.movie_ratings: Dict[int, Dict[int, float]] = defaultdict(dict)
        self.user_profiles: Dict[int, Dict[str, Any]] = {}
        
        logger.info("MovieRecommendationSystem initialized")
    
    def load_movies(self, movies: List[Dict[str, Any]]) -> None:
        """
        Load movie data into the system.
        
        Args:
            movies: List of movie dictionaries
        
        Raises:
            ValueError: If movies list is empty or invalid
        
        Time Complexity: O(n) where n = number of movies
        Space Complexity: O(n)
        """
        if not isinstance(movies, list) or not movies:
            raise ValueError("Movies must be a non-empty list")
        
        self.movies = {}
        for movie in movies:
            if "movie_id" not in movie:
                raise ValueError("Movie must have 'movie_id' field")
            
            movie_id = movie["movie_id"]
            self.movies[movie_id] = {
                "title": movie.get("title", ""),
                "genres": movie.get("genres", []),
                "director": movie.get("director", ""),
                "actors": movie.get("actors", []),
                "year": movie.get("year", 0),
                "rating": movie.get("rating", 0.0),
                "description": movie.get("description", "")
            }
        
        logger.info(f"Loaded {len(self.movies)} movies")
    
    def load_ratings(self, ratings: List[Dict[str, Any]]) -> None:
        """
        Load user ratings into the system.
        
        Args:
            ratings: List of rating dictionaries
        
        Raises:
            ValueError: If ratings list is invalid
        
        Time Complexity: O(r) where r = number of ratings
        Space Complexity: O(r)
        """
        if not isinstance(ratings, list):
            raise ValueError("Ratings must be a list")
        
        self.ratings = ratings
        self.user_ratings = defaultdict(dict)
        self.movie_ratings = defaultdict(dict)
        
        for rating in ratings:
            if not all(k in rating for k in ["user_id", "movie_id", "rating"]):
                continue
            
            user_id = rating["user_id"]
            movie_id = rating["movie_id"]
            rating_value = float(rating["rating"])
            
            # Validate rating range
            if not (1.0 <= rating_value <= 5.0):
                logger.warning(f"Invalid rating {rating_value} for user {user_id}, movie {movie_id}")
                continue
            
            self.user_ratings[user_id][movie_id] = rating_value
            self.movie_ratings[movie_id][user_id] = rating_value
        
        # Build user profiles
        self._build_user_profiles()
        
        logger.info(f"Loaded {len(self.ratings)} ratings from {len(self.user_ratings)} users")
    
    def _build_user_profiles(self) -> None:
        """
        Build user profiles from ratings.
        
        Time Complexity: O(u × m) where u = users, m = average movies per user
        Space Complexity: O(u)
        """
        self.user_profiles = {}
        
        for user_id, movie_ratings in self.user_ratings.items():
            ratings_list = list(movie_ratings.values())
            avg_rating = sum(ratings_list) / len(ratings_list) if ratings_list else 0.0
            
            self.user_profiles[user_id] = {
                "rated_movies": list(movie_ratings.keys()),
                "avg_rating": avg_rating,
                "total_ratings": len(ratings_list)
            }
    
    def _jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard similarity between two sets.
        
        Args:
            set1: First set
            set2: Second set
        
        Returns:
            Jaccard similarity score (0.0-1.0)
        
        Time Complexity: O(min(|set1|, |set2|))
        Space Complexity: O(1)
        """
        if not set1 and not set2:
            return 1.0
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
        
        Returns:
            Cosine similarity score (0.0-1.0)
        
        Time Complexity: O(n) where n = vector length
        Space Complexity: O(1)
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        if NUMPY_AVAILABLE:
            vec1_np = np.array(vec1)
            vec2_np = np.array(vec2)
            dot_product = np.dot(vec1_np, vec2_np)
            norm1 = np.linalg.norm(vec1_np)
            norm2 = np.linalg.norm(vec2_np)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return float(dot_product / (norm1 * norm2))
        else:
            # Manual calculation
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sqrt(sum(a * a for a in vec1))
            norm2 = sqrt(sum(b * b for b in vec2))
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
    
    def _pearson_correlation(
        self,
        user1_ratings: Dict[int, float],
        user2_ratings: Dict[int, float]
    ) -> float:
        """
        Calculate Pearson correlation coefficient between two users.
        
        Args:
            user1_ratings: Ratings dictionary for user 1
            user2_ratings: Ratings dictionary for user 2
        
        Returns:
            Pearson correlation coefficient (-1.0 to 1.0)
        
        Time Complexity: O(m) where m = common movies
        Space Complexity: O(m)
        """
        # Find common movies
        common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
        
        if len(common_movies) < 2:
            return 0.0
        
        # Get ratings for common movies
        ratings1 = [user1_ratings[m] for m in common_movies]
        ratings2 = [user2_ratings[m] for m in common_movies]
        
        # Calculate means
        mean1 = sum(ratings1) / len(ratings1)
        mean2 = sum(ratings2) / len(ratings2)
        
        # Calculate numerator and denominators
        numerator = sum((ratings1[i] - mean1) * (ratings2[i] - mean2) for i in range(len(ratings1)))
        sum_sq_diff1 = sum((r - mean1) ** 2 for r in ratings1)
        sum_sq_diff2 = sum((r - mean2) ** 2 for r in ratings2)
        
        denominator = sqrt(sum_sq_diff1 * sum_sq_diff2)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _calculate_movie_similarity(
        self,
        movie1_id: int,
        movie2_id: int
    ) -> float:
        """
        Calculate similarity between two movies based on content features.
        
        Args:
            movie1_id: First movie ID
            movie2_id: Second movie ID
        
        Returns:
            Similarity score (0.0-1.0)
        
        Time Complexity: O(f) where f = number of features
        Space Complexity: O(1)
        """
        if movie1_id not in self.movies or movie2_id not in self.movies:
            return 0.0
        
        movie1 = self.movies[movie1_id]
        movie2 = self.movies[movie2_id]
        
        # Genre similarity (Jaccard)
        genres1 = set(movie1.get("genres", []))
        genres2 = set(movie2.get("genres", []))
        genre_sim = self._jaccard_similarity(genres1, genres2)
        
        # Actor similarity (Jaccard)
        actors1 = set(movie1.get("actors", []))
        actors2 = set(movie2.get("actors", []))
        actor_sim = self._jaccard_similarity(actors1, actors2)
        
        # Director similarity (exact match)
        director1 = movie1.get("director", "").lower().strip()
        director2 = movie2.get("director", "").lower().strip()
        director_sim = 1.0 if director1 and director1 == director2 else 0.0
        
        # Year similarity (normalized difference)
        year1 = movie1.get("year", 0)
        year2 = movie2.get("year", 0)
        if year1 > 0 and year2 > 0:
            year_diff = abs(year1 - year2)
            year_sim = max(0.0, 1.0 - (year_diff / 50.0))  # Decay over 50 years
        else:
            year_sim = 0.0
        
        # Weighted combination
        similarity = (
            0.4 * genre_sim +
            0.3 * actor_sim +
            0.2 * director_sim +
            0.1 * year_sim
        )
        
        return similarity
    
    def _find_similar_users(
        self,
        user_id: int,
        min_similarity: float = 0.0,
        max_users: int = 50
    ) -> List[Tuple[int, float]]:
        """
        Find users similar to the target user.
        
        Args:
            user_id: Target user ID
            min_similarity: Minimum similarity threshold
            max_users: Maximum number of similar users to return
        
        Returns:
            List of (user_id, similarity_score) tuples, sorted by similarity
        
        Time Complexity: O(u × m) where u = users, m = average movies per user
        Space Complexity: O(u)
        """
        if user_id not in self.user_ratings:
            return []
        
        user_ratings = self.user_ratings[user_id]
        similar_users = []
        
        for other_user_id, other_ratings in self.user_ratings.items():
            if other_user_id == user_id:
                continue
            
            similarity = self._pearson_correlation(user_ratings, other_ratings)
            
            if similarity >= min_similarity:
                similar_users.append((other_user_id, similarity))
        
        # Sort by similarity (descending)
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        return similar_users[:max_users]
    
    def _content_based_recommendations(
        self,
        user_id: int,
        top_n: int = 10,
        exclude_rated: bool = True,
        min_rating: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Generate content-based recommendations for a user.
        
        Args:
            user_id: User ID
            top_n: Number of recommendations
            exclude_rated: Exclude already rated movies
            min_rating: Minimum rating threshold for user's rated movies
        
        Returns:
            List of recommendation dictionaries
        
        Time Complexity: O(n × m) where n = movies, m = user's rated movies
        Space Complexity: O(n)
        """
        if user_id not in self.user_ratings:
            # Cold start: return popular movies
            return self._popularity_based_recommendations(top_n)
        
        user_ratings = self.user_ratings[user_id]
        
        # Get user's highly-rated movies
        highly_rated_movies = [
            movie_id for movie_id, rating in user_ratings.items()
            if rating >= min_rating
        ]
        
        if not highly_rated_movies:
            # No highly-rated movies, use all rated movies
            highly_rated_movies = list(user_ratings.keys())
        
        # Calculate similarity scores for all movies
        movie_scores = {}
        
        for movie_id in self.movies.keys():
            if exclude_rated and movie_id in user_ratings:
                continue
            
            # Calculate similarity to user's preferred movies
            similarities = []
            for preferred_movie_id in highly_rated_movies:
                similarity = self._calculate_movie_similarity(preferred_movie_id, movie_id)
                # Weight by user's rating
                weight = user_ratings.get(preferred_movie_id, 3.0) / 5.0
                similarities.append(similarity * weight)
            
            if similarities:
                avg_similarity = sum(similarities) / len(similarities)
                movie_scores[movie_id] = avg_similarity
        
        # Sort by score and get top-N
        sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for movie_id, similarity_score in sorted_movies[:top_n]:
            movie = self.movies[movie_id]
            predicted_rating = 3.0 + (similarity_score * 2.0)  # Scale to 3.0-5.0
            
            recommendations.append({
                "movie_id": movie_id,
                "title": movie["title"],
                "predicted_rating": round(predicted_rating, 2),
                "confidence_score": round(similarity_score, 2),
                "reason": f"Similar to movies you rated highly (similarity: {similarity_score:.2f})",
                "similarity_score": round(similarity_score, 2)
            })
        
        return recommendations
    
    def _collaborative_recommendations(
        self,
        user_id: int,
        top_n: int = 10,
        exclude_rated: bool = True,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Generate collaborative filtering recommendations for a user.
        
        Args:
            user_id: User ID
            top_n: Number of recommendations
            exclude_rated: Exclude already rated movies
            min_similarity: Minimum user similarity threshold
        
        Returns:
            List of recommendation dictionaries
        
        Time Complexity: O(u × m) where u = users, m = movies
        Space Complexity: O(m)
        """
        if user_id not in self.user_ratings:
            # Cold start: return popular movies
            return self._popularity_based_recommendations(top_n)
        
        # Find similar users
        similar_users = self._find_similar_users(user_id, min_similarity=min_similarity)
        
        if not similar_users:
            # No similar users, fallback to content-based
            logger.warning(f"No similar users found for user {user_id}, using content-based")
            return self._content_based_recommendations(user_id, top_n, exclude_rated)
        
        user_ratings = self.user_ratings[user_id]
        user_avg_rating = self.user_profiles[user_id]["avg_rating"]
        
        # Predict ratings for unrated movies
        movie_predictions = {}
        
        for movie_id in self.movies.keys():
            if exclude_rated and movie_id in user_ratings:
                continue
            
            # Predict rating using similar users
            numerator = 0.0
            denominator = 0.0
            
            for similar_user_id, similarity in similar_users:
                if movie_id in self.user_ratings[similar_user_id]:
                    similar_user_rating = self.user_ratings[similar_user_id][movie_id]
                    similar_user_avg = self.user_profiles[similar_user_id]["avg_rating"]
                    
                    numerator += similarity * (similar_user_rating - similar_user_avg)
                    denominator += abs(similarity)
            
            if denominator > 0:
                predicted_rating = user_avg_rating + (numerator / denominator)
                # Clamp to valid range
                predicted_rating = max(1.0, min(5.0, predicted_rating))
                confidence = min(1.0, denominator / len(similar_users))
                
                movie_predictions[movie_id] = {
                    "predicted_rating": predicted_rating,
                    "confidence": confidence
                }
        
        # Sort by predicted rating and get top-N
        sorted_movies = sorted(
            movie_predictions.items(),
            key=lambda x: x[1]["predicted_rating"],
            reverse=True
        )
        
        recommendations = []
        for movie_id, pred_data in sorted_movies[:top_n]:
            movie = self.movies[movie_id]
            
            recommendations.append({
                "movie_id": movie_id,
                "title": movie["title"],
                "predicted_rating": round(pred_data["predicted_rating"], 2),
                "confidence_score": round(pred_data["confidence"], 2),
                "reason": f"Users with similar preferences rated this highly",
                "similarity_score": 0.0
            })
        
        return recommendations
    
    def _popularity_based_recommendations(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Generate popularity-based recommendations (for cold start).
        
        Args:
            top_n: Number of recommendations
        
        Returns:
            List of recommendation dictionaries
        
        Time Complexity: O(n) where n = number of movies
        Space Complexity: O(n)
        """
        # Calculate average ratings for each movie
        movie_avg_ratings = {}
        
        for movie_id, ratings in self.movie_ratings.items():
            if ratings:
                avg_rating = sum(ratings.values()) / len(ratings)
                movie_avg_ratings[movie_id] = avg_rating
            else:
                # Use movie's own rating if available
                movie_avg_ratings[movie_id] = self.movies[movie_id].get("rating", 0.0) / 2.0
        
        # Sort by average rating
        sorted_movies = sorted(
            movie_avg_ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        recommendations = []
        for movie_id, avg_rating in sorted_movies[:top_n]:
            movie = self.movies[movie_id]
            
            recommendations.append({
                "movie_id": movie_id,
                "title": movie["title"],
                "predicted_rating": round(avg_rating, 2),
                "confidence_score": 0.65,  # Lower confidence for cold start
                "reason": f"Popular item: High average rating ({avg_rating:.2f})",
                "similarity_score": 0.0
            })
        
        return recommendations
    
    def _hybrid_recommendations(
        self,
        user_id: int,
        top_n: int = 10,
        exclude_rated: bool = True,
        content_weight: float = 0.5,
        min_rating: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Generate hybrid recommendations combining content-based and collaborative.
        
        Args:
            user_id: User ID
            top_n: Number of recommendations
            exclude_rated: Exclude already rated movies
            content_weight: Weight for content-based (0.0-1.0)
            min_rating: Minimum rating threshold
        
        Returns:
            List of recommendation dictionaries
        
        Time Complexity: O(n × m) where n = movies, m = users
        Space Complexity: O(n)
        """
        # Get content-based recommendations
        content_recs = self._content_based_recommendations(
            user_id, top_n * 2, exclude_rated, min_rating
        )
        
        # Get collaborative recommendations
        collaborative_recs = self._collaborative_recommendations(
            user_id, top_n * 2, exclude_rated
        )
        
        # Create score dictionaries
        content_scores = {r["movie_id"]: r["predicted_rating"] for r in content_recs}
        collaborative_scores = {r["movie_id"]: r["predicted_rating"] for r in collaborative_recs}
        
        # Combine scores
        all_movie_ids = set(content_scores.keys()) | set(collaborative_scores.keys())
        hybrid_scores = {}
        
        for movie_id in all_movie_ids:
            content_score = content_scores.get(movie_id, 3.0)
            collaborative_score = collaborative_scores.get(movie_id, 3.0)
            
            hybrid_score = (
                content_weight * content_score +
                (1 - content_weight) * collaborative_score
            )
            
            hybrid_scores[movie_id] = hybrid_score
        
        # Sort by hybrid score
        sorted_movies = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Build recommendations
        recommendations = []
        for movie_id, hybrid_score in sorted_movies[:top_n]:
            movie = self.movies[movie_id]
            content_score = content_scores.get(movie_id, 0)
            collaborative_score = collaborative_scores.get(movie_id, 0)
            
            # Determine reason
            if content_score > 0 and collaborative_score > 0:
                reason = "Combined: Similar users liked it (collaborative) + Similar content (content-based)"
            elif content_score > 0:
                reason = "Content-based: Similar to movies you rated highly"
            else:
                reason = "Collaborative: Users with similar preferences rated this highly"
            
            recommendations.append({
                "movie_id": movie_id,
                "title": movie["title"],
                "predicted_rating": round(hybrid_score, 2),
                "confidence_score": 0.82,  # Higher confidence for hybrid
                "reason": reason,
                "similarity_score": 0.0
            })
        
        return recommendations
    
    def find_similar_movies(
        self,
        movie_id: int,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Find movies similar to the given movie.
        
        Args:
            movie_id: Movie ID
            top_n: Number of similar movies
        
        Returns:
            Dictionary with similar movies
        
        Raises:
            ValueError: If movie_id is invalid
        
        Time Complexity: O(n) where n = number of movies
        Space Complexity: O(n)
        """
        if movie_id not in self.movies:
            raise ValueError(f"Movie {movie_id} not found")
        
        movie = self.movies[movie_id]
        similarities = []
        
        for other_movie_id, other_movie in self.movies.items():
            if other_movie_id == movie_id:
                continue
            
            similarity = self._calculate_movie_similarity(movie_id, other_movie_id)
            
            # Find common features
            common_genres = set(movie.get("genres", [])) & set(other_movie.get("genres", []))
            common_actors = set(movie.get("actors", [])) & set(other_movie.get("actors", []))
            common_features = list(common_genres) + list(common_actors)
            
            if movie.get("director") == other_movie.get("director") and movie.get("director"):
                common_features.append(f"Director: {movie.get('director')}")
            
            similarities.append({
                "movie_id": other_movie_id,
                "title": other_movie["title"],
                "similarity_score": round(similarity, 2),
                "common_features": common_features
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return {
            "movie_id": movie_id,
            "title": movie["title"],
            "similar_movies": similarities[:top_n],
            "metadata": {
                "total_movies": len(self.movies),
                "computation_time": 0.0  # Will be set by caller
            }
        }
    
    def recommend(
        self,
        user_id: int,
        method: str = "hybrid",
        top_n: int = 10,
        min_rating: float = 3.0,
        exclude_rated: bool = True,
        diversity: bool = False,
        movie_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate movie recommendations for a user.
        
        Args:
            user_id: User ID
            method: Recommendation method ("content", "collaborative", "hybrid", "similar")
            top_n: Number of recommendations
            min_rating: Minimum rating threshold
            exclude_rated: Exclude already rated movies
            diversity: Include diversity in recommendations (not implemented in basic version)
            movie_id: Movie ID (required for "similar" method)
        
        Returns:
            Dictionary with recommendations and metadata
        
        Raises:
            ValueError: If inputs are invalid
        
        Time Complexity: O(n × m) where n = movies, m = users
        Space Complexity: O(n)
        
        Examples:
            >>> system = MovieRecommendationSystem()
            >>> system.load_movies(movies)
            >>> system.load_ratings(ratings)
            >>> result = system.recommend(user_id=1, method="hybrid", top_n=10)
            >>> print(result["recommendations"][0]["title"])
        """
        start_time = time.time()
        warnings = []
        
        # Validate inputs
        if method not in ["content", "collaborative", "hybrid", "similar"]:
            raise ValueError(f"Invalid method: {method}. Must be one of: content, collaborative, hybrid, similar")
        
        if top_n < 1 or top_n > 100:
            raise ValueError("top_n must be between 1 and 100")
        
        if method == "similar":
            if movie_id is None:
                raise ValueError("movie_id is required for 'similar' method")
            return self.find_similar_movies(movie_id, top_n)
        
        # Check for cold start
        cold_start = user_id not in self.user_ratings
        
        if cold_start:
            warnings.append("User has no ratings. Using popularity-based recommendations.")
            recommendations = self._popularity_based_recommendations(top_n)
        else:
            # Generate recommendations based on method
            if method == "content":
                recommendations = self._content_based_recommendations(
                    user_id, top_n, exclude_rated, min_rating
                )
            elif method == "collaborative":
                recommendations = self._collaborative_recommendations(
                    user_id, top_n, exclude_rated
                )
            else:  # hybrid
                recommendations = self._hybrid_recommendations(
                    user_id, top_n, exclude_rated, content_weight=0.5, min_rating=min_rating
                )
        
        computation_time = time.time() - start_time
        
        # Filter candidates count
        total_candidates = len(self.movies)
        if exclude_rated and not cold_start:
            rated_count = len(self.user_ratings.get(user_id, {}))
            filtered_candidates = total_candidates - rated_count
        else:
            filtered_candidates = total_candidates
        
        logger.info(
            f"Generated {len(recommendations)} recommendations for user {user_id} "
            f"using {method} method in {computation_time:.2f}s"
        )
        
        return {
            "user_id": user_id,
            "method": method,
            "recommendations": recommendations,
            "metadata": {
                "total_candidates": total_candidates,
                "filtered_candidates": filtered_candidates,
                "computation_time": round(computation_time, 2),
                "cold_start": cold_start
            },
            "warnings": warnings
        }


def main():
    """Demonstrate recommendation system with examples."""
    system = MovieRecommendationSystem()
    
    print("=" * 80)
    print("Movie Recommendation System - Examples")
    print("=" * 80)
    
    # Sample movie data
    movies = [
        {
            "movie_id": 1,
            "title": "The Matrix",
            "genres": ["Action", "Sci-Fi"],
            "director": "Wachowski Brothers",
            "actors": ["Keanu Reeves", "Laurence Fishburne"],
            "year": 1999,
            "rating": 8.7
        },
        {
            "movie_id": 2,
            "title": "Inception",
            "genres": ["Action", "Sci-Fi", "Thriller"],
            "director": "Christopher Nolan",
            "actors": ["Leonardo DiCaprio", "Marion Cotillard"],
            "year": 2010,
            "rating": 8.8
        },
        {
            "movie_id": 3,
            "title": "The Godfather",
            "genres": ["Crime", "Drama"],
            "director": "Francis Ford Coppola",
            "actors": ["Marlon Brando", "Al Pacino"],
            "year": 1972,
            "rating": 9.2
        },
        {
            "movie_id": 4,
            "title": "Interstellar",
            "genres": ["Adventure", "Drama", "Sci-Fi"],
            "director": "Christopher Nolan",
            "actors": ["Matthew McConaughey", "Anne Hathaway"],
            "year": 2014,
            "rating": 8.6
        },
        {
            "movie_id": 5,
            "title": "The Dark Knight",
            "genres": ["Action", "Crime", "Drama"],
            "director": "Christopher Nolan",
            "actors": ["Christian Bale", "Heath Ledger"],
            "year": 2008,
            "rating": 9.0
        }
    ]
    
    # Sample ratings data
    ratings = [
        {"user_id": 1, "movie_id": 1, "rating": 5.0},
        {"user_id": 1, "movie_id": 2, "rating": 4.5},
        {"user_id": 2, "movie_id": 1, "rating": 4.5},
        {"user_id": 2, "movie_id": 2, "rating": 5.0},
        {"user_id": 2, "movie_id": 3, "rating": 4.5},
        {"user_id": 2, "movie_id": 4, "rating": 4.0},
        {"user_id": 3, "movie_id": 1, "rating": 3.0},
        {"user_id": 3, "movie_id": 3, "rating": 4.0},
        {"user_id": 3, "movie_id": 5, "rating": 4.5}
    ]
    
    # Load data
    system.load_movies(movies)
    system.load_ratings(ratings)
    
    # Example 1: Content-based recommendations
    print("\n" + "-" * 80)
    print("Example 1: Content-Based Recommendations for User 1")
    print("-" * 80)
    
    try:
        result1 = system.recommend(user_id=1, method="content", top_n=3)
        print(f"✓ Generated {len(result1['recommendations'])} recommendations")
        for rec in result1["recommendations"]:
            print(f"  - {rec['title']}: Predicted rating {rec['predicted_rating']}, "
                  f"Confidence {rec['confidence_score']}")
            print(f"    Reason: {rec['reason']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 2: Collaborative filtering recommendations
    print("\n" + "-" * 80)
    print("Example 2: Collaborative Filtering Recommendations for User 1")
    print("-" * 80)
    
    try:
        result2 = system.recommend(user_id=1, method="collaborative", top_n=3)
        print(f"✓ Generated {len(result2['recommendations'])} recommendations")
        for rec in result2["recommendations"]:
            print(f"  - {rec['title']}: Predicted rating {rec['predicted_rating']}, "
                  f"Confidence {rec['confidence_score']}")
            print(f"    Reason: {rec['reason']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 3: Hybrid recommendations
    print("\n" + "-" * 80)
    print("Example 3: Hybrid Recommendations for User 1")
    print("-" * 80)
    
    try:
        result3 = system.recommend(user_id=1, method="hybrid", top_n=3)
        print(f"✓ Generated {len(result3['recommendations'])} recommendations")
        for rec in result3["recommendations"]:
            print(f"  - {rec['title']}: Predicted rating {rec['predicted_rating']}, "
                  f"Confidence {rec['confidence_score']}")
            print(f"    Reason: {rec['reason']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 4: Similar movies
    print("\n" + "-" * 80)
    print("Example 4: Find Similar Movies to 'The Matrix'")
    print("-" * 80)
    
    try:
        result4 = system.find_similar_movies(movie_id=1, top_n=3)
        print(f"✓ Found {len(result4['similar_movies'])} similar movies")
        for similar in result4["similar_movies"]:
            print(f"  - {similar['title']}: Similarity {similar['similarity_score']}")
            if similar['common_features']:
                print(f"    Common features: {', '.join(similar['common_features'][:3])}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 5: Cold start (new user)
    print("\n" + "-" * 80)
    print("Example 5: Cold Start - New User (User 999)")
    print("-" * 80)
    
    try:
        result5 = system.recommend(user_id=999, method="hybrid", top_n=3)
        print(f"✓ Generated {len(result5['recommendations'])} recommendations")
        if result5['metadata']['cold_start']:
            print("  Cold start detected: Using popularity-based recommendations")
        for rec in result5["recommendations"]:
            print(f"  - {rec['title']}: Predicted rating {rec['predicted_rating']}, "
                  f"Confidence {rec['confidence_score']}")
            print(f"    Reason: {rec['reason']}")
        if result5['warnings']:
            print(f"  Warnings: {result5['warnings']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 6: Error handling
    print("\n" + "-" * 80)
    print("Example 6: Error Handling - Invalid Method")
    print("-" * 80)
    
    try:
        result6 = system.recommend(user_id=1, method="invalid_method")
        print(f"Result: {result6}")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print("\n" + "=" * 80)
    print("Important Notes:")
    print("=" * 80)
    print("""
1. Content-based filtering uses movie features (genres, actors, director, year)
2. Collaborative filtering uses user rating patterns and similarity
3. Hybrid approach combines both methods for better recommendations
4. Cold start problems are handled with popularity-based recommendations
5. Similarity calculations use Jaccard (sets) and cosine/Pearson (vectors)
6. For production use:
   - Consider using sparse matrices for large datasets
   - Implement caching for similarity calculations
   - Add diversity filtering for more varied recommendations
   - Use machine learning models for better predictions
   - Handle real-time updates for new ratings
    """)
    
    print("=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()

