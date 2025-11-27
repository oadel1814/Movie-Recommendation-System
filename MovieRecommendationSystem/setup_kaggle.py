"""
Script to download and setup Kaggle movie dataset with 5000+ movies
"""
import os
import sys

def setup_kaggle_dataset():
    """Download TMDB 5000 movies dataset from Kaggle"""
    
    try:
        import kaggle
        print("✓ Kaggle library is installed")
    except ImportError:
        print("✗ Kaggle not installed. Installing...")
        os.system("pip install kaggle")
        import kaggle
    
    # Check kaggle.json
    kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_json_path):
        print("\n⚠ kaggle.json not found!")
        print("Please:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Click 'Create New API Token'")
        print("3. Place kaggle.json in: ~/.kaggle/kaggle.json")
        print("4. Run this script again")
        return False
    
    print("✓ kaggle.json found")
    
    # Download dataset
    dataset_name = "tmdb-movie-metadata"
    print(f"\n📥 Downloading dataset: {dataset_name}...")
    
    try:
        kaggle.api.dataset_download_files(dataset_name, path='.', unzip=True)
        print(f"✓ Dataset downloaded successfully")
        
        # List files
        files = [f for f in os.listdir('.') if f.endswith('.csv')]
        print(f"\n📄 CSV files found:")
        for f in files:
            print(f"  - {f}")
        
        return True
    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")
        print("\nMake sure:")
        print("1. Your Kaggle account has accepted the dataset terms")
        print("2. Your kaggle.json is properly configured")
        return False

if __name__ == "__main__":
    success = setup_kaggle_dataset()
    sys.exit(0 if success else 1)
