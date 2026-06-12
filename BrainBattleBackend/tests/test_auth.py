"""
=============================================================
  Brain Battle – Backend Unit & Functional Tests: AUTH
=============================================================
  Coverage:
    ✅ TC-AUTH-001  Signup with valid data           → 201
    ✅ TC-AUTH-002  Signup with missing fields       → 400
    ✅ TC-AUTH-003  Signup with duplicate email      → 409
    ✅ TC-AUTH-004  Login with valid credentials     → 200
    ✅ TC-AUTH-005  Login with wrong password        → 401
    ✅ TC-AUTH-006  Login with unknown email         → 404
    ✅ TC-AUTH-007  Login with empty body            → 400
    ✅ TC-AUTH-008  Signup no JSON body              → 400
"""

import pytest
import sys
import os

# Make the project root importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BrainBattleBackend'))

from app import create_app
from database.db import db as _db


# ─────────────────────────── Fixtures ────────────────────────────

@pytest.fixture(scope='session')
def app():
    """Create a test Flask application with an in-memory SQLite DB."""
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
    """Wipe tables between every test so tests are independent."""
    with app.app_context():
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
    yield


# ─────────────────────── Helper ───────────────────────────────────

def signup(client, username='TestUser', email='test@example.com', password='Pass1234'):
    return client.post('/api/auth/signup',
                       json={'username': username, 'email': email, 'password': password})


def login(client, email='test@example.com', password='Pass1234'):
    return client.post('/api/auth/login',
                       json={'email': email, 'password': password})


# ═══════════════════════ SIGNUP TESTS ═══════════════════════════

class TestSignup:

    def test_tc_auth_001_signup_valid(self, client):
        """TC-AUTH-001: Valid signup returns 201 + success status."""
        res = signup(client)
        assert res.status_code == 201
        data = res.get_json()
        assert data['status'] == 'success'
        assert 'registered' in data['message'].lower()

    def test_tc_auth_002_signup_missing_username(self, client):
        """TC-AUTH-002a: Missing username returns 400."""
        res = client.post('/api/auth/signup',
                          json={'email': 'x@x.com', 'password': 'abc123'})
        assert res.status_code == 400
        assert res.get_json()['status'] == 'error'

    def test_tc_auth_002_signup_missing_email(self, client):
        """TC-AUTH-002b: Missing email returns 400."""
        res = client.post('/api/auth/signup',
                          json={'username': 'Alice', 'password': 'abc123'})
        assert res.status_code == 400

    def test_tc_auth_002_signup_missing_password(self, client):
        """TC-AUTH-002c: Missing password returns 400."""
        res = client.post('/api/auth/signup',
                          json={'username': 'Alice', 'email': 'x@x.com'})
        assert res.status_code == 400

    def test_tc_auth_003_signup_duplicate_email(self, client):
        """TC-AUTH-003: Duplicate email returns 409 conflict."""
        signup(client)                          # first registration
        res = signup(client)                    # second with same email
        assert res.status_code == 409
        assert res.get_json()['status'] == 'error'

    def test_tc_auth_008_signup_no_json(self, client):
        """TC-AUTH-008: No JSON body returns 400."""
        res = client.post('/api/auth/signup', data='not json',
                          content_type='text/plain')
        assert res.status_code == 400


# ═══════════════════════ LOGIN TESTS ════════════════════════════

class TestLogin:

    def test_tc_auth_004_login_valid(self, client):
        """TC-AUTH-004: Valid login returns 200 + username + email."""
        signup(client)
        res = login(client)
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'success'
        assert data['username'] == 'TestUser'
        assert data['email'] == 'test@example.com'

    def test_tc_auth_005_login_wrong_password(self, client):
        """TC-AUTH-005: Wrong password returns 401."""
        signup(client)
        res = login(client, password='WrongPass!')
        assert res.status_code == 401
        assert res.get_json()['status'] == 'error'

    def test_tc_auth_006_login_unknown_email(self, client):
        """TC-AUTH-006: Non-existent email returns 404."""
        res = login(client, email='nobody@unknown.com')
        assert res.status_code == 404
        assert res.get_json()['status'] == 'error'

    def test_tc_auth_007_login_empty_body(self, client):
        """TC-AUTH-007: Empty / missing fields returns 400."""
        res = client.post('/api/auth/login', json={})
        assert res.status_code == 400
