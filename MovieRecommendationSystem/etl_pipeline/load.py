from database.db import db
from database.models import Movie

def load_movies_to_db(df, app):
    """Load transformed movies into the database"""
    with app.app_context():
        inserted = 0
        updated = 0
        
        for _, row in df.iterrows():
            try:
                existing = Movie.query.filter_by(tmdb_id=row['tmdb_id']).first()
                
                if existing:
                    # Update existing movie
                    existing.title = row['title']
                    existing.overview = row['overview']
                    existing.genres = row['genres']
                    existing.release_date = row['release_date']
                    existing.vote_average = row['vote_average']
                    existing.vote_count = row['vote_count']
                    existing.popularity = row['popularity']
                    existing.poster_path = row['poster_path']
                    existing.backdrop_path = row['backdrop_path']
                    existing.original_language = row['original_language']
                    existing.combined_features = row['combined_features']
                    updated += 1
                else:
                    # Insert new movie
                    movie = Movie(
                        tmdb_id=row['tmdb_id'],
                        title=row['title'],
                        overview=row['overview'],
                        genres=row['genres'],
                        release_date=row['release_date'],
                        vote_average=row['vote_average'],
                        vote_count=row['vote_count'],
                        popularity=row['popularity'],
                        poster_path=row['poster_path'],
                        backdrop_path=row['backdrop_path'],
                        original_language=row['original_language'],
                        combined_features=row['combined_features']
                    )
                    db.session.add(movie)
                    inserted += 1
                
                if (inserted + updated) % 50 == 0:
                    db.session.commit()
                    print(f"Processed {inserted + updated} movies...")
            
            except Exception as e:
                print(f"Error loading movie {row['tmdb_id']}: {e}")
                db.session.rollback()
                continue
        
        db.session.commit()
        print(f"\nLoad complete: {inserted} inserted, {updated} updated")
        return inserted, updated