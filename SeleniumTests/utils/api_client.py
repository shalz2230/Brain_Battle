"""
SeleniumTests/utils/api_client.py
===================================
Centralised HTTP client for Brain Battle Flask backend.
Used by all Selenium test modules (Python + requests).
"""
import requests

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT  = 10


class ApiClient:

    @staticmethod
    def signup(username=None, email=None, password=None):
        payload = {}
        if username is not None: payload["username"] = username
        if email    is not None: payload["email"]    = email
        if password is not None: payload["password"] = password
        return requests.post(f"{BASE_URL}/api/auth/signup", json=payload, timeout=TIMEOUT)

    @staticmethod
    def login(email=None, password=None):
        payload = {}
        if email    is not None: payload["email"]    = email
        if password is not None: payload["password"] = password
        return requests.post(f"{BASE_URL}/api/auth/login", json=payload, timeout=TIMEOUT)

    @staticmethod
    def get_user(email):
        return requests.post(f"{BASE_URL}/api/user/get-user", json={"email": email}, timeout=TIMEOUT)

    @staticmethod
    def forgot_password(email):
        return requests.post(f"{BASE_URL}/api/user/forgot-password", json={"email": email}, timeout=TIMEOUT)

    @staticmethod
    def change_password(email, password):
        return requests.post(f"{BASE_URL}/api/user/change-password",
                             json={"email": email, "password": password}, timeout=TIMEOUT)

    @staticmethod
    def save_progress(email, game_type, level, stars, time_taken):
        return requests.post(f"{BASE_URL}/api/progress/save",
                             json={"email": email, "game_type": game_type,
                                   "level": level, "stars": stars,
                                   "time_taken": time_taken}, timeout=TIMEOUT)

    @staticmethod
    def get_progress(email, game_type):
        return requests.get(f"{BASE_URL}/api/progress/get/{email}/{game_type}", timeout=TIMEOUT)

    @staticmethod
    def get_dashboard(email):
        return requests.get(f"{BASE_URL}/api/dashboard/{email}", timeout=TIMEOUT)


import uuid, time as _time
def random_email():
    return f"sel_{uuid.uuid4().hex[:8]}@brainbattle.com"
