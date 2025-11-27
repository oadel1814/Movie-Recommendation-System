# ETL Pipeline Data Source Setup Guide

Your ETL pipeline now supports **3 different data sources**:

## Option 1: TMDB API (Original Method)

### Setup
1. Get an API key from: https://www.themoviedb.org/settings/api
2. Set environment variable:
   ```powershell
   $env:TMDB_API_KEY = "your_api_key_here"
   ```
3. Run the pipeline:
   ```bash
   python etl_pipeline/run_pipeline.py
   ```

### Pros
- Real-time data
- Always up-to-date

### Cons
- Requires API key registration
- Rate-limited (40 requests per 10 seconds)
- May need paid tier for large datasets

---

## Option 2: Kaggle Dataset (Recommended for Local Testing)

### Setup

#### Step 1: Install kaggle library
```bash
pip install kaggle
```

#### Step 2: Download kaggle.json credentials
1. Go to: https://www.kaggle.com/settings/account
2. Click "Create New API Token"
3. Save the `kaggle.json` file to: `~/.kaggle/kaggle.json`

#### Step 3: Set permissions (Windows)
```powershell
# On Windows, the file should be accessible, but if you get permission errors:
# Open File Explorer > navigate to C:\Users\YourUsername\.kaggle
# Right-click kaggle.json > Properties > Security > Advanced
# Make sure your user has Read permissions
```

#### Step 4: Popular Movie Datasets on Kaggle

**Option A: TMDB Movie Metadata**
```bash
# Edit run_pipeline.py and uncomment:
run_etl_pipeline(
    source='kaggle',
    dataset_name='tmdb-movie-metadata',
    csv_file_name='tmdb_5000_movies.csv'
)
```
- 5,000 TMDB movies
- URL: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

**Option B: The Movies Dataset**
```bash
run_etl_pipeline(
    source='kaggle',
    dataset_name='the-movies-dataset',
    csv_file_name='movies_metadata.csv'
)
```
- 45,000+ movies
- URL: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

**Option C: Rotten Tomatoes Movies**
```bash
run_etl_pipeline(
    source='kaggle',
    dataset_name='rotten-tomatoes-movies',
    csv_file_name='movies.csv'
)
```
- Rotten Tomatoes data
- URL: https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset

### Pros
- No API key needed after setup
- Offline-friendly (download once, use anytime)
- Large pre-processed datasets available
- Faster than API calls

### Cons
- One-time data (not real-time)
- Requires kaggle account

---

## Option 3: Local CSV File (Most Flexible)

### Setup
1. Place your CSV file in the project directory (or specify path)
2. CSV should have these columns (or similar):
   ```
   id, title, overview, genres, release_date, vote_average, 
   vote_count, popularity, poster_path, backdrop_path, original_language
   ```

3. Run the pipeline:
   ```bash
   python etl_pipeline/run_pipeline.py
   ```
   Or modify `run_pipeline.py`:
   ```python
   run_etl_pipeline(source='csv', csv_path='your_movies.csv')
   ```

### Pros
- Maximum flexibility
- Can use any CSV format
- No API/authentication needed
- Works 100% offline

### Cons
- Need to prepare CSV yourself
- Must have the right columns

---

## Quick Start Examples

### Example 1: Using Kaggle (Fastest Setup)
```bash
# 1. Install kaggle
pip install kaggle

# 2. Download credentials from https://www.kaggle.com/settings/account
#    Save to ~/.kaggle/kaggle.json

# 3. Edit run_pipeline.py - uncomment Kaggle option:
# Modify the if __name__ == '__main__': section to:
run_etl_pipeline(
    source='kaggle',
    dataset_name='tmdb-movie-metadata',
    csv_file_name='tmdb_5000_movies.csv'
)

# 4. Run pipeline
python etl_pipeline/run_pipeline.py
```

### Example 2: Using Local CSV
```bash
# 1. Place your CSV file: movies.csv

# 2. Edit run_pipeline.py:
run_etl_pipeline(source='csv', csv_path='movies.csv')

# 3. Run pipeline
python etl_pipeline/run_pipeline.py
```

### Example 3: Using TMDB (If you have API key)
```powershell
$env:TMDB_API_KEY = "your_key_here"
python etl_pipeline/run_pipeline.py
```

---

## Troubleshooting

### Kaggle Issues
```
Error: credentials not found at ~/.kaggle/kaggle.json
Solution: Download kaggle.json from https://www.kaggle.com/settings/account
          Place in C:\Users\YourUsername\.kaggle\
```

### CSV Format Issues
```
Error: KeyError when accessing column
Solution: Check that your CSV has required columns (id, title, etc.)
          Use flexible column names (id, movie_id, movie_title, title, etc.)
```

### Too Many/Few Movies
```
Edit transform.py line 56:
df = df[df['vote_count'] > 10]  # Change threshold from 10 to 1, 50, etc.
```

---

## Architecture Changes Made

1. **extract.py**: Added `fetch_movies_from_kaggle()` and `fetch_movies_from_csv()`
2. **run_pipeline.py**: Updated to accept `source` parameter
3. **Backward compatible**: TMDB method still works as before

---

## Next Steps

1. Choose your data source (Kaggle recommended for easy setup)
2. Follow setup steps above
3. Run: `python etl_pipeline/run_pipeline.py`
4. Check that movies appear on homepage

Happy coding! 🎬
