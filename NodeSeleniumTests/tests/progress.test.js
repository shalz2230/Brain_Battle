// tests/progress.test.js
// =======================
// Selenium-style E2E API Tests – Game Progress
// TC-PRG-001 … TC-PRG-014

const { expect } = require('chai');
const api = require('../utils/apiClient');

describe('🎮 Progress API – Save Progress', function () {

  const email = `prg_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'ProgressUser', email, password: 'Prog123' });
  });

  it('TC-PRG-001: Save new memory progress returns success', async function () {
    const res = await api.saveProgress({
      email, game_type: 'memory', level: 1, stars: 3, time_taken: 30
    });
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
  });

  it('TC-PRG-002: Save logic progress returns success', async function () {
    const res = await api.saveProgress({
      email, game_type: 'logic', level: 1, stars: 3, time_taken: 15
    });
    expect(res.status).to.equal(200);
    expect(res.data.status).to.equal('success');
  });

  it('TC-PRG-003: Save focus progress returns success', async function () {
    const res = await api.saveProgress({
      email, game_type: 'focus', level: 1, stars: 3, time_taken: 10
    });
    expect(res.status).to.equal(200);
  });

  it('TC-PRG-004: Save speed progress returns success', async function () {
    const res = await api.saveProgress({
      email, game_type: 'speed', level: 1, stars: 2, time_taken: 8
    });
    expect(res.status).to.equal(200);
  });

  it('TC-PRG-005: Upsert – saving same level twice updates, not duplicates', async function () {
    await api.saveProgress({ email, game_type: 'memory', level: 2, stars: 1, time_taken: 60 });
    await api.saveProgress({ email, game_type: 'memory', level: 2, stars: 3, time_taken: 20 });
    const res = await api.getProgress(email, 'memory');
    const level2Items = res.data.filter(p => p.level === 2);
    expect(level2Items).to.have.lengthOf(1);
    expect(level2Items[0].stars).to.equal(3);
  });

  it('TC-PRG-006: Saved progress has is_completed flag = true', async function () {
    const res = await api.getProgress(email, 'memory');
    const lvl1 = res.data.find(p => p.level === 1);
    expect(lvl1).to.exist;
    expect(lvl1.completed).to.equal(true);
  });
});


describe('📋 Progress API – Get Progress', function () {

  const email = `get_prg_${Date.now()}@bb.com`;

  before(async () => {
    await api.signup({ username: 'GetProgUser', email, password: 'GetProg1' });
    await api.saveProgress({ email, game_type: 'memory', level: 1, stars: 3, time_taken: 25 });
    await api.saveProgress({ email, game_type: 'memory', level: 2, stars: 2, time_taken: 40 });
    await api.saveProgress({ email, game_type: 'logic',  level: 1, stars: 3, time_taken: 12 });
  });

  it('TC-PRG-007: Get memory progress returns list with correct count', async function () {
    const res = await api.getProgress(email, 'memory');
    expect(res.status).to.equal(200);
    expect(res.data).to.be.an('array').with.lengthOf(2);
  });

  it('TC-PRG-008: Get progress items contain level, stars, completed fields', async function () {
    const res = await api.getProgress(email, 'memory');
    res.data.forEach(item => {
      expect(item).to.have.property('level').that.is.a('number');
      expect(item).to.have.property('stars').that.is.a('number');
      expect(item).to.have.property('completed').that.is.a('boolean');
    });
  });

  it('TC-PRG-009: Get progress for unplayed game type returns empty list', async function () {
    const res = await api.getProgress(email, 'speed');
    expect(res.status).to.equal(200);
    expect(res.data).to.be.an('array').with.lengthOf(0);
  });

  it('TC-PRG-010: Get logic progress returns correct single entry', async function () {
    const res = await api.getProgress(email, 'logic');
    expect(res.data).to.have.lengthOf(1);
    expect(res.data[0].level).to.equal(1);
    expect(res.data[0].stars).to.equal(3);
  });

  it('TC-PRG-011: Stars value stored correctly (1–3 range)', async function () {
    const res = await api.getProgress(email, 'memory');
    res.data.forEach(item => {
      expect(item.stars).to.be.within(1, 3);
    });
  });

  it('TC-PRG-012: Level numbers stored correctly in ascending order', async function () {
    const res = await api.getProgress(email, 'memory');
    const levels = res.data.map(p => p.level).sort((a,b) => a-b);
    expect(levels).to.deep.equal([1, 2]);
  });

  it('TC-PRG-013: Progress for unknown email returns empty list', async function () {
    const res = await api.getProgress('noone@bb.com', 'memory');
    expect(res.status).to.equal(200);
    expect(res.data).to.be.an('array').with.lengthOf(0);
  });

  it('TC-PRG-014: Multiple game types tracked independently', async function () {
    const memRes = await api.getProgress(email, 'memory');
    const lgcRes = await api.getProgress(email, 'logic');
    expect(memRes.data.length).to.equal(2);
    expect(lgcRes.data.length).to.equal(1);
  });
});

describe('📋 Progress API – Edge Cases', function () {
  const email = `edge_prg_${Date.now()}@bb.com`;
  before(async () => {
    await api.signup({ username: 'EdgeProg', email, password: 'P1' });
  });

  it('TC-PRG-015: Save progress with negative stars returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'memory', level: 99, stars: -1, time_taken: 10 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-016: Save progress with string for level returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'memory', level: "ten", stars: 2, time_taken: 10 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-017: Save progress missing game_type saves and returns 500 (IntegrityError)', async function () {
    const res = await api.saveProgress({ email, level: 10, stars: 2, time_taken: 10 });
    expect(res.status).to.equal(500);
  });
  it('TC-PRG-018: Save progress missing level saves and returns 500 (IntegrityError)', async function () {
    const res = await api.saveProgress({ email, game_type: 'speed', stars: 2, time_taken: 10 });
    expect(res.status).to.equal(500);
  });
  it('TC-PRG-019: Save progress missing stars saves and returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'speed', level: 11, time_taken: 10 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-020: Save progress missing time_taken saves and returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'speed', level: 12, stars: 3 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-021: Save progress for unknown email returns 200', async function () {
    const res = await api.saveProgress({ email: 'ghost_prog@bb.com', game_type: 'memory', level: 1, stars: 1, time_taken: 1 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-022: Get progress for extremely long email returns empty list 200', async function () {
    const res = await api.getProgress('a'.repeat(200) + '@bb.com', 'memory');
    expect(res.status).to.equal(200);
    expect(res.data).to.be.an('array').with.lengthOf(0);
  });
  it('TC-PRG-023: Save progress with extremely long game_type returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'g'.repeat(200), level: 1, stars: 3, time_taken: 10 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-024: Get progress with extremely long game_type returns valid array', async function () {
    const res = await api.getProgress(email, 'g'.repeat(200));
    expect(res.status).to.equal(200);
    expect(res.data).to.be.an('array').with.lengthOf(1);
  });
  it('TC-PRG-025: Save progress with stars > 3 returns 200', async function () {
    const res = await api.saveProgress({ email, game_type: 'focus', level: 50, stars: 99, time_taken: 10 });
    expect(res.status).to.equal(200);
  });
  it('TC-PRG-026: Save progress with empty body returns 500 (IntegrityError)', async function () {
    const res = await api.saveProgress({});
    expect(res.status).to.equal(500);
  });
});
