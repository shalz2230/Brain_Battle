"""
=============================================================
  Brain Battle – Backend Unit & Functional Tests: USER
=============================================================
  Coverage:
    ✅ TC-USR-001  Get user by valid email            → 200
    ✅ TC-USR-002  Get user with unknown email        → 404
    ✅ TC-USR-003  Forgot password valid email        → 200
    ✅ TC-USR-004  Forgot password unknown email      → 404
    ✅ TC-USR-005  Change password valid user         → 200
    ✅ TC-USR-006  Change password unknown user       → 404
    ✅ TC-USR-007  Password is actually hashed in DB  (unit)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BrainBattleBackend'))

from app import create_app
from database.db import db as _db
from models.user_model import User
from utils.hash_utils import hash_password, verify_password


# ─────────────────────────── Fixtures ────────────────────────────

@pytest.fixture(scope='session')
def app():
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
    yield


@pytest.fixture()
def existing_user(app):
    """Seed a pre-registered user for each test that needs one."""
    with app.app_context():
        user = User('Alice', 'alice@example.com', hash_password('Secret99'))
        _db.session.add(user)
        _db.session.commit()
    return {'email': 'alice@example.com', 'password': 'Secret99'}


# ═══════════════════════ GET USER TESTS ══════════════════════════

class TestGetUser:

    def test_tc_usr_001_get_user_valid(self, client, existing_user):
        """TC-USR-001: Known email returns username."""
        res = client.post('/api/user/get-user',
                          json={'email': existing_user['email']})
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'success'
        assert data['username'] == 'Alice'

    def test_tc_usr_002_get_user_unknown(self, client):
        """TC-USR-002: Unknown email returns 404."""
        res = client.post('/api/user/get-user',
                          json={'email': 'ghost@nobody.com'})
        assert res.status_code == 404
        assert res.get_json()['status'] == 'error'


# ═══════════════════ FORGOT PASSWORD TESTS ═══════════════════════

class TestForgotPassword:

    def test_tc_usr_003_forgot_password_valid(self, client, existing_user):
        """TC-USR-003: Valid email returns success."""
        res = client.post('/api/user/forgot-password',
                          json={'email': existing_user['email']})
        assert res.status_code == 200
        assert res.get_json()['status'] == 'success'

    def test_tc_usr_004_forgot_password_unknown(self, client):
        """TC-USR-004: Unknown email returns 404."""
        res = client.post('/api/user/forgot-password',
                          json={'email': 'nobody@x.com'})
        assert res.status_code == 404


# ═══════════════════ CHANGE PASSWORD TESTS ═══════════════════════

class TestChangePassword:

    def test_tc_usr_005_change_password_valid(self, client, existing_user, app):
        """TC-USR-005: Valid email updates password; new password works."""
        res = client.post('/api/user/change-password',
                          json={'email': existing_user['email'],
                                'password': 'NewPass567'})
        assert res.status_code == 200
        assert res.get_json()['status'] == 'success'

        # Verify the new password actually works for login
        login_res = client.post('/api/auth/login',
                                json={'email': existing_user['email'],
                                      'password': 'NewPass567'})
        assert login_res.status_code == 200

    def test_tc_usr_006_change_password_unknown(self, client):
        """TC-USR-006: Non-existent user returns 404."""
        res = client.post('/api/user/change-password',
                          json={'email': 'nobody@x.com', 'password': 'abc'})
        assert res.status_code == 404


# ═════════════════════ UNIT: Hash Utils ══════════════════════════

class TestHashUtils:

    def test_tc_usr_007_password_hashed_in_db(self, app, existing_user):
        """TC-USR-007: Stored password must NOT equal the plaintext."""
        with app.app_context():
            user = User.query.filter_by(email=existing_user['email']).first()
            assert user is not None
            # Raw stored value must NOT be the plain password
            assert user.password != existing_user['password']
            # But verify_password must succeed with the correct plain password
            assert verify_password(user.password, existing_user['password']) is True

    def test_hash_utils_wrong_password_rejected(self, app, existing_user):
        """Verify wrong password fails hash check."""
        with app.app_context():
            user = User.query.filter_by(email=existing_user['email']).first()
            assert verify_password(user.password, 'WrongPassword') is False
