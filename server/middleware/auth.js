const jwt = require('jsonwebtoken');
const config = require('../config');
const response = require('../utils/response');

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json(response.error('未提供认证令牌', 401));
  }
  try {
    const decoded = jwt.verify(token, config.jwt.secret);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json(response.error('令牌无效或已过期', 401));
  }
}

function adminMiddleware(req, res, next) {
  if (!req.user || !req.user.isAdmin) {
    return res.status(403).json(response.error('需要管理员权限', 403));
  }
  next();
}

module.exports = { authMiddleware, adminMiddleware };
