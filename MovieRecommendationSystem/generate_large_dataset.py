import csv
import random

# Generate a larger dataset with 500+ movies
movies = [
    ("The Shawshank Redemption", "Drama", "1994-10-14", 8.7),
    ("The Godfather", "Crime Drama", "1972-03-24", 9.2),
    ("The Dark Knight", "Action Crime Drama", "2008-07-18", 9.0),
    ("Inception", "Action Sci-Fi Thriller", "2010-07-16", 8.8),
    ("Pulp Fiction", "Crime Drama", "1994-10-14", 8.9),
    ("Forrest Gump", "Drama Romance", "1994-07-06", 8.8),
    ("The Matrix", "Action Sci-Fi", "1999-03-31", 8.7),
    ("Goodfellas", "Crime Drama", "1990-09-19", 8.7),
    ("The Silence of the Lambs", "Crime Drama Thriller", "1991-02-14", 8.6),
    ("Se7en", "Crime Drama Mystery", "1995-09-22", 8.6),
    ("Saving Private Ryan", "Drama War", "1998-07-24", 8.6),
    ("Schindler's List", "Biography Drama History", "1993-12-15", 9.0),
    ("Gladiator", "Action Adventure Drama", "2000-05-05", 8.5),
    ("The Green Mile", "Crime Drama Fantasy", "1999-12-10", 8.6),
    ("Interstellar", "Adventure Drama Sci-Fi", "2014-11-07", 8.6),
    ("The Usual Suspects", "Crime Drama Mystery", "1995-08-02", 8.5),
    ("L.A. Confidential", "Crime Drama Mystery", "1997-09-19", 8.2),
    ("The Departed", "Crime Drama Thriller", "2006-10-06", 8.5),
    ("Mystic River", "Crime Drama Mystery", "2003-10-10", 8.2),
    ("The Prestige", "Drama Mystery Sci-Fi", "2006-10-20", 8.5),
    ("Fight Club", "Drama Thriller", "1999-10-15", 8.8),
    ("The Sixth Sense", "Drama Mystery Thriller", "1999-08-06", 8.2),
    ("Jurassic Park", "Action Adventure Sci-Fi", "1993-06-11", 8.2),
    ("The Lion King", "Animation Adventure Drama", "1994-06-15", 8.5),
    ("Avatar", "Action Adventure Sci-Fi", "2009-12-18", 8.0),
    ("Titanic", "Adventure Drama Romance", "1997-12-19", 7.9),
    ("Jaws", "Adventure Thriller", "1975-06-20", 8.1),
    ("E.T.", "Adventure Family Sci-Fi", "1982-06-11", 7.9),
    ("Back to the Future", "Adventure Comedy Sci-Fi", "1985-07-03", 8.5),
    ("The Terminator", "Action Sci-Fi Thriller", "1984-10-26", 8.1),
    ("Alien", "Horror Sci-Fi Thriller", "1979-05-25", 8.4),
    ("The Thing", "Horror Sci-Fi Thriller", "1982-06-25", 8.1),
    ("Blade Runner", "Neo-Noir Sci-Fi Thriller", "1982-06-25", 8.1),
    ("2001: A Space Odyssey", "Adventure Sci-Fi", "1968-04-02", 8.3),
    ("The Shining", "Horror Thriller", "1980-05-23", 8.4),
    ("Psycho", "Horror Thriller", "1960-12-08", 8.4),
    ("Vertigo", "Mystery Thriller", "1958-05-09", 8.3),
    ("Rear Window", "Mystery Thriller", "1954-08-01", 8.5),
    ("Casablanca", "Drama Romance War", "1942-11-26", 8.5),
    ("Citizen Kane", "Drama Mystery", "1941-05-01", 8.3),
    ("Singin' in the Rain", "Comedy Musical Romance", "1952-03-27", 8.3),
    ("Some Like It Hot", "Comedy", "1959-03-19", 8.2),
    ("Breakfast at Tiffany's", "Comedy Romance", "1961-10-05", 7.8),
    ("Roman Holiday", "Comedy Romance", "1953-09-02", 8.0),
    ("Sabrina", "Comedy Drama Romance", "1995-12-15", 7.6),
    ("My Fair Lady", "Comedy Drama Musical", "1964-10-21", 8.0),
    ("Grease", "Comedy Drama Musical", "1978-06-16", 7.2),
    ("Hairspray", "Comedy Drama Musical", "2007-07-20", 7.0),
    ("The Sound of Music", "Drama Family Musical", "1965-03-02", 8.0),
    ("West Side Story", "Drama Musical Romance", "1961-10-18", 7.9),
]

# Colors for placeholder images
colors = ['FF6B6B', 'FFA07A', 'FFD700', 'ADFF2F', '3CB371', '00CED1', '1E90FF', '9370DB', 'FF69B4', 'FF8C00']

# Expand to 500+ movies by creating variations
all_movies = []
movie_id = 1
for i in range(12):  # 12 rounds = 600 movies
    for idx, (title, genres, release_date, rating) in enumerate(movies):
        year_offset = i * 5
        year = int(release_date.split('-')[0]) + year_offset
        rating_variation = rating + random.uniform(-0.5, 0.5)
        rating_variation = max(1.0, min(10.0, rating_variation))
        
        # Use different colored placeholders
        color = colors[(movie_id + idx) % len(colors)]
        poster_url = f"https://dummyimage.com/500x750/{color}/FFFFFF.jpg?text={title.replace(' ', '+')[:30]}"
        backdrop_url = f"https://dummyimage.com/1280x720/{color}/FFFFFF.jpg?text={title.replace(' ', '+')[:30]}"
        
        all_movies.append({
            'id': movie_id,
            'title': f"{title} ({year})" if i > 0 else title,
            'overview': f"An interesting movie about {title.lower()}. " * 3,
            'genres': genres,
            'release_date': f"{year}-{release_date.split('-')[1]}-{release_date.split('-')[2]}",
            'vote_average': round(rating_variation, 1),
            'vote_count': random.randint(1000, 50000),
            'popularity': random.uniform(10, 100),
            'poster_path': poster_url,
            'backdrop_path': backdrop_url,
            'original_language': 'en'
        })
        movie_id += 1

# Write to CSV
with open('large_movies.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'title', 'overview', 'genres', 'release_date', 
                                           'vote_average', 'vote_count', 'popularity', 
                                           'poster_path', 'backdrop_path', 'original_language'])
    writer.writeheader()
    writer.writerows(all_movies)

print(f"✓ Created large_movies.csv with {len(all_movies)} movies!")
print(f"Using DummyImage.com URLs (more reliable than placeholder.com)")
print(f"\nNext steps:")
print(f"1. Delete database: remove instance/movies.db")
print(f"2. Run: python etl_pipeline/run_pipeline.py")
print(f"3. Start Flask app to see movies with colored placeholders")
