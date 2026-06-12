from database.db import db

class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), nullable=False)

    game_type = db.Column(db.String(50), nullable=False)

    level = db.Column(db.Integer, nullable=False)

    stars = db.Column(db.Integer, default=0)

    time_taken = db.Column(db.Integer, default=0)   # ✅ NEW

    is_completed = db.Column(db.Boolean, default=False)