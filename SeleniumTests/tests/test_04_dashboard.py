"""
SeleniumTests/tests/test_04_dashboard.py
==========================================
Selenium-style E2E Web API Tests – Dashboard & Ranking
TC-DSH-001 … TC-DSH-012
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.api_client import ApiClient, random_email


class TestDashboardFreshUser:
    """TC-DSH-001..004: Dashboard for brand-new user"""

    @pytest.fixture(scope="class")
    def fresh_email(self):
        email = random_email()
        ApiClient.signup("DashFresh", email, "DashP1")
        return email

    def test_tc_dsh_001_fresh_user_total_stars_is_0(self, fresh_email):
        """TC-DSH-001: Fresh user total_stars = 0."""
        res = ApiClient.get_dashboard(fresh_email)
        assert res.status_code == 200
        assert res.json().get("total_stars") == 0

    def test_tc_dsh_002_fresh_user_current_level_is_1(self, fresh_email):
        """TC-DSH-002: Fresh user current_level = 1."""
        assert ApiClient.get_dashboard(fresh_email).json().get("current_level") == 1

    def test_tc_dsh_003_fresh_user_levels_completed_is_0(self, fresh_email):
        """TC-DSH-003: Fresh user levels_completed = 0."""
        assert ApiClient.get_dashboard(fresh_email).json().get("levels_completed") == 0

    def test_tc_dsh_004_response_has_all_required_fields(self, fresh_email):
        """TC-DSH-004: Dashboard response has current_level, total_stars, last_game, rank, levels_completed."""
        data = ApiClient.get_dashboard(fresh_email).json()
        for field in ("current_level", "total_stars", "last_game", "rank", "levels_completed"):
            assert field in data, f"Missing field: {field}"


class TestDashboardWithProgress:
    """TC-DSH-005..008: Dashboard after saving game progress"""

    @pytest.fixture(scope="class")
    def user_email(self):
        email = random_email()
        ApiClient.signup("DashProg", email, "DashP2")
        ApiClient.save_progress(email, "memory", 1, 3, 30)
        ApiClient.save_progress(email, "memory", 2, 2, 45)
        ApiClient.save_progress(email, "logic",  1, 1, 20)
        return email

    def test_tc_dsh_005_total_stars_equals_sum(self, user_email):
        """TC-DSH-005: total_stars = 3+2+1 = 6."""
        res = ApiClient.get_dashboard(user_email)
        assert res.json().get("total_stars") == 6

    def test_tc_dsh_006_levels_completed_matches_records(self, user_email):
        """TC-DSH-006: levels_completed = 3 (number of saved records)."""
        assert ApiClient.get_dashboard(user_email).json().get("levels_completed") == 3

    def test_tc_dsh_007_last_game_reflects_most_recent(self, user_email):
        """TC-DSH-007: last_game reflects the most recently saved game type."""
        assert ApiClient.get_dashboard(user_email).json().get("last_game") == "logic"

    def test_tc_dsh_008_current_level_is_positive(self, user_email):
        """TC-DSH-008: current_level is a positive integer."""
        lvl = ApiClient.get_dashboard(user_email).json().get("current_level")
        assert isinstance(lvl, int) and lvl > 0


class TestDashboardRanking:
    """TC-DSH-009..012: Ranking tests"""

    @pytest.fixture(scope="class")
    def two_users(self):
        e1 = random_email(); e2 = random_email()
        ApiClient.signup("RankUser1", e1, "Rank1P")
        ApiClient.signup("RankUser2", e2, "Rank2P")
        ApiClient.save_progress(e1, "memory", 1,  3, 30)   # 3 stars
        ApiClient.save_progress(e2, "memory", 1, 15, 10)   # 15 stars → should rank #1
        return {"low_star_email": e1, "high_star_email": e2}

    def test_tc_dsh_009_single_user_rank_is_positive(self):
        """TC-DSH-009: A user with progress gets a positive rank number."""
        email = random_email()
        ApiClient.signup("OnlyUser", email, "Only1")
        ApiClient.save_progress(email, "focus", 1, 5, 15)
        rank = ApiClient.get_dashboard(email).json().get("rank")
        assert isinstance(rank, int) and rank >= 1

    def test_tc_dsh_010_top_scorer_has_lower_rank_number(self, two_users):
        """TC-DSH-010: User with more stars has lower (better) rank number."""
        r_low  = ApiClient.get_dashboard(two_users["low_star_email"]).json()
        r_high = ApiClient.get_dashboard(two_users["high_star_email"]).json()
        assert r_high["rank"] < r_low["rank"]

    def test_tc_dsh_011_top_scorer_rank_equals_1(self, two_users):
        """TC-DSH-011: Top scorer rank = 1."""
        rank = ApiClient.get_dashboard(two_users["high_star_email"]).json().get("rank")
        assert rank == 1

    def test_tc_dsh_012_rank_is_positive_integer(self, two_users):
        """TC-DSH-012: Rank is always a positive integer."""
        rank = ApiClient.get_dashboard(two_users["low_star_email"]).json().get("rank")
        assert isinstance(rank, int) and rank >= 1
