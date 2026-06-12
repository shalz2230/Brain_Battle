from flask import Flask
from database.db import db
from config import Config   # ✅ import config

def create_app():
    app = Flask(__name__)

    # ✅ use config.py (absolute DB path)
    app.config.from_object(Config)

    db.init_app(app)

    # import routes AFTER db init
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from routes.progress_routes import progress_bp
    app.register_blueprint(progress_bp, url_prefix='/api/progress')

    from routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/user')

    from routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    return app


app = create_app()

# ✅ create tables automatically (important)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)