"""
=============================================================
  Brain Battle – Backend Functional Tests: PROGRESS & DASHBOARD
=============================================================
  Coverage:
    ✅ TC-PRG-001  Save new progress record           → 200
    ✅ TC-PRG-002  Update existing progress (upsert)  → 200
    ✅ TC-PRG-003  Get progress returns correct data  → 200
    ✅ TC-PRG-004  Get progress empty (no records)    → [] (200)
    ✅ TC-DSH-001  Dashboard with no progress         → defaults
    ✅ TC-DSH-002  Dashboard with progress            → correct stats
    ✅ TC-DSH-003  Rank calculation single user       → rank = 1
    ✅ TC-DSH-004  Rank calculation multi user        → ranked correctly
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'BrainBattleBackend'))

from app import create_app
from database.db import db as _db
from models.progress_model import UserProgress
from models.user_model import User
from utils.hash_utils import hash_password


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


EMAIL = 'player@example.com'


def save_progress(client, email=EMAIL, game_type='memory',
                  level=1, stars=3, time_taken=45):
    return client.post('/api/progress/save',
                       json={'email': email, 'game_type': game_type,
                             'level': level, 'stars': stars,
                             'time_taken': time_taken})


# ═══════════════════════ PROGRESS TESTS ══════════════════════════

class TestProgress:

    def test_tc_prg_001_save_new_progress(self, client):
        """TC-PRG-001: Saving a new progress entry returns success."""
        res = save_progress(client)
        assert res.status_code == 200
        assert res.get_json()['status'] == 'success'

    def test_tc_prg_002_upsert_progress(self, client, app):
        """TC-PRG-002: Saving same level twice updates the record (not duplicate)."""
        save_progress(client, stars=1)
        save_progress(client, stars=3)   # update same level

        with app.app_context():
            records = UserProgress.query.filter_by(
                email=EMAIL, game_type='memory', level=1
            ).all()
        # Must be exactly ONE record (upsert behaviour)
        assert len(records) == 1
        assert records[0].stars == 3

    def test_tc_prg_003_get_progress_returns_data(self, client):
        """TC-PRG-003: Get progress returns saved levels."""
        save_progress(client, level=1, stars=2)
        save_progress(client, level=2, stars=3)

        res = client.get(f'/api/progress/get/{EMAIL}/memory')
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, list)
        assert len(data) == 2

        levels = {item['level'] for item in data}
        assert levels == {1, 2}

    def test_tc_prg_004_get_progress_empty(self, client):
        """TC-PRG-004: No saved progress returns empty list."""
        res = client.get(f'/api/progress/get/{EMAIL}/logic')
        assert res.status_code == 200
        assert res.get_json() == []

    def test_tc_prg_completed_flag(self, client):
        """Saved progress records have is_completed = True."""
        save_progress(client, level=5, stars=3)
        res = client.get(f'/api/progress/get/{EMAIL}/memory')
        item = next(x for x in res.get_json() if x['level'] == 5)
        assert item['completed'] is True


# ═══════════════════════ DASHBOARD TESTS ═════════════════════════

class TestDashboard:

    def test_tc_dsh_001_dashboard_no_progress(self, client):
        """TC-DSH-001: Fresh user gets default dashboard values."""
        res = client.get(f'/api/dashboard/{EMAIL}')
        assert res.status_code == 200
        data = res.get_json()
        assert data['total_stars'] == 0
        assert data['current_level'] == 1
        assert data['levels_completed'] == 0

    def test_tc_dsh_002_dashboard_with_progress(self, client):
        """TC-DSH-002: Dashboard stats match saved progress."""
        save_progress(client, level=1, stars=3, game_type='memory')
        save_progress(client, level=2, stars=2, game_type='memory')
        save_progress(client, level=1, stars=1, game_type='logic')

        res = client.get(f'/api/dashboard/{EMAIL}')
        assert res.status_code == 200
        data = res.get_json()
        assert data['total_stars'] == 6        # 3 + 2 + 1
        assert data['levels_completed'] == 3

    def test_tc_dsh_003_rank_single_user(self, client):
        """TC-DSH-003: Single user with any stars is ranked #1."""
        save_progress(client, stars=5)
        res = client.get(f'/api/dashboard/{EMAIL}')
        assert res.get_json()['rank'] == 1

    def test_tc_dsh_004_rank_multiple_users(self, client, app):
        """TC-DSH-004: User with more stars gets a lower rank number."""
        EMAIL_2 = 'topplayer@example.com'

        # player 1 – 3 stars total
        save_progress(client, email=EMAIL, stars=3)
        # player 2 – 10 stars total (higher → rank 1)
        save_progress(client, email=EMAIL_2, game_type='logic',
                      level=1, stars=10)

        res1 = client.get(f'/api/dashboard/{EMAIL}')
        res2 = client.get(f'/api/dashboard/{EMAIL_2}')

        rank1 = res1.get_json()['rank']
        rank2 = res2.get_json()['rank']

        assert rank2 < rank1          # top player ranked higher (smaller number)
        assert rank2 == 1
        assert rank1 == 2
