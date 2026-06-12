// tests/auth.test.js
// ===================
// Selenium-style E2E API Tests – Authentication (Signup & Login)
// Framework: Mocha + Chai + Axios
//
// TC-AUTH-001 … TC-AUTH-012

const { expect } = require('chai');
const api = require('../utils/apiClient');

describe('🔐 Auth API – Signup', function () {

  let uniqueEmail;

  before(() => {
    uniqueEmail = api.randomEmail();
  });

  it('TC-AUTH-001: Valid signup returns 201', async function () {
    const res = await api.signup({ username: 'SeleniumUser', email: uniqueEmail, password: 'Pass1234' });
    expect(res.status).to.equal(201);
    expect(res.data.status).to.equal('success');
  });

  it('TC-AUTH-002: Signup response message confirms registration', async function () {
    const email2 = api.randomEmail();
    const res = await api.signup({ username: 'User2', email: email2, password: 'Pass1234' });
    expect(res.status).to.equal(201);
    expect(res.data.message).to.be.a('string').that.is.not.empty;
  });

  it('TC-AUTH-003: Signup missing username returns 400', async function () {
    const res = await api.signup({ email: api.randomEmail(), password: 'Pass1234' });
    expect(res.status).to.equal(400);
    expect(res.data.status).to.equal('error');
  });

  it('TC-AUTH-004: Signup missing email returns 400', async function () {
    const res = await api.signup({ username: 'Alice', password: 'Pass1234' });
    expect(res.status).to.equal(400);
  });

  it('TC-AUTH-005: Signup missing password returns 400', async function () {
    const res = await api.signup({ username: 'Alice', email: api.randomEmail() });
    expect(res.status).to.equal(400);
  });

  it('TC-AUTH-006: Signup with duplicate email returns 409', async function () {
    const res = await api.signup({ username: 'Dup', email: uniqueEmail, password: 'AnyPass' });
    expect(res.status).to.equal(409);
    expect(res.data.status).to.equal('error');
  });

  it('TC-AUTH-007: Signup with empty body returns 400', async function () {
    const res = await api.signup({});
    expect(res.status).to.equal(400);
  });
});


describe('🔐 Auth API – Login', function () {

  const testEmail    = `login_test_${Date.now()}@bb.com`;
  const testPassword = 'LoginPass99';

  before(async () => {
    await api.signup({ username: 'LoginUser', email: testEmail, password: testPassword });
  });

  it('TC-AUTH-008: Valid login returns 200', async function () {
    const res = await api.login({ email: testEmail, password: testPassword });
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
  });

  it('TC-AUTH-009: Login response contains username and email', async function () {
    const res = await api.login({ email: testEmail, password: testPassword });
    expect(res.data).to.have.property('username').that.is.a('string');
    expect(res.data).to.have.property('email').that.equals(testEmail);
  });

  it('TC-AUTH-010: Login with wrong password returns 401', async function () {
    const res = await api.login({ email: testEmail, password: 'WrongPassword!' });
    expect(res.status).to.equal(401);
    expect(res.data.status).to.equal('error');
  });

  it('TC-AUTH-011: Login with unregistered email returns 404', async function () {
    const res = await api.login({ email: 'nobody@unknown.com', password: 'any' });
    expect(res.status).to.equal(404);
  });

  it('TC-AUTH-012: Login with empty body returns 400', async function () {
    const res = await api.login({});
    expect(res.status).to.equal(400);
  });
});

describe('🔐 Auth API – Edge Cases', function () {
  it('TC-AUTH-013: Signup with extremely long email returns 201', async function () {
    const longEmail = 'a'.repeat(150) + Date.now() + '@bb.com';
    const res = await api.signup({ username: 'LongEmail', email: longEmail, password: 'Pass1234' });
    expect(res.status).to.equal(201);
  });
  it('TC-AUTH-014: Signup with invalid email format (no @) returns 201 (no backend validation)', async function () {
    const res = await api.signup({ username: 'InvalidEmail', email: `not-an-email-${Date.now()}`, password: 'Pass' });
    expect(res.status).to.equal(201);
  });
  it('TC-AUTH-015: Signup with extremely long username returns 201', async function () {
    const longUser = 'u'.repeat(200);
    const res = await api.signup({ username: longUser, email: api.randomEmail(), password: 'Pass' });
    expect(res.status).to.equal(201);
  });
  it('TC-AUTH-016: Signup with SQL injection string in username returns 201', async function () {
    const res = await api.signup({ username: "' OR 1=1 --", email: api.randomEmail(), password: 'Pass' });
    expect(res.status).to.equal(201);
  });
  it('TC-AUTH-017: Login with invalid email format returns 404', async function () {
    const res = await api.login({ email: 'not-an-email', password: 'Any' });
    expect(res.status).to.equal(404);
  });
  it('TC-AUTH-018: Login with SQL injection in email returns 404', async function () {
    const res = await api.login({ email: "' OR 1=1 --", password: 'Any' });
    expect(res.status).to.equal(404);
  });
  it('TC-AUTH-019: Signup with extra fields ignores them and returns 201', async function () {
    const res = await api.signup({ username: 'Extra', email: api.randomEmail(), password: 'Pass', extra: 'field' });
    expect(res.status).to.equal(201);
  });
  it('TC-AUTH-020: Login with extra fields ignores them and logs in', async function () {
    const email = api.randomEmail();
    await api.signup({ username: 'ExLog', email, password: 'Pass' });
    const res = await api.login({ email, password: 'Pass', extra: 'field' });
    expect(res.status).to.equal(200);
  });
  it('TC-AUTH-021: Signup with username as empty string returns 400', async function () {
    const res = await api.signup({ username: '', email: api.randomEmail(), password: 'Pass' });
    expect(res.status).to.equal(400);
  });
  it('TC-AUTH-022: Signup with password as empty string returns 400', async function () {
    const res = await api.signup({ username: 'User', email: api.randomEmail(), password: '' });
    expect(res.status).to.equal(400);
  });
  it('TC-AUTH-023: Login with email as empty string returns 400', async function () {
    const res = await api.login({ email: '', password: 'Pass' });
    expect(res.status).to.equal(400);
  });
  it('TC-AUTH-024: Login with password as empty string returns 400', async function () {
    const res = await api.login({ email: 'email@test.com', password: '' });
    expect(res.status).to.equal(400);
  });
  it('TC-AUTH-025: Signup duplicate email with different case returns 201 (SQLite case-sensitive)', async function () {
    const email = `Case_${Date.now()}@Test.com`;
    await api.signup({ username: 'U1', email, password: 'P1' });
    const res = await api.signup({ username: 'U2', email: email.toLowerCase(), password: 'P2' });
    expect(res.status).to.equal(201);
  });
});
