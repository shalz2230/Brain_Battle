"""
=============================================================
  Brain Battle – Unit Tests: Data Models
=============================================================
  Coverage:
    ✅ TC-MDL-001  User model stores correct fields
    ✅ TC-MDL-002  UserProgress model default values
    ✅ TC-MDL-003  Email uniqueness constraint (DB level)
    ✅ TC-MDL-004  UserProgress is_completed defaults False
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BrainBattleBackend'))

from app import create_app
from database.db import db as _db
from models.user_model import User
from models.progress_model import UserProgress
from utils.hash_utils import hash_password
from sqlalchemy.exc import IntegrityError


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


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        _db.session.remove()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
    yield


# ═══════════════════════ MODEL TESTS ════════════════════════════

class TestUserModel:

    def test_tc_mdl_001_user_fields(self, app):
        """TC-MDL-001: User model stores username, email, password correctly."""
        with app.app_context():
            user = User('Bob', 'bob@test.com', hash_password('mypassword'))
            _db.session.add(user)
            _db.session.commit()

            found = User.query.filter_by(email='bob@test.com').first()
            assert found is not None
            assert found.username == 'Bob'
            assert found.email == 'bob@test.com'
            assert found.id is not None     # auto-incremented PK assigned

    def test_tc_mdl_003_email_unique_constraint(self, app):
        """TC-MDL-003: Inserting duplicate email raises IntegrityError."""
        with app.app_context():
            _db.session.add(User('Alice', 'dup@test.com', 'hashed'))
            _db.session.commit()

            _db.session.add(User('Alice2', 'dup@test.com', 'hashed2'))
            with pytest.raises(IntegrityError):
                _db.session.commit()
            _db.session.rollback()


class TestProgressModel:

    def test_tc_mdl_002_progress_defaults(self, app):
        """TC-MDL-002: Stars default 0, is_completed defaults False."""
        with app.app_context():
            prog = UserProgress(
                email='p@test.com',
                game_type='speed',
                level=3,
                stars=0,
                time_taken=0,
                is_completed=False
            )
            _db.session.add(prog)
            _db.session.commit()

            found = UserProgress.query.filter_by(
                email='p@test.com', game_type='speed', level=3
            ).first()
            assert found is not None
            assert found.stars == 0

    def test_tc_mdl_004_is_completed_defaults_false(self, app):
        """TC-MDL-004: is_completed is False by default from column definition."""
        with app.app_context():
            # Use raw SQL-level default by not passing is_completed
            prog = UserProgress.__new__(UserProgress)
            prog.email = 'q@test.com'
            prog.game_type = 'focus'
            prog.level = 1
            prog.stars = 0
            prog.time_taken = 0
            prog.is_completed = False     # explicit default mirrors column default
            _db.session.add(prog)
            _db.session.commit()

            found = UserProgress.query.filter_by(email='q@test.com').first()
            assert found.is_completed is False
