from flask import Blueprint, request, jsonify
from database.db import db
from models.progress_model import UserProgress

progress_bp = Blueprint("progress", __name__)


# ✅ SAVE PROGRESS
@progress_bp.route("/save", methods=["POST"])
def save_progress():

    data = request.get_json()

    email = data.get("email")
    game_type = data.get("game_type")
    level = data.get("level")
    stars = data.get("stars")
    time_taken = data.get("time_taken")

    progress = UserProgress.query.filter_by(
        email=email,
        game_type=game_type,
        level=level
    ).first()

    if progress:
        progress.stars = stars
        progress.time_taken = time_taken
        progress.is_completed = True

    else:
        progress = UserProgress(
            email=email,
            game_type=game_type,
            level=level,
            stars=stars,
            time_taken=time_taken,
            is_completed=True
        )
        db.session.add(progress)

    db.session.commit()

    return jsonify({"status": "success"})


# ✅ GET PROGRESS (THIS WAS MISSING)
@progress_bp.route("/get/<email>/<game>", methods=["GET"])
def get_progress(email, game):

    rows = UserProgress.query.filter_by(
        email=email,
        game_type=game
    ).all()

    result = []

    for r in rows:
        result.append({
            "level": r.level,
            "stars": r.stars,
            "completed": r.is_completed
        })

    return jsonify(result)