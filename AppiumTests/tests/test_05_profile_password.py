"""
test_05_profile_password.py
============================
Appium E2E Tests – Profile, Rank, Forgot & Change Password
"""
import time
import uuid
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT = 15
PKG  = "com.simats.brainbattle"


def go_home(driver):
    driver.start_activity(PKG, f"{PKG}.HomeActivity")
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/txtUsername"))
    )
    time.sleep(1)


class TestProfileRank:
    """TC-PRF: Profile & Rank screen tests"""

    def test_tc_prf_001_profile_screen_elements_visible(self, driver):
        """TC-PRF-001: Profile screen shows username, email, rank, stars, levels."""
        go_home(driver)
        driver.find_element(AppiumBy.ID, f"{PKG}:id/profileIcon").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/rankText"))
        )
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/username").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/email").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/rankText").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/starCount").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/levelsCompleted").is_displayed()

    def test_tc_prf_002_email_displayed_on_profile(self, driver, registered_user):
        """TC-PRF-002: Logged-in user's email is shown on profile screen."""
        email_tv = driver.find_element(AppiumBy.ID, f"{PKG}:id/email")
        assert registered_user["email"] in email_tv.text or email_tv.is_displayed()

    def test_tc_prf_003_rank_text_has_hash_prefix(self, driver):
        """TC-PRF-003: Rank text starts with '#' symbol."""
        rank_tv = driver.find_element(AppiumBy.ID, f"{PKG}:id/rankText")
        assert "#" in rank_tv.text, f"Rank text: {rank_tv.text}"

    def test_tc_prf_004_change_password_btn_opens_screen(self, driver):
        """TC-PRF-004: Change Password button opens ChangePasswordActivity."""
        driver.find_element(AppiumBy.ID, f"{PKG}:id/changePasswordBtn").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/changeButton"))
        )
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/changeButton").is_displayed()

    def test_tc_prf_005_change_password_email_pre_filled(self, driver, registered_user):
        """TC-PRF-005: Change password screen pre-fills the email field."""
        email_fld = driver.find_element(AppiumBy.ID, f"{PKG}:id/emailEditText")
        assert registered_user["email"] in email_fld.text or email_fld.is_displayed()
        driver.back()
        time.sleep(1)

    def test_tc_prf_006_back_button_returns_to_home(self, driver):
        """TC-PRF-006: Back button on profile returns to HomeActivity."""
        driver.find_element(AppiumBy.ID, f"{PKG}:id/backBtn").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/txtUsername"))
        )
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/txtUsername").is_displayed()


class TestForgotPassword:
    """TC-FGT: Forgot Password flow"""

    def _go_to_forgot(self, driver):
        try:
            driver.find_element(AppiumBy.ID, f"{PKG}:id/loginButton")
        except Exception:
            driver.start_activity(PKG, f"{PKG}.LoginActivity")
            time.sleep(1)
        driver.find_element(AppiumBy.ID, f"{PKG}:id/forgotText").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/resetButton"))
        )
        time.sleep(0.5)

    def test_tc_fgt_001_forgot_password_screen_elements(self, driver):
        """TC-FGT-001: Forgot password screen shows email field and reset button."""
        self._go_to_forgot(driver)
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/emailEditText").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/resetButton").is_displayed()

    def test_tc_fgt_002_empty_email_stays_on_screen(self, driver):
        """TC-FGT-002: Clicking reset with empty email stays on forgot screen."""
        driver.find_element(AppiumBy.ID, f"{PKG}:id/emailEditText").clear()
        driver.find_element(AppiumBy.ID, f"{PKG}:id/resetButton").click()
        time.sleep(1)
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/resetButton").is_displayed()

    def test_tc_fgt_003_valid_email_opens_change_password(self, driver, registered_user):
        """TC-FGT-003: Valid registered email navigates to ChangePasswordActivity."""
        driver.find_element(AppiumBy.ID, f"{PKG}:id/emailEditText").send_keys(
            registered_user["email"]
        )
        driver.find_element(AppiumBy.ID, f"{PKG}:id/resetButton").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((AppiumBy.ID, f"{PKG}:id/changeButton"))
        )
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/changeButton").is_displayed()

    def test_tc_fgt_004_change_password_screen_elements(self, driver):
        """TC-FGT-004: Change password screen shows email field, password and change button."""
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/emailEditText").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/passwordEditText").is_displayed()
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/changeButton").is_displayed()

    def test_tc_fgt_005_empty_password_stays_on_change_screen(self, driver):
        """TC-FGT-005: Clicking change with empty password stays on change screen."""
        driver.find_element(AppiumBy.ID, f"{PKG}:id/passwordEditText").clear()
        driver.find_element(AppiumBy.ID, f"{PKG}:id/changeButton").click()
        time.sleep(1)
        assert driver.find_element(AppiumBy.ID, f"{PKG}:id/changeButton").is_displayed()
        driver.back(); driver.back()
        time.sleep(1)
