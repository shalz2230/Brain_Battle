"""
SeleniumTests/tests/test_01_auth.py
=====================================
Selenium-style E2E Web API Tests – Authentication (Signup & Login)
Framework : Python pytest + requests
TC-AUTH-001 … TC-AUTH-012
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.api_client import ApiClient, random_email


# ─── Shared test email for duplicate tests ─────────────────────
@pytest.fixture(scope="module")
def registered_email():
    email = random_email()
    ApiClient.signup(username="AuthUser", email=email, password="AuthPass99")
    return email


class TestSignup:
    """TC-AUTH-001..007: Signup endpoint tests"""

    def test_tc_auth_001_valid_signup_returns_201(self):
        """TC-AUTH-001: Valid signup data returns HTTP 201 Created."""
        res = ApiClient.signup("NewUser", random_email(), "Pass1234")
        assert res.status_code == 201
        assert res.json().get("status") == "success"

    def test_tc_auth_002_signup_response_message_non_empty(self):
        """TC-AUTH-002: Signup response contains a non-empty message."""
        res = ApiClient.signup("NewUser2", random_email(), "Pass1234")
        assert res.status_code == 201
        msg = res.json().get("message", "")
        assert isinstance(msg, str) and len(msg) > 0

    def test_tc_auth_003_signup_missing_username_returns_400(self):
        """TC-AUTH-003: Signup with missing username returns HTTP 400."""
        res = ApiClient.signup(email=random_email(), password="Pass1234")
        assert res.status_code == 400
        assert res.json().get("status") == "error"

    def test_tc_auth_004_signup_missing_email_returns_400(self):
        """TC-AUTH-004: Signup with missing email returns HTTP 400."""
        res = ApiClient.signup(username="Alice", password="Pass1234")
        assert res.status_code == 400

    def test_tc_auth_005_signup_missing_password_returns_400(self):
        """TC-AUTH-005: Signup with missing password returns HTTP 400."""
        res = ApiClient.signup(username="Alice", email=random_email())
        assert res.status_code == 400

    def test_tc_auth_006_duplicate_email_returns_409(self, registered_email):
        """TC-AUTH-006: Duplicate email returns HTTP 409 Conflict."""
        res = ApiClient.signup("DupUser", registered_email, "AnyPass")
        assert res.status_code == 409
        assert res.json().get("status") == "error"

    def test_tc_auth_007_empty_body_returns_400(self):
        """TC-AUTH-007: Signup with empty JSON body returns HTTP 400."""
        import requests
        res = requests.post("http://127.0.0.1:5000/api/auth/signup",
                            json={}, timeout=10)
        assert res.status_code == 400


class TestLogin:
    """TC-AUTH-008..012: Login endpoint tests"""

    @pytest.fixture(scope="class")
    def login_user(self):
        email = random_email()
        ApiClient.signup("LoginUser", email, "LoginPass99")
        return {"email": email, "password": "LoginPass99"}

    def test_tc_auth_008_valid_login_returns_200(self, login_user):
        """TC-AUTH-008: Valid credentials return HTTP 200."""
        res = ApiClient.login(login_user["email"], login_user["password"])
        assert res.status_code == 200
        assert res.json().get("status") == "success"

    def test_tc_auth_009_login_response_has_username_and_email(self, login_user):
        """TC-AUTH-009: Login response body contains username and email."""
        res = ApiClient.login(login_user["email"], login_user["password"])
        data = res.json()
        assert "username" in data and isinstance(data["username"], str)
        assert "email" in data and data["email"] == login_user["email"]

    def test_tc_auth_010_wrong_password_returns_401(self, login_user):
        """TC-AUTH-010: Wrong password returns HTTP 401 Unauthorized."""
        res = ApiClient.login(login_user["email"], "WrongPassword!")
        assert res.status_code == 401
        assert res.json().get("status") == "error"

    def test_tc_auth_011_unknown_email_returns_404(self):
        """TC-AUTH-011: Unknown email returns HTTP 404 Not Found."""
        res = ApiClient.login("nobody@unknown.com", "anypass")
        assert res.status_code == 404

    def test_tc_auth_012_empty_body_returns_400(self):
        """TC-AUTH-012: Login with empty body returns HTTP 400."""
        import requests
        res = requests.post("http://127.0.0.1:5000/api/auth/login",
                            json={}, timeout=10)
        assert res.status_code == 400
