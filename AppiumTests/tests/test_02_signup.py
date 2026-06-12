"""
test_02_signup.py
==================
Appium E2E Tests – Signup Flow
Covers: SignupActivity
"""
import time
import uuid
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT = 15


class TestSignupFlow:
    """TC-SGN: Signup screen tests"""

    def _go_to_signup(self, driver):
        try:
            driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
        except Exception:
            driver.start_activity("com.simats.brainbattle", "com.simats.brainbattle.LoginActivity")
            time.sleep(1)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/signupText").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/btnSignup")
            )
        )
        time.sleep(0.5)

    def test_tc_sgn_001_signup_screen_fields_visible(self, driver):
        """TC-SGN-001: Signup screen shows username, email, password and signup button."""
        self._go_to_signup(driver)
        assert driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etUsername").is_displayed()
        assert driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etEmail").is_displayed()
        assert driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etPassword").is_displayed()
        assert driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/btnSignup").is_displayed()

    def test_tc_sgn_002_empty_signup_stays_on_screen(self, driver):
        """TC-SGN-002: Empty signup button tap stays on signup screen."""
        self._go_to_signup(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etUsername").clear()
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etEmail").clear()
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etPassword").clear()
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/btnSignup").click()
        time.sleep(1)
        assert driver.find_element(
            AppiumBy.ID, "com.simats.brainbattle:id/btnSignup"
        ).is_displayed(), "Should stay on Signup screen with empty fields"

    def test_tc_sgn_003_login_link_navigates_back(self, driver):
        """TC-SGN-003: Tapping 'Login' link navigates back to LoginActivity."""
        self._go_to_signup(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginText").click()
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
            )
        )
        assert driver.find_element(
            AppiumBy.ID, "com.simats.brainbattle:id/loginButton"
        ).is_displayed()

    def test_tc_sgn_004_valid_signup_succeeds(self, driver):
        """TC-SGN-004: Valid unique signup navigates to LoginActivity."""
        self._go_to_signup(driver)
        unique_email = f"user_{uuid.uuid4().hex[:6]}@brainbattle.com"
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etUsername").send_keys("NewUser")
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etEmail").send_keys(unique_email)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etPassword").send_keys("NewPass123")
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/btnSignup").click()
        wait = WebDriverWait(driver, WAIT)
        login_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
            )
        )
        assert login_btn.is_displayed(), "Should navigate to Login after successful signup"

    def test_tc_sgn_005_duplicate_email_stays_on_signup(self, driver, registered_user):
        """TC-SGN-005: Duplicate email signup stays on signup screen with error."""
        self._go_to_signup(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etUsername").send_keys("DupUser")
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etEmail").send_keys(registered_user["email"])
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/etPassword").send_keys("AnyPass123")
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/btnSignup").click()
        time.sleep(2)
        assert driver.find_element(
            AppiumBy.ID, "com.simats.brainbattle:id/btnSignup"
        ).is_displayed(), "Should stay on Signup screen on duplicate email"
