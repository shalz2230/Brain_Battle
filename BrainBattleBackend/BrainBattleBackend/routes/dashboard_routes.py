from flask import Blueprint, jsonify
from models.progress_model import UserProgress

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/<email>", methods=["GET"])
def get_dashboard(email):

    progress = UserProgress.query.filter_by(email=email).all()

    if not progress:
        return jsonify({
            "current_level": 1,
            "total_stars": 0,
            "last_game": "memory",
            "rank": 0,
            "levels_completed": 0
        })

    # ✅ total stars for current user
    total_stars = sum(p.stars for p in progress)

    # ✅ last played game
    last_entry = UserProgress.query.filter_by(email=email)\
        .order_by(UserProgress.id.desc()).first()

    last_game = last_entry.game_type

    # ✅ current level for that game
    game_progress = UserProgress.query.filter_by(
        email=email,
        game_type=last_game
    ).all()

    current_level = max([p.level for p in game_progress], default=1)

    # ✅ levels completed
    levels_completed = len(progress)

    # ==========================
    # 🔥 RANK CALCULATION
    # ==========================

    all_progress = UserProgress.query.all()

    user_totals = {}

    for p in all_progress:
        user_totals[p.email] = user_totals.get(p.email, 0) + p.stars

    # sort by stars DESC
    sorted_users = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)

    rank = 1
    for i, (user_email, _) in enumerate(sorted_users):
        if user_email == email:
            rank = i + 1
            break

    return jsonify({
        "current_level": current_level,
        "total_stars": total_stars,
        "last_game": last_game,
        "rank": rank,
        "levels_completed": levels_completed
    })