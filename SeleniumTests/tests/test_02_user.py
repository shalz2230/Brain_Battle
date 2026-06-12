"""
SeleniumTests/tests/test_02_user.py
=====================================
Selenium-style E2E Web API Tests – User Management
TC-USR-001 … TC-USR-012
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.api_client import ApiClient, random_email


class TestGetUser:
    """TC-USR-001..003: Get user endpoint"""

    @pytest.fixture(scope="class")
    def user(self):
        email = random_email()
        ApiClient.signup("TestUser", email, "UserPass99")
        return {"email": email, "username": "TestUser"}

    def test_tc_usr_001_valid_email_returns_200_with_username(self, user):
        """TC-USR-001: Valid email returns 200 + correct username."""
        res = ApiClient.get_user(user["email"])
        assert res.status_code == 200
        assert res.json().get("status") == "success"
        assert res.json().get("username") == user["username"]

    def test_tc_usr_002_response_has_username_field(self, user):
        """TC-USR-002: Response JSON contains 'username' string field."""
        res = ApiClient.get_user(user["email"])
        assert isinstance(res.json().get("username"), str)

    def test_tc_usr_003_unknown_email_returns_404(self):
        """TC-USR-003: Unknown email returns HTTP 404."""
        res = ApiClient.get_user("nobody@nobody.com")
        assert res.status_code == 404
        assert res.json().get("status") == "error"


class TestForgotPassword:
    """TC-USR-004..006: Forgot password endpoint"""

    @pytest.fixture(scope="class")
    def user_email(self):
        email = random_email()
        ApiClient.signup("ForgotUser", email, "OldPass99")
        return email

    def test_tc_usr_004_registered_email_returns_200(self, user_email):
        """TC-USR-004: Registered email returns HTTP 200."""
        res = ApiClient.forgot_password(user_email)
        assert res.status_code == 200
        assert res.json().get("status") == "success"

    def test_tc_usr_005_response_message_is_non_empty(self, user_email):
        """TC-USR-005: Response message is non-empty string."""
        res = ApiClient.forgot_password(user_email)
        msg = res.json().get("message", "")
        assert isinstance(msg, str) and len(msg) > 0

    def test_tc_usr_006_unregistered_email_returns_404(self):
        """TC-USR-006: Unregistered email returns HTTP 404."""
        res = ApiClient.forgot_password("ghost@nobody.com")
        assert res.status_code == 404


class TestChangePassword:
    """TC-USR-007..012: Change password endpoint"""

    @pytest.fixture(scope="class")
    def user(self):
        email    = random_email()
        old_pass = "OldSecret77"
        new_pass = "NewSecret88"
        ApiClient.signup("ChangeUser", email, old_pass)
        return {"email": email, "old_pass": old_pass, "new_pass": new_pass}

    def test_tc_usr_007_valid_change_returns_200(self, user):
        """TC-USR-007: Change password for valid user returns HTTP 200."""
        res = ApiClient.change_password(user["email"], user["new_pass"])
        assert res.status_code == 200
        assert res.json().get("status") == "success"

    def test_tc_usr_008_new_password_works_for_login(self, user):
        """TC-USR-008: New password can be used to login successfully."""
        res = ApiClient.login(user["email"], user["new_pass"])
        assert res.status_code == 200

    def test_tc_usr_009_old_password_rejected_after_change(self, user):
        """TC-USR-009: Old password is rejected (401) after password change."""
        res = ApiClient.login(user["email"], user["old_pass"])
        assert res.status_code == 401

    def test_tc_usr_010_unknown_user_returns_404(self):
        """TC-USR-010: Change password for unknown email returns 404."""
        res = ApiClient.change_password("nobody@bb.com", "anypass")
        assert res.status_code == 404

    def test_tc_usr_011_response_has_success_message_string(self):
        """TC-USR-011: Successful change has non-empty message."""
        email = random_email()
        ApiClient.signup("TmpUser", email, "OldP99")
        res = ApiClient.change_password(email, "NewP99")
        assert isinstance(res.json().get("message"), str)

    def test_tc_usr_012_login_after_change_returns_username(self, user):
        """TC-USR-012: Login after change returns correct username in response."""
        res = ApiClient.login(user["email"], user["new_pass"])
        assert res.json().get("username") == "ChangeUser"
