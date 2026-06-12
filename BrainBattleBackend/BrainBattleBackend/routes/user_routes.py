from flask import Blueprint, request, jsonify
from database.db import db
from models.user_model import User
from utils.hash_utils import hash_password   # ⭐ ADD THIS

user_bp = Blueprint('user_bp', __name__)


# ---------------- GET USER ----------------
@user_bp.route('/get-user', methods=['POST'])
def get_user():

    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "status": "success",
            "username": user.username
        })
    else:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404


# ---------------- FORGOT PASSWORD ----------------
@user_bp.route('/forgot-password', methods=['POST'])
def forgot_password():

    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "status": "success",
            "message": "Email verified"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Email not found"
        }), 404


# ---------------- CHANGE PASSWORD ----------------
@user_bp.route('/change-password', methods=['POST'])
def change_password():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user:

        # ⭐ HASH THE PASSWORD BEFORE SAVING
        user.password = hash_password(password)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Password updated"
        })

    else:

        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404