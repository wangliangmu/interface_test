const db = require('../models');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('../config');

function findOrCreateByOpenid(openid, userInfo) {
  let user = db.prepare('SELECT * FROM users WHERE openid = ?').get(openid);
  if (!user) {
    const stmt = db.prepare('INSERT INTO users (openid, nickname, avatar_url) VALUES (?, ?, ?)');
    const result = stmt.run(openid, userInfo.nickname || '', userInfo.avatar_url || '');
    user = db.prepare('SELECT * FROM users WHERE id = ?').get(result.lastInsertRowid);
  } else {
    if (userInfo.nickname || userInfo.avatar_url) {
      db.prepare('UPDATE users SET nickname = ?, avatar_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').run(
        userInfo.nickname || user.nickname,
        userInfo.avatar_url || user.avatar_url,
        user.id
      );
      user = db.prepare('SELECT * FROM users WHERE id = ?').get(user.id);
    }
  }
  return user;
}

function generateToken(user) {
  return jwt.sign(
    {
      id: user.id,
      openid: user.openid,
      isAdmin: !!user.is_admin
    },
    config.jwt.secret,
    { expiresIn: config.jwt.expiresIn }
  );
}

function adminLogin(username, password) {
  if (username !== config.admin.username) return null;
  const isValid = password === config.admin.password;
  if (!isValid) return null;

  let admin = db.prepare('SELECT * FROM users WHERE is_admin = 1').get();
  if (!admin) {
    const stmt = db.prepare('INSERT INTO users (openid, nickname, is_admin) VALUES (?, ?, ?)');
    const result = stmt.run(`admin_${Date.now()}`, '管理员', 1);
    admin = db.prepare('SELECT * FROM users WHERE id = ?').get(result.lastInsertRowid);
  }

  return admin;
}

function getUserById(id) {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(id);
}

function getAllUsers({ page = 1, pageSize = 10, keyword = '' }) {
  let where = '';
  const params = [];

  if (keyword) {
    where = 'WHERE nickname LIKE ? OR phone LIKE ?';
    params.push(`%${keyword}%`, `%${keyword}%`);
  }

  const total = db.prepare(`SELECT COUNT(*) as count FROM users ${where}`).get(...params).count;
  const offset = (page - 1) * pageSize;
  const list = db.prepare(`SELECT * FROM users ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`).all(...params, pageSize, offset);
  return { list, total };
}

function getUserCount() {
  return db.prepare('SELECT COUNT(*) as count FROM users').get().count;
}

module.exports = {
  findOrCreateByOpenid,
  generateToken,
  adminLogin,
  getUserById,
  getAllUsers,
  getUserCount
};
