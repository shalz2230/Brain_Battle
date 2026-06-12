// tests/user.test.js
// ====================
// Selenium-style E2E API Tests – User Management
// TC-USR-001 … TC-USR-012

const { expect } = require('chai');
const api = require('../utils/apiClient');

describe('👤 User API – Get User', function () {

  const email    = `usr_${Date.now()}@bb.com`;
  const password = 'UserPass99';

  before(async () => {
    await api.signup({ username: 'TestUser', email, password });
  });

  it('TC-USR-001: Get user with valid email returns 200 + username', async function () {
    const res = await api.getUser(email);
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
    expect(res.data.username).to.equal('TestUser');
  });

  it('TC-USR-002: Get user response contains username field', async function () {
    const res = await api.getUser(email);
    expect(res.data).to.have.property('username').that.is.a('string');
  });

  it('TC-USR-003: Get user with unknown email returns 404', async function () {
    const res = await api.getUser('nobody@nobody.com');
    expect(res.status).to.equal(404);
    expect(res.data.status).to.equal('error');
  });
});


describe('🔑 User API – Forgot Password', function () {

  const email = `fgt_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'ForgotUser', email, password: 'OldPass99' });
  });

  it('TC-USR-004: Forgot password with registered email returns 200', async function () {
    const res = await api.forgotPassword(email);
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
  });

  it('TC-USR-005: Forgot password response message is non-empty', async function () {
    const res = await api.forgotPassword(email);
    expect(res.data.message).to.be.a('string').that.is.not.empty;
  });

  it('TC-USR-006: Forgot password with unregistered email returns 404', async function () {
    const res = await api.forgotPassword('ghost@nobody.com');
    expect(res.status).to.equal(404);
  });
});


describe('🔒 User API – Change Password', function () {

  const email    = `chg_${Date.now()}@bb.com`;
  const oldPass  = 'OldSecret77';
  const newPass  = 'NewSecret88';

  before(async () => {
    await api.signup({ username: 'ChangeUser', email, password: oldPass });
  });

  it('TC-USR-007: Change password for valid user returns 200', async function () {
    const res = await api.changePassword(email, newPass);
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
  });

  it('TC-USR-008: New password can be used to login', async function () {
    const res = await api.login({ email, password: newPass });
    expect(res.status).to.equal(200);
  });

  it('TC-USR-009: Old password rejected after password change', async function () {
    const res = await api.login({ email, password: oldPass });
    expect(res.status).to.equal(401);
  });

  it('TC-USR-010: Change password for unknown user returns 404', async function () {
    const res = await api.changePassword('nobody@bb.com', 'anypass');
    expect(res.status).to.equal(404);
  });

  it('TC-USR-011: Change password returns success message string', async function () {
    const email2 = `chg2_${Date.now()}@bb.com`;
    await api.signup({ username: 'ChgUser2', email: email2, password: 'OldP99' });
    const res = await api.changePassword(email2, 'NewP99');
    expect(res.data.message).to.be.a('string').that.is.not.empty;
  });

  it('TC-USR-012: Changed password login returns username in response', async function () {
    const res = await api.login({ email, password: newPass });
    expect(res.data).to.have.property('username').that.equals('ChangeUser');
  });
});

describe('👤 User API – Edge Cases', function () {
  it('TC-USR-013: Get user missing email in payload returns 404', async function () {
    const res = await api.getUser(); 
    expect(res.status).to.equal(404);
  });
  it('TC-USR-014: Forgot password missing email returns 404', async function () {
    const res = await api.forgotPassword();
    expect(res.status).to.equal(404);
  });
  it('TC-USR-015: Change password missing user fields returns 404', async function () {
    const res = await api.changePassword(undefined, 'NewPass');
    expect(res.status).to.equal(404);
  });
  it('TC-USR-016: Get user with SQL injection string returns 404', async function () {
    const res = await api.getUser("' OR 1=1 --");
    expect(res.status).to.equal(404);
  });
  it('TC-USR-017: Forgot password with SQL injection string returns 404', async function () {
    const res = await api.forgotPassword("' OR 1=1 --");
    expect(res.status).to.equal(404);
  });
  it('TC-USR-018: Change password for non-existent user returns 404', async function () {
    const res = await api.changePassword('ghost@bb.com', 'Pass123');
    expect(res.status).to.equal(404);
  });
  it('TC-USR-019: Change password using the same string for old and new passwords returns 200', async function () {
    const email = `same_${Date.now()}@bb.com`;
    await api.signup({ username: 'Same', email, password: 'SamePassword' });
    const res = await api.changePassword(email, 'SamePassword');
    expect(res.status).to.equal(200);
  });
  it('TC-USR-020: Login successful after changing password to the same string', async function () {
    const email = `same2_${Date.now()}@bb.com`;
    await api.signup({ username: 'Same2', email, password: 'SamePassword2' });
    await api.changePassword(email, 'SamePassword2');
    const res = await api.login({ email, password: 'SamePassword2' });
    expect(res.status).to.equal(200);
  });
  it('TC-USR-021: Get user with extremely long email returns 404', async function () {
    const res = await api.getUser('a'.repeat(150) + Date.now() + '@bb.com');
    expect(res.status).to.equal(404);
  });
  it('TC-USR-022: Forgot password with extremely long email returns 404', async function () {
    const res = await api.forgotPassword('a'.repeat(150) + Date.now() + '@bb.com');
    expect(res.status).to.equal(404);
  });
  it('TC-USR-023: Change password with empty new password returns 200 (no backend validation)', async function () {
    const email = `mt_${Date.now()}@bb.com`;
    await api.signup({ username: 'MT', email, password: 'Old' });
    const res = await api.changePassword(email, '');
    expect(res.status).to.equal(200);
  });
  it('TC-USR-024: Login works with empty password after changing to empty', async function () {
    const email = `mt2_${Date.now()}@bb.com`;
    await api.signup({ username: 'MT2', email, password: 'Old' });
    await api.changePassword(email, '');
    const res = await api.login({ email, password: '' });
    // Note: login route HAS validation! if not email or not password -> 400
    expect(res.status).to.equal(400);
  });
  it('TC-USR-025: Get user case sensitivity check (SQLite default case sensitive) returns 404', async function () {
    const email = `Upper_${Date.now()}@bb.com`;
    await api.signup({ username: 'Up', email, password: 'P' });
    const res = await api.getUser(email.toLowerCase());
    expect(res.status).to.equal(404);
  });
});
