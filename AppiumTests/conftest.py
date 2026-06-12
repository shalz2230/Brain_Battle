"""
conftest.py  ─  Appium shared driver fixture for Brain Battle E2E tests
"""
import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options


# ─────────────────────────────────────────────────────────────────
#  DESIRED CAPABILITIES
#  ➜  Make sure:
#     1. Appium Server is running  →  appium  (default port 4723)
#     2. Android Emulator is running (AVD)
#     3. BrainBattle APK is already installed on the emulator
# ─────────────────────────────────────────────────────────────────
APPIUM_SERVER  = "http://127.0.0.1:4723"
APP_PACKAGE    = "com.simats.brainbattle"
APP_ACTIVITY   = "com.simats.brainbattle.SplashActivity"
DEVICE_NAME    = "moto g32"                          # Motorola Moto G32
DEVICE_UDID    = "adb-ZD222H9SLV-Gl6lse._adb-tls-connect._tcp"  # real device ADB ID
PLATFORM_VER  = "13"                                # Android 13

# ADB executable path (full path since adb may not be in system PATH)
ADB_PATH       = r"C:\Users\adminuser\AppData\Local\Android\Sdk\platform-tools\adb.exe"

# Test user credentials  (must already be registered in the backend)
TEST_EMAIL     = "appiumtest@brainbattle.com"
TEST_PASSWORD  = "TestPass123"
TEST_USERNAME  = "AppiumUser"

# Backend URL (Flask)
# For a real USB device use your PC's local network IP
BACKEND_URL    = "http://127.0.0.1:5000"  # Flask backend on this PC


def get_options() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name          = "Android"
    options.platform_version       = PLATFORM_VER
    options.device_name            = DEVICE_NAME
    options.udid                   = DEVICE_UDID
    options.app_package            = APP_PACKAGE
    options.app_activity           = APP_ACTIVITY
    options.automation_name        = "UiAutomator2"
    options.no_reset               = True        # keep app data between tests
    options.full_reset             = False
    options.new_command_timeout    = 120
    options.auto_grant_permissions = True
    options.skip_server_installation = False
    options.adb_exec_timeout       = 60000       # ms
    return options


@pytest.fixture(scope="session")
def driver():
    """Create ONE Appium driver for the entire test session."""
    drv = webdriver.Remote(APPIUM_SERVER, options=get_options())
    drv.implicitly_wait(10)
    time.sleep(3)          # wait for splash animation
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def registered_user(driver):
    """
    Ensure test account exists. Registers via the app signup flow once,
    then yields the credentials dict for all tests.
    """
    import requests
    resp = requests.post(
        f"{BACKEND_URL}/api/auth/signup",
        json={"username": TEST_USERNAME,
              "email": TEST_EMAIL,
              "password": TEST_PASSWORD},
        timeout=10
    )
    # 201 = created, 409 = already exists — both are fine
    assert resp.status_code in (201, 409), f"Signup pre-check failed: {resp.text}"
    return {"email": TEST_EMAIL, "password": TEST_PASSWORD, "username": TEST_USERNAME}
