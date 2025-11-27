#!/usr/bin/env python3
"""
Standalone downloader for TMDB 5000 Movie Dataset
No dependencies on the Flask app
"""
import os
import sys
import urllib.request
import json

def download_tmdb_dataset():
    """Download TMDB 5000 dataset from multiple sources"""
    
    print("=" * 70)
    print("TMDB 5000 Movie Dataset Downloader")
    print("=" * 70)
    
    # Check if kaggle.json exists for API download
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    has_kaggle_auth = os.path.exists(kaggle_json_path)
    
    if has_kaggle_auth:
        print("\n✓ Kaggle credentials found!")
        print("  Attempting Kaggle API download...")
        try:
            # Try importing only when needed
            import kaggle
            print("  📥 Downloading tmdb-movie-metadata...")
            kaggle.api.dataset_download_files('tmdb/tmdb-movie-metadata', path='.', unzip=True)
            
            print("\n✓ Download successful!")
            print("\nFiles in directory:")
            for file in os.listdir('.'):
                if file.endswith('.csv'):
                    size_mb = os.path.getsize(file) / (1024 * 1024)
                    print(f"  ✓ {file} ({size_mb:.2f} MB)")
            return True
        except ImportError:
            print("  ✗ Kaggle library not installed")
            print("  Install with: pip install kaggle")
        except Exception as e:
            print(f"  ✗ Kaggle download failed: {str(e)[:100]}")
    else:
        print("\n⚠ No Kaggle credentials found")
        print("  (Optional) Set up Kaggle API:")
        print("  1. Visit: https://www.kaggle.com/settings/account")
        print("  2. Click 'Create New API Token'")
        print("  3. Save to: ~/.kaggle/kaggle.json")
    
    # Try GitHub mirror - The Movies Dataset
    print("\n📥 Downloading from GitHub mirror...")
    print("  (This contains 45,000+ movies from TMDB)")
    
    try:
        github_url = 'https://raw.githubusercontent.com/rounakbanik/the-movies-dataset/master/movies_metadata.csv'
        print(f"  Source: GitHub rounakbanik/the-movies-dataset")
        print(f"  Downloading... (this may take 1-2 minutes)")
        
        # Download with progress
        class ProgressBar(urllib.request.urlretrieve):
            def __call__(self, blocknum, blocksize, totalsize):
                if totalsize > 0:
                    percent = min(blocknum * blocksize, totalsize) / totalsize
                    print(f"\r  Progress: {percent*100:.1f}%", end='', flush=True)
        
        urllib.request.urlretrieve(github_url, 'movies_metadata.csv')
        print("\n\n✓ Download successful!")
        
        size_mb = os.path.getsize('movies_metadata.csv') / (1024 * 1024)
        print(f"\nFile: movies_metadata.csv ({size_mb:.2f} MB)")
        
        # Check file
        with open('movies_metadata.csv', 'r', encoding='utf-8', errors='ignore') as f:
            lines = len(f.readlines())
            print(f"Records: ~{lines-1:,} movies")
        
        return True
    except Exception as e:
        print(f"\n✗ GitHub download failed: {str(e)}")
    
    print("\n" + "=" * 70)
    print("MANUAL DOWNLOAD OPTIONS")
    print("=" * 70)
    print("\nIf automatic download fails, download manually from:")
    print("\n1. TMDB 5000 on Kaggle:")
    print("   https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
    print("   Files: tmdb_5000_movies.csv, tmdb_5000_credits.csv")
    
    print("\n2. The Movies Dataset on Kaggle (45K+ movies):")
    print("   https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset")
    print("   File: movies_metadata.csv")
    
    print("\n3. GitHub Mirror:")
    print("   https://github.com/rounakbanik/the-movies-dataset")
    print("   Raw CSV: https://raw.githubusercontent.com/rounakbanik/the-movies-dataset/master/movies_metadata.csv")
    
    print("\nAfter download, place CSV in this directory:")
    print(f"  {os.getcwd()}")
    
    return False

if __name__ == "__main__":
    try:
        success = download_tmdb_dataset()
        
        if success:
            print("\n" + "=" * 70)
            print("NEXT STEPS")
            print("=" * 70)
            print("\n1. Update run_pipeline.py to use the downloaded CSV:")
            print("   run_etl_pipeline(source='csv', csv_path='movies_metadata.csv')")
            print("\n2. Delete old database:")
            print("   rm instance/movies.db  (or delete manually)")
            print("\n3. Run the ETL pipeline:")
            print("   python etl_pipeline/run_pipeline.py")
            print("\n4. Start Flask app:")
            print("   python app.py")
            
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
