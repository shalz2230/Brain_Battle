from flask import Blueprint, request, jsonify
from database.db import db
from models.user_model import User
from utils.hash_utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

# ---------------- SIGNUP ----------------
@auth_bp.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid request"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # validation
    if not username or not email or not password:
        return jsonify({
            "status": "error",
            "message": "All fields required"
        }), 400

    # check existing user
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 409

    # hash password
    hashed_password = hash_password(password)

    # create user
    new_user = User(username, email, hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully"
    }), 201


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid request"
        }), 400

    email = data.get("email")
    password = data.get("password")

    # validation
    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password required"
        }), 400

    # check user
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    # verify password
    if not verify_password(user.password, password):
        return jsonify({
            "status": "error",
            "message": "Invalid password"
        }), 401

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "username": user.username,
        "email": user.email
    }), 200