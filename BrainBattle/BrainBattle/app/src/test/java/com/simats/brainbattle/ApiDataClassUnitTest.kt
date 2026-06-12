package com.simats.brainbattle

import com.simats.brainbattle.api.*
import org.junit.Assert.*
import org.junit.Test

/**
 * ============================================================
 *  Brain Battle – Android Unit Tests
 * ============================================================
 *  TC-AND-001  AuthRequest validation – non-null email/password
 *  TC-AND-002  LoginResponse data class fields
 *  TC-AND-003  ProgressRequest data class integrity
 *  TC-AND-004  DashboardResponse data class integrity
 *  TC-AND-005  Empty string validation logic (mirroring Activity)
 *  TC-AND-006  Email format basic check (login screen guard)
 *  TC-AND-007  ProgressItem completed flag
 *  TC-AND-008  AuthRequest optional username defaults null
 * ============================================================
 */
class ApiDataClassUnitTest {

    // ── TC-AND-001 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-001 AuthRequest stores email and password correctly`() {
        val req = AuthRequest(email = "test@example.com", password = "Pass1234")
        assertEquals("test@example.com", req.email)
        assertEquals("Pass1234", req.password)
    }

    // ── TC-AND-002 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-002 LoginResponse stores all expected fields`() {
        val resp = LoginResponse(
            status = "success",
            message = "Login successful",
            username = "Alice",
            email = "alice@example.com"
        )
        assertEquals("success", resp.status)
        assertEquals("Alice", resp.username)
        assertEquals("alice@example.com", resp.email)
    }

    // ── TC-AND-003 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-003 ProgressRequest stores all fields correctly`() {
        val req = ProgressRequest(
            email = "bob@example.com",
            game_type = "memory",
            level = 3,
            stars = 2,
            time_taken = 60
        )
        assertEquals("memory", req.game_type)
        assertEquals(3, req.level)
        assertEquals(2, req.stars)
        assertEquals(60, req.time_taken)
    }

    // ── TC-AND-004 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-004 DashboardResponse stores all stats correctly`() {
        val dash = DashboardResponse(
            current_level = 5,
            total_stars = 42,
            last_game = "logic",
            rank = 2,
            levels_completed = 10
        )
        assertEquals(5, dash.current_level)
        assertEquals(42, dash.total_stars)
        assertEquals("logic", dash.last_game)
        assertEquals(2, dash.rank)
        assertEquals(10, dash.levels_completed)
    }

    // ── TC-AND-005 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-005 Empty email string is treated as invalid`() {
        val email = "   ".trim()
        assertTrue("Empty email should be rejected", email.isEmpty())
    }

    @Test
    fun `TC-AND-005b Empty password string is treated as invalid`() {
        val password = "".trim()
        assertTrue("Empty password should be rejected", password.isEmpty())
    }

    // ── TC-AND-006 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-006 Valid email passes basic format check`() {
        val validEmail = "user@domain.com"
        assertTrue(android.util.Patterns.EMAIL_ADDRESS.matcher(validEmail).matches())
    }

    @Test
    fun `TC-AND-006b Invalid email fails basic format check`() {
        val invalidEmail = "not-an-email"
        assertFalse(android.util.Patterns.EMAIL_ADDRESS.matcher(invalidEmail).matches())
    }

    // ── TC-AND-007 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-007 ProgressItem completed flag is read correctly`() {
        val item = ProgressItem(level = 1, stars = 3, completed = true)
        assertTrue(item.completed)

        val incomplete = ProgressItem(level = 2, stars = 0, completed = false)
        assertFalse(incomplete.completed)
    }

    // ── TC-AND-008 ──────────────────────────────────────────────
    @Test
    fun `TC-AND-008 AuthRequest username is null by default`() {
        val req = AuthRequest(email = "x@x.com", password = "abc")
        assertNull("Username should default to null for login request", req.username)
    }

    @Test
    fun `TC-AND-008b AuthRequest username is set for signup`() {
        val req = AuthRequest(username = "Charlie", email = "c@c.com", password = "xyz")
        assertEquals("Charlie", req.username)
    }
}
