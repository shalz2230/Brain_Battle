"""
test_01_splash_login.py
========================
Appium E2E Tests – Splash Screen & Login Flow
Covers: SplashActivity → LoginActivity
"""
import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT = 15   # seconds


class TestSplashScreen:
    """TC-SPL: Splash screen behaviour"""

    def test_tc_spl_001_splash_navigates_to_login(self, driver):
        """TC-SPL-001: After splash animation, LoginActivity opens."""
        wait = WebDriverWait(driver, WAIT)
        login_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
            )
        )
        assert login_btn.is_displayed(), "Login button not visible after splash"

    def test_tc_spl_002_login_screen_elements_visible(self, driver):
        """TC-SPL-002: Login screen shows email, password, login button."""
        email_fld   = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/emailEditText")
        pass_fld    = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/passwordEditText")
        login_btn   = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
        signup_text = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/signupText")
        forgot_text = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/forgotText")
        assert email_fld.is_displayed()
        assert pass_fld.is_displayed()
        assert login_btn.is_displayed()
        assert signup_text.is_displayed()
        assert forgot_text.is_displayed()


class TestLoginFlow:
    """TC-LOG: Login screen interaction tests"""

    def _go_to_login(self, driver):
        """Helper: ensure we are on the login screen."""
        try:
            driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton")
        except Exception:
            driver.execute_script("mobile: startActivity", {
                "intent": "com.simats.brainbattle/.LoginActivity"
            })
            time.sleep(1)

    def test_tc_log_001_empty_login_stays_on_screen(self, driver):
        """TC-LOG-001: Tapping login with empty fields stays on Login screen."""
        self._go_to_login(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/emailEditText").clear()
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/passwordEditText").clear()
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton").click()
        time.sleep(1)
        assert driver.find_element(
            AppiumBy.ID, "com.simats.brainbattle:id/loginButton"
        ).is_displayed(), "Should stay on Login screen"

    def test_tc_log_002_navigate_to_signup(self, driver):
        """TC-LOG-002: Tapping 'Sign up' text opens SignupActivity."""
        self._go_to_login(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/signupText").click()
        wait = WebDriverWait(driver, WAIT)
        signup_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/btnSignup")
            )
        )
        assert signup_btn.is_displayed(), "Signup button not visible"
        driver.back()
        time.sleep(1)

    def test_tc_log_003_navigate_to_forgot_password(self, driver):
        """TC-LOG-003: Tapping 'Forgot?' opens ForgotPasswordActivity."""
        self._go_to_login(driver)
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/forgotText").click()
        wait = WebDriverWait(driver, WAIT)
        reset_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/resetButton")
            )
        )
        assert reset_btn.is_displayed()
        driver.back()
        time.sleep(1)

    def test_tc_log_004_wrong_password_fails(self, driver, registered_user):
        """TC-LOG-004: Wrong password shows Login Failed toast, stays on login."""
        self._go_to_login(driver)
        email_fld = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/emailEditText")
        pass_fld  = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/passwordEditText")
        email_fld.clear(); email_fld.send_keys(registered_user["email"])
        pass_fld.clear();  pass_fld.send_keys("WrongPassword!")
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton").click()
        time.sleep(2)
        assert driver.find_element(
            AppiumBy.ID, "com.simats.brainbattle:id/loginButton"
        ).is_displayed(), "Should stay on Login after wrong password"

    def test_tc_log_005_valid_login_opens_home(self, driver, registered_user):
        """TC-LOG-005: Valid credentials open HomeActivity with welcome greeting."""
        self._go_to_login(driver)
        email_fld = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/emailEditText")
        pass_fld  = driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/passwordEditText")
        email_fld.clear(); email_fld.send_keys(registered_user["email"])
        pass_fld.clear();  pass_fld.send_keys(registered_user["password"])
        driver.find_element(AppiumBy.ID, "com.simats.brainbattle:id/loginButton").click()
        wait = WebDriverWait(driver, WAIT)
        username_tv = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.simats.brainbattle:id/txtUsername")
            )
        )
        assert username_tv.is_displayed(), "Home screen username not visible"
