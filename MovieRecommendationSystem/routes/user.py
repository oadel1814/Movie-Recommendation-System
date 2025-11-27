from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from database.db import db
from database.models import Watchlist, Movie
from config import Config

user_bp = Blueprint('user', __name__)

@user_bp.route('/watchlist')
@login_required
def watchlist():
    watchlist_items = Watchlist.query.filter_by(
        user_id=current_user.id
    ).order_by(Watchlist.added_at.desc()).all()
    
    movies = [item.movie for item in watchlist_items if item.movie]
    
    return render_template('watchlist.html', movies=movies, watchlist_items=watchlist_items)

@user_bp.route('/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist():
    data = request.get_json()
    movie_id = data.get('movie_id')
    
    if not movie_id:
        return jsonify({'success': False, 'message': 'Movie ID required'}), 400
    
    # Check if already in watchlist
    existing = Watchlist.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Already in watchlist'}), 400
    
    # Add to watchlist
    watchlist_item = Watchlist(user_id=current_user.id, movie_id=movie_id)
    
    try:
        db.session.add(watchlist_item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Added to watchlist'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@user_bp.route('/watchlist/remove', methods=['POST'])
@login_required
def remove_from_watchlist():
    data = request.get_json()
    movie_id = data.get('movie_id')
    
    if not movie_id:
        return jsonify({'success': False, 'message': 'Movie ID required'}), 400
    
    watchlist_item = Watchlist.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if not watchlist_item:
        return jsonify({'success': False, 'message': 'Not in watchlist'}), 404
    
    try:
        db.session.delete(watchlist_item)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Removed from watchlist'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@user_bp.route('/watchlist/toggle-watched', methods=['POST'])
@login_required
def toggle_watched():
    data = request.get_json()
    movie_id = data.get('movie_id')
    
    watchlist_item = Watchlist.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first()
    
    if not watchlist_item:
        return jsonify({'success': False, 'message': 'Not in watchlist'}), 404
    
    try:
        watchlist_item.watched = not watchlist_item.watched
        db.session.commit()
        return jsonify({
            'success': True,
            'watched': watchlist_item.watched
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@user_bp.route('/recommendations')
@login_required
def recommendations():
    from app import recommendation_engine
    
    if not recommendation_engine or not recommendation_engine.is_fitted:
        flash('Recommendation engine not ready. Please try again later.', 'warning')
        return redirect(url_for('movies.index'))
    
    # Get personalized recommendations
    recommended = recommendation_engine.get_recommendations_for_user(
        current_user.id,
        top_n=Config.TOP_N_RECOMMENDATIONS
    )
    
    movies = [movie for movie, score in recommended]
    
    return render_template('recommendations.html', movies=movies)

@user_bp.route('/check-watchlist/<int:movie_id>')
@login_required
def check_watchlist(movie_id):
    exists = Watchlist.query.filter_by(
        user_id=current_user.id,
        movie_id=movie_id
    ).first() is not None
    
    return jsonify({'in_watchlist': exists})