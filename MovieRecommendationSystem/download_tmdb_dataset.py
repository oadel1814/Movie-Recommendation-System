"""
Download TMDB 5000 Movie Dataset directly
"""
import os
import urllib.request
import zipfile
import shutil

def download_tmdb_dataset():
    """Download TMDB 5000 dataset from Kaggle or alternative source"""
    
    print("=" * 60)
    print("TMDB 5000 Movie Dataset Downloader")
    print("=" * 60)
    
    # Try multiple sources
    sources = [
        {
            'name': 'Kaggle Direct (via kaggle.com)',
            'url': 'https://www.kaggle.com/api/v1/datasets/download/tmdb/tmdb-movie-metadata',
            'requires_auth': True
        },
        {
            'name': 'GitHub Mirror',
            'url': 'https://raw.githubusercontent.com/rounakbanik/movies/master/movies.csv',
            'requires_auth': False
        },
    ]
    
    # Check if kaggle.json exists
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    has_kaggle_auth = os.path.exists(kaggle_json_path)
    
    if has_kaggle_auth:
        print("\n✓ Kaggle authentication found!")
        print("  Attempting to download from Kaggle...")
        try:
            import kaggle
            kaggle.api.dataset_download_files('tmdb/tmdb-movie-metadata', path='.', unzip=True)
            print("✓ Successfully downloaded TMDB 5000 dataset!")
            print("\nFiles downloaded:")
            for file in os.listdir('.'):
                if file.endswith('.csv'):
                    size_mb = os.path.getsize(file) / (1024 * 1024)
                    print(f"  - {file} ({size_mb:.2f} MB)")
            return True
        except Exception as e:
            print(f"✗ Kaggle download failed: {e}")
            print("  Trying alternative method...\n")
    else:
        print("\n⚠ Kaggle authentication not found")
        print("  To use Kaggle API:")
        print("  1. Go to https://www.kaggle.com/settings/account")
        print("  2. Click 'Create New API Token'")
        print("  3. Place kaggle.json in ~/.kaggle/kaggle.json")
        print("\n  Trying GitHub mirror...\n")
    
    # Try GitHub mirror (The Movies Dataset)
    print("📥 Downloading from GitHub mirror...")
    try:
        github_url = 'https://raw.githubusercontent.com/rounakbanik/the-movies-dataset/master/movies_metadata.csv'
        print(f"   URL: {github_url}")
        urllib.request.urlretrieve(github_url, 'movies_metadata.csv')
        print("✓ Successfully downloaded movies_metadata.csv!")
        
        # Get file size
        size_mb = os.path.getsize('movies_metadata.csv') / (1024 * 1024)
        print(f"   Size: {size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print(f"✗ GitHub download failed: {e}")
    
    print("\n" + "=" * 60)
    print("Alternative: Manual Download")
    print("=" * 60)
    print("\nYou can manually download from:")
    print("1. Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
    print("2. GitHub: https://github.com/rounakbanik/the-movies-dataset")
    print("3. Zenodo: https://zenodo.org/record/848809")
    print("\nThen place the CSV file in this directory")
    return False

if __name__ == "__main__":
    success = download_tmdb_dataset()
    
    if success:
        print("\n" + "=" * 60)
        print("Next steps:")
        print("=" * 60)
        print("\nEdit run_pipeline.py and use:")
        print("  run_etl_pipeline(source='csv', csv_path='movies_metadata.csv')")
        print("\nOr update the configuration to:")
        print("  source='kaggle'")
        print("  dataset_name='tmdb/tmdb-movie-metadata'")
        print("  csv_file_name='tmdb_5000_movies.csv'")
    else:
        print("\n⚠ Could not download automatically")
        print("Please download manually and retry")
