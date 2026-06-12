package com.simats.brainbattle

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * ============================================================
 *  Brain Battle – Android Instrumented UI / Integration Tests
 * ============================================================
 *  These tests run ON THE EMULATOR via Espresso.
 *
 *  TC-UI-001   Login screen visible on launch
 *  TC-UI-002   Empty login shows validation hint
 *  TC-UI-003   Login → Signup navigation works
 *  TC-UI-004   Signup screen shows required fields
 *  TC-UI-005   Empty signup shows validation hint
 *  TC-UI-006   Signup → Login back-navigation works
 *  TC-UI-007   ForgotPassword screen opens from Login
 * ============================================================
 *
 *  ⚠️  IMPORTANT: Make sure your Flask backend is running and
 *      ApiClient BASE_URL points to your PC IP (not 10.0.2.2
 *      if testing on a real device).
 */
@RunWith(AndroidJUnit4::class)
class LoginInstrumentedTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    // ── TC-UI-001 ──────────────────────────────────────────────
    @Test
    fun tc_ui_001_loginScreenIsDisplayed() {
        onView(withId(R.id.emailEditText)).check(matches(isDisplayed()))
        onView(withId(R.id.passwordEditText)).check(matches(isDisplayed()))
        onView(withId(R.id.loginButton)).check(matches(isDisplayed()))
    }

    // ── TC-UI-002 ──────────────────────────────────────────────
    @Test
    fun tc_ui_002_emptyLogin_showsToastOrStaysOnScreen() {
        // Leave fields empty and tap login – app should stay on login screen
        onView(withId(R.id.loginButton)).perform(click())
        // Login screen is still displayed (did NOT navigate away)
        onView(withId(R.id.loginButton)).check(matches(isDisplayed()))
    }

    // ── TC-UI-003 ──────────────────────────────────────────────
    @Test
    fun tc_ui_003_loginToSignupNavigation() {
        onView(withId(R.id.signupText)).perform(click())
        // After clicking signup text, Signup Activity's username field should appear
        onView(withId(R.id.etUsername)).check(matches(isDisplayed()))
    }

    // ── TC-UI-007 ──────────────────────────────────────────────
    @Test
    fun tc_ui_007_forgotPasswordNavigation() {
        onView(withId(R.id.forgotText)).perform(click())
        // ForgotPasswordActivity should show an email input field
        onView(withId(R.id.etForgotEmail)).check(matches(isDisplayed()))
    }
}


@RunWith(AndroidJUnit4::class)
class SignupInstrumentedTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(SignupActivity::class.java)

    // ── TC-UI-004 ──────────────────────────────────────────────
    @Test
    fun tc_ui_004_signupScreenShowsAllFields() {
        onView(withId(R.id.etUsername)).check(matches(isDisplayed()))
        onView(withId(R.id.etEmail)).check(matches(isDisplayed()))
        onView(withId(R.id.etPassword)).check(matches(isDisplayed()))
        onView(withId(R.id.btnSignup)).check(matches(isDisplayed()))
    }

    // ── TC-UI-005 ──────────────────────────────────────────────
    @Test
    fun tc_ui_005_emptySignup_staysOnScreen() {
        onView(withId(R.id.btnSignup)).perform(click())
        // Signup Activity should remain open (validation prevents navigation)
        onView(withId(R.id.btnSignup)).check(matches(isDisplayed()))
    }

    // ── TC-UI-006 ──────────────────────────────────────────────
    @Test
    fun tc_ui_006_signupToLoginNavigation() {
        onView(withId(R.id.loginText)).perform(click())
        // LoginActivity's login button should appear
        onView(withId(R.id.loginButton)).check(matches(isDisplayed()))
    }
}
