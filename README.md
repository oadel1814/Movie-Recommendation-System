# 🎬 Movie Recommender System

A full-stack web application that provides personalized movie recommendations using content-based filtering and machine learning. Built with Flask, SQLAlchemy, and Scikit-learn.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Recommendation Algorithm](#recommendation-algorithm)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### User Features
- 🔐 **User Authentication** - Secure signup/login with password hashing
- 🎥 **Browse Movies** - Explore thousands of movies with poster images
- 🔍 **Real-time Search** - Instant search with autocomplete suggestions
- 📊 **Advanced Filtering** - Filter by genre, sort by popularity/rating/release date
- ⭐ **Watchlist Management** - Add/remove movies, mark as watched
- 🤖 **Smart Recommendations** - AI-powered personalized suggestions
- 🎯 **Similar Movies** - Find movies similar to ones you like
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile

### Technical Features
- 🧠 **Content-Based Filtering** - TF-IDF + Cosine Similarity algorithm
- 🔄 **ETL Pipeline** - Automated data extraction from TMDB API
- 💾 **SQLite Database** - Efficient data storage with SQLAlchemy ORM
- 🎨 **Modern UI/UX** - Netflix-inspired dark theme
- ⚡ **AJAX Requests** - Smooth, non-blocking user interactions
- 🔒 **Session Management** - Secure user sessions with Flask-Login

---

## 🎥 Demo

<img width="1605" height="862" alt="image" src="https://github.com/user-attachments/assets/9c2509f2-458c-414a-8652-03da131b534a" />



## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  CLIENT (Browser)                    │
│           HTML / CSS / JavaScript                    │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP Requests
                       ▼
┌─────────────────────────────────────────────────────┐
│              FLASK APPLICATION                       │
│  ┌────────────┐ ┌──────────┐ ┌─────────────┐      │
│  │   Auth     │ │  Movies  │ │    User     │      │
│  │  Routes    │ │  Routes  │ │   Routes    │      │
│  └────────────┘ └──────────┘ └─────────────┘      │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
┌──────────────┐ ┌─────────┐ ┌──────────────────┐
│  Database    │ │  ML     │ │   ETL Pipeline   │
│  (SQLite)    │ │ Engine  │ │  (TMDB API)      │
│  - Users     │ │ TF-IDF  │ │  Extract         │
│  - Movies    │ │ Cosine  │ │  Transform       │
│  - Watchlist │ │ Sim     │ │  Load            │
└──────────────┘ └─────────┘ └──────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Flask** 3.0.0 - Web framework
- **SQLAlchemy** 3.1.1 - ORM for database operations
- **Flask-Login** 0.6.3 - User session management
- **Werkzeug** 3.0.1 - Password hashing & utilities

### Machine Learning
- **Scikit-learn** 1.3.2 - TF-IDF vectorization & cosine similarity
- **Pandas** 2.1.4 - Data manipulation
- **NumPy** 1.26.2 - Numerical computations

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Custom, no frameworks)
- **Vanilla JavaScript** - Interactivity (No jQuery)
- **AJAX** - Asynchronous requests

### Data Source
- **TMDB API** - Movie data provider

### Database
- **SQLite** - Lightweight, serverless database

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- TMDB API Key (free registration)

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
```

#### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Get TMDB API Key

1. Visit [https://www.themoviedb.org/](https://www.themoviedb.org/)
2. Create a free account
3. Go to Settings → API
4. Request an API key (choose "Developer")
5. Copy your API key

#### 5. Configure Environment Variables

**Option A: Using .env file (Recommended)**

Create a `.env` file in the project root:

```bash
# .env
TMDB_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option B: Direct configuration**

Edit `config.py`:

```python
TMDB_API_KEY = 'your_actual_api_key_here'
SECRET_KEY = 'your_generated_secret_key_here'
```

#### 6. Run ETL Pipeline (Populate Database)

```bash
python etl_pipeline/run_pipeline.py
```

**Expected Output:**
```
==================================================
Starting ETL Pipeline
==================================================

[1/3] EXTRACTING DATA FROM TMDB...
Fetching page 1...
Fetching page 2...
...
Total movies extracted: 200

[2/3] TRANSFORMING DATA...
Transformed 198 movies

[3/3] LOADING DATA TO DATABASE...
Processed 50 movies...
Processed 100 movies...
Load complete: 198 inserted, 0 updated

==================================================
ETL Pipeline Complete!
Total movies in database: 198
==================================================
```

⏱️ **Time**: ~2-3 minutes for 200 movies

#### 7. Run the Application

```bash
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
Recommendation engine initialized
```

#### 8. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TMDB_API_KEY` | Your TMDB API key | - | ✅ Yes |
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key...` | ✅ Yes (Production) |
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `sqlite:///movies.db` | ❌ No |
| `MOVIES_PER_PAGE` | Pagination size | `20` | ❌ No |
| `TOP_N_RECOMMENDATIONS` | Number of recommendations | `10` | ❌ No |

### ETL Pipeline Configuration

Edit `etl_pipeline/run_pipeline.py`:

```python
# Fetch more movies (more data = better recommendations)
run_etl_pipeline(pages=10)  # Fetches 200 movies

# For production:
run_etl_pipeline(pages=50)  # Fetches 1000 movies
```

**Trade-offs:**
- More movies = Better recommendations but slower initial load
- Fewer movies = Faster setup but limited content

### Recommendation Engine Tuning

Edit `recommender/preprocess.py`:

```python
self.vectorizer = TfidfVectorizer(
    max_features=5000,      # Vocabulary size (increase for more precision)
    stop_words='english',   # Remove common words
    ngram_range=(1, 2)      # Use 1-word and 2-word phrases
)
```

---

## 🚀 Usage

### First-Time User Flow

#### 1. **Sign Up**
```
Navigate to: http://localhost:5000/signup

Fill in:
- Username: john_doe
- Email: john@example.com
- Password: ********
- Confirm Password: ********

Click "Sign Up"
```

#### 2. **Log In**
```
Navigate to: http://localhost:5000/login

Enter credentials and click "Login"
```

#### 3. **Browse Movies**
```
Home page displays movies automatically

Use filters:
- Sort by: Popular / Top Rated / Recent
- Genre: Action / Comedy / Drama / etc.
```

#### 4. **Search for Movies**
```
Type in the search bar: "Matrix"

Results appear instantly:
- The Matrix (1999)
- The Matrix Reloaded (2003)
- The Matrix Revolutions (2003)
```

#### 5. **Add to Watchlist**
```
Click "+ Watchlist" button on any movie card

Button changes to "✓ In Watchlist"
Toast notification: "Added to watchlist"
```

#### 6. **View Watchlist**
```
Navigate to: http://localhost:5000/watchlist

See all
