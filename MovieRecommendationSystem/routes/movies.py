from flask import Blueprint, render_template

movies_bp = Blueprint('movies', __name__, template_folder='../templates')

@movies_bp.route('/')
def index():
    # TODO: list movies from DB
    return render_template('index.html')

@movies_bp.route('/movies/<int:movie_id>')
def detail(movie_id):
    # TODO: fetch movie details
    return render_template('index.html')
