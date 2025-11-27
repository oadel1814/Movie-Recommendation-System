from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, template_folder='../templates')

@user_bp.route('/watchlist')
def watchlist():
    # TODO: display user's watchlist
    return render_template('watchlist.html')

@user_bp.route('/recommendations')
def recommendations():
    # TODO: generate recommendations for the user
    return render_template('recommendations.html')
