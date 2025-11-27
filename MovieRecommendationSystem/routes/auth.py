from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: authenticate
        return redirect(url_for('movies.index'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # TODO: create user
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    # TODO: logout
    return redirect(url_for('movies.index'))
