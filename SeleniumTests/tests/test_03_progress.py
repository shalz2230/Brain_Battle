"""
SeleniumTests/tests/test_03_progress.py
=========================================
Selenium-style E2E Web API Tests – Game Progress
TC-PRG-001 … TC-PRG-014
"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.api_client import ApiClient, random_email


class TestSaveProgress:
    """TC-PRG-001..006: Save progress endpoint"""

    @pytest.fixture(scope="class")
    def user_email(self):
        email = random_email()
        ApiClient.signup("ProgressUser", email, "Prog123")
        return email

    def test_tc_prg_001_save_memory_returns_success(self, user_email):
        """TC-PRG-001: Save memory game progress returns status=success."""
        res = ApiClient.save_progress(user_email, "memory", 1, 3, 30)
        assert res.status_code == 200
        assert res.json().get("status") == "success"

    def test_tc_prg_002_save_logic_returns_success(self, user_email):
        """TC-PRG-002: Save logic game progress returns status=success."""
        res = ApiClient.save_progress(user_email, "logic", 1, 3, 15)
        assert res.status_code == 200

    def test_tc_prg_003_save_focus_returns_success(self, user_email):
        """TC-PRG-003: Save focus game progress returns status=success."""
        res = ApiClient.save_progress(user_email, "focus", 1, 3, 10)
        assert res.status_code == 200

    def test_tc_prg_004_save_speed_returns_success(self, user_email):
        """TC-PRG-004: Save speed game progress returns status=success."""
        res = ApiClient.save_progress(user_email, "speed", 1, 2, 8)
        assert res.status_code == 200

    def test_tc_prg_005_upsert_same_level_not_duplicated(self, user_email):
        """TC-PRG-005: Saving same level twice updates record, not duplicates it."""
        ApiClient.save_progress(user_email, "memory", 5, 1, 60)
        ApiClient.save_progress(user_email, "memory", 5, 3, 20)
        res = ApiClient.get_progress(user_email, "memory")
        level5 = [p for p in res.json() if p["level"] == 5]
        assert len(level5) == 1
        assert level5[0]["stars"] == 3

    def test_tc_prg_006_is_completed_set_true(self, user_email):
        """TC-PRG-006: Saved progress record has is_completed = True."""
        res = ApiClient.get_progress(user_email, "memory")
        lvl1 = next((p for p in res.json() if p["level"] == 1), None)
        assert lvl1 is not None
        assert lvl1.get("completed") is True


class TestGetProgress:
    """TC-PRG-007..014: Get progress endpoint"""

    @pytest.fixture(scope="class")
    def user_email(self):
        email = random_email()
        ApiClient.signup("GetProgUser", email, "GetProg1")
        ApiClient.save_progress(email, "memory", 1, 3, 25)
        ApiClient.save_progress(email, "memory", 2, 2, 40)
        ApiClient.save_progress(email, "logic",  1, 3, 12)
        return email

    def test_tc_prg_007_get_memory_returns_correct_count(self, user_email):
        """TC-PRG-007: Get memory progress returns list with 2 entries."""
        res = ApiClient.get_progress(user_email, "memory")
        assert res.status_code == 200
        assert len(res.json()) == 2

    def test_tc_prg_008_items_have_level_stars_completed_fields(self, user_email):
        """TC-PRG-008: Each item contains level, stars, completed fields."""
        res = ApiClient.get_progress(user_email, "memory")
        for item in res.json():
            assert "level"     in item
            assert "stars"     in item
            assert "completed" in item
            assert isinstance(item["level"], int)
            assert isinstance(item["stars"], int)
            assert isinstance(item["completed"], bool)

    def test_tc_prg_009_unplayed_game_returns_empty_list(self, user_email):
        """TC-PRG-009: Get progress for unplayed game returns empty list []."""
        res = ApiClient.get_progress(user_email, "speed")
        assert res.status_code == 200
        assert res.json() == []

    def test_tc_prg_010_logic_progress_returns_correct_entry(self, user_email):
        """TC-PRG-010: Get logic progress returns single entry with correct data."""
        res = ApiClient.get_progress(user_email, "logic")
        assert len(res.json()) == 1
        assert res.json()[0]["level"] == 1
        assert res.json()[0]["stars"] == 3

    def test_tc_prg_011_stars_within_valid_range(self, user_email):
        """TC-PRG-011: Stars value is within 1–3 range for all entries."""
        res = ApiClient.get_progress(user_email, "memory")
        for item in res.json():
            assert 1 <= item["stars"] <= 3

    def test_tc_prg_012_level_numbers_correct(self, user_email):
        """TC-PRG-012: Level numbers stored correctly in the response."""
        res = ApiClient.get_progress(user_email, "memory")
        levels = sorted([p["level"] for p in res.json()])
        assert levels == [1, 2]

    def test_tc_prg_013_unknown_email_returns_empty_list(self):
        """TC-PRG-013: Progress for unknown email returns empty list."""
        res = ApiClient.get_progress("noone@bb.com", "memory")
        assert res.status_code == 200
        assert res.json() == []

    def test_tc_prg_014_multiple_game_types_tracked_independently(self, user_email):
        """TC-PRG-014: Memory and Logic game types are tracked independently."""
        mem_res = ApiClient.get_progress(user_email, "memory")
        lgc_res = ApiClient.get_progress(user_email, "logic")
        assert len(mem_res.json()) == 2
        assert len(lgc_res.json()) == 1
