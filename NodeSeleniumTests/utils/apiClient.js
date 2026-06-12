// utils/apiClient.js
// ==================
// Centralised API client for Brain Battle Flask backend
// All Selenium/Node.js tests import this module.

const axios = require('axios');

const BASE_URL = 'http://127.0.0.1:5000';   // Flask backend

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
  validateStatus: () => true,   // never throw on any HTTP status
});

// ── Auth ────────────────────────────────────────────────────────
const signup  = (data) => client.post('/api/auth/signup', data);
const login   = (data) => client.post('/api/auth/login',  data);

// ── User ────────────────────────────────────────────────────────
const getUser         = (email)           => client.post('/api/user/get-user',        { email });
const forgotPassword  = (email)           => client.post('/api/user/forgot-password', { email });
const changePassword  = (email, password) => client.post('/api/user/change-password', { email, password });

// ── Progress ─────────────────────────────────────────────────────
const saveProgress  = (data) => client.post('/api/progress/save', data);
const getProgress   = (email, game) => client.get(`/api/progress/get/${email}/${game}`);

// ── Dashboard ────────────────────────────────────────────────────
const getDashboard  = (email) => client.get(`/api/dashboard/${email}`);

// ── Helpers ──────────────────────────────────────────────────────
const randomEmail = () => `test_${Date.now()}_${Math.random().toString(36).slice(2,6)}@bb.com`;

module.exports = {
  BASE_URL,
  signup, login,
  getUser, forgotPassword, changePassword,
  saveProgress, getProgress,
  getDashboard,
  randomEmail,
};
