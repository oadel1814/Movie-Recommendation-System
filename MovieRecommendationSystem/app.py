from flask import Flask
from config import SECRET_KEY
from database.db import init_db
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.user import user_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    # initialize database WITH app context
    init_db(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(user_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
