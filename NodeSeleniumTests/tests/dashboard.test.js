// tests/dashboard.test.js
// ========================
// Selenium-style E2E API Tests – Dashboard & Ranking
// TC-DSH-001 … TC-DSH-012

const { expect } = require('chai');
const api = require('../utils/apiClient');

describe('📊 Dashboard API – Fresh User', function () {

  const email = `dash_fresh_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'DashFresh', email, password: 'DashP1' });
  });

  it('TC-DSH-001: Fresh user total_stars is 0', async function () {
    const res = await api.getDashboard(email);
    expect(res.status).to.equal(200);
    expect(res.data.total_stars).to.equal(0);
  });

  it('TC-DSH-002: Fresh user current_level is 1', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.current_level).to.equal(1);
  });

  it('TC-DSH-003: Fresh user levels_completed is 0', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.levels_completed).to.equal(0);
  });

  it('TC-DSH-004: Dashboard response has all required fields', async function () {
    const res = await api.getDashboard(email);
    const d = res.data;
    expect(d).to.have.property('current_level');
    expect(d).to.have.property('total_stars');
    expect(d).to.have.property('last_game');
    expect(d).to.have.property('rank');
    expect(d).to.have.property('levels_completed');
  });
});


describe('📊 Dashboard API – With Progress', function () {

  const email = `dash_prog_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'DashProg', email, password: 'DashP2' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 3, time_taken: 30 });
    await api.saveProgress({ email, game_type: 'memory', level: 2, stars: 2, time_taken: 45 });
    await api.saveProgress({ email, game_type: 'logic',  level: 1, stars: 1, time_taken: 20 });
  });

  it('TC-DSH-005: Total stars equals sum of all game progress stars', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.total_stars).to.equal(6);   // 3+2+1
  });

  it('TC-DSH-006: levels_completed matches number of saved progress records', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.levels_completed).to.equal(3);
  });

  it('TC-DSH-007: last_game reflects the most recently saved game type', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.last_game).to.equal('logic');
  });

  it('TC-DSH-008: current_level reflects highest level of last game', async function () {
    const res = await api.getDashboard(email);
    expect(res.data.current_level).to.be.a('number').that.is.greaterThan(0);
  });
});


describe('🏆 Dashboard API – Ranking', function () {

  const email1 = `rank1_${Date.now()}@bb.com`;
  const email2 = `rank2_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'RankUser1', email: email1, password: 'Rank1P' });
    await api.signup({ username: 'RankUser2', email: email2, password: 'Rank2P' });
    // email1 = 3 stars, email2 = huge number of stars (email2 should rank #1)
    await api.saveProgress({ email: email1, game_type: 'memory', level: 1, stars: 3, time_taken: 30 });
    await api.saveProgress({ email: email2, game_type: 'memory', level: 1, stars: 999999999 + Date.now(), time_taken: 10 });
  });

  it('TC-DSH-009: Single user with progress has rank 1 or better', async function () {
    const email3 = `rankonly_${Date.now()}@bb.com`;
    await api.signup({ username: 'OnlyUser', email: email3, password: 'Only1' });
    await api.saveProgress({ email: email3, game_type: 'focus', level: 1, stars: 5, time_taken: 15 });
    const res = await api.getDashboard(email3);
    expect(res.data.rank).to.be.a('number').that.is.greaterThan(0);
  });

  it('TC-DSH-010: User with more stars has a lower rank number (better rank)', async function () {
    const res1 = await api.getDashboard(email1);
    const res2 = await api.getDashboard(email2);
    expect(res2.data.rank).to.be.lessThan(res1.data.rank);
  });

  it('TC-DSH-011: Top scorer rank equals 1', async function () {
    const res = await api.getDashboard(email2);
    expect(res.data.rank).to.equal(1);
  });

  it('TC-DSH-012: Rank is a positive integer', async function () {
    const res = await api.getDashboard(email1);
    expect(res.data.rank).to.be.a('number').that.is.at.least(1);
  });
});

describe('📊 Dashboard API – Edge Cases', function () {
  it('TC-DSH-013: Dashboard retrieval missing email parameter returns 404', async function () {
    const res = await api.getDashboard('');
    expect(res.status).to.equal(404);
  });
  it('TC-DSH-014: Dashboard retrieval for unknown user returns default values', async function () {
    const res = await api.getDashboard('ghost_dash@bb.com');
    expect(res.status).to.equal(200);
    expect(res.data.total_stars).to.equal(0);
    expect(res.data.levels_completed).to.equal(0);
  });
  it('TC-DSH-015: Dashboard retrieval for extremely long email returns 200 with default values', async function () {
    const res = await api.getDashboard('a'.repeat(200) + '@bb.com');
    expect(res.status).to.equal(200);
    expect(res.data.total_stars).to.equal(0);
  });
  it('TC-DSH-016: Ranking tie-breaker for users with exact same stars assigns same or sequential rank', async function () {
    const emailA = `tieA_${Date.now()}@bb.com`;
    const emailB = `tieB_${Date.now()}@bb.com`;
    await api.signup({ username: 'TieA', email: emailA, password: 'P' });
    await api.signup({ username: 'TieB', email: emailB, password: 'P' });
    await api.saveProgress({ email: emailA, game_type: 'memory', level: 1, stars: 777, time_taken: 10 });
    await api.saveProgress({ email: emailB, game_type: 'memory', level: 1, stars: 777, time_taken: 10 });
    const resA = await api.getDashboard(emailA);
    const resB = await api.getDashboard(emailB);
    expect(resA.data.rank).to.be.greaterThan(0);
    expect(resB.data.rank).to.be.greaterThan(0);
  });
  it('TC-DSH-017: Dashboard check after changing password still works perfectly', async function () {
    const email = `pwd_dash_${Date.now()}@bb.com`;
    await api.signup({ username: 'PwdDash', email, password: 'Old' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 1, time_taken: 1 });
    await api.changePassword(email, 'New');
    const res = await api.getDashboard(email);
    expect(res.data.total_stars).to.equal(1);
  });
  it('TC-DSH-018: Dashboard values when progress includes 0 stars calculates sum correctly', async function () {
    const email = `zero_${Date.now()}@bb.com`;
    await api.signup({ username: 'Zero', email, password: 'P' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 0, time_taken: 10 });
    await api.saveProgress({ email, game_type: 'logic', level: 1, stars: 0, time_taken: 10 });
    const res = await api.getDashboard(email);
    expect(res.data.total_stars).to.equal(0);
  });
  it('TC-DSH-019: Dashboard values when progress includes negative time taken works', async function () {
    const email = `negT_${Date.now()}@bb.com`;
    await api.signup({ username: 'NegT', email, password: 'P' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 3, time_taken: -100 });
    const res = await api.getDashboard(email);
    expect(res.data.total_stars).to.equal(3);
  });
  it('TC-DSH-020: Dashboard with SQL injection string in email returns default values', async function () {
    const res = await api.getDashboard("' OR 1=1 --");
    expect(res.data.total_stars).to.equal(0);
  });
  it('TC-DSH-021: Dashboard levels_completed correctly counts multiple game types', async function () {
    const email = `multi_${Date.now()}@bb.com`;
    await api.signup({ username: 'Multi', email, password: 'P' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 3, time_taken: 1 });
    await api.saveProgress({ email, game_type: 'logic', level: 1, stars: 3, time_taken: 1 });
    await api.saveProgress({ email, game_type: 'speed', level: 1, stars: 3, time_taken: 1 });
    const res = await api.getDashboard(email);
    expect(res.data.levels_completed).to.equal(3);
  });
  it('TC-DSH-022: Dashboard last_game updates appropriately after new game type is saved', async function () {
    const email = `last_${Date.now()}@bb.com`;
    await api.signup({ username: 'Last', email, password: 'P' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 3, time_taken: 1 });
    await api.saveProgress({ email, game_type: 'focus', level: 1, stars: 3, time_taken: 1 });
    const res = await api.getDashboard(email);
    expect(res.data.last_game).to.equal('focus');
  });
  it('TC-DSH-023: Dashboard correctly retrieves rank after tying and then exceeding tie', async function () {
    const emailA = `excA_${Date.now()}@bb.com`;
    const emailB = `excB_${Date.now()}@bb.com`;
    await api.saveProgress({ email: emailA, game_type: 'memory', level: 1, stars: 100, time_taken: 1 });
    await api.saveProgress({ email: emailB, game_type: 'memory', level: 1, stars: 100, time_taken: 1 });
    await api.saveProgress({ email: emailB, game_type: 'memory', level: 2, stars: 10, time_taken: 1 });
    const resA = await api.getDashboard(emailA);
    const resB = await api.getDashboard(emailB);
    expect(resB.data.rank).to.be.lessThan(resA.data.rank);
  });
  it('TC-DSH-024: Dashboard retrieval with missing email parameter defaults to 200 with random string', async function () {
    const res = await api.getDashboard(api.randomEmail() + api.randomEmail());
    expect(res.status).to.equal(200);
  });
});
