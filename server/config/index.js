require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  jwt: {
    secret: process.env.JWT_SECRET || 'wx-file-preview-jwt-secret-key-2024',
    expiresIn: process.env.JWT_EXPIRES_IN || '7d'
  },
  wx: {
    appid: process.env.WX_APPID || 'wx1234567890abcdef',
    secret: process.env.WX_SECRET || 'your-wechat-secret-key'
  },
  upload: {
    dir: process.env.UPLOAD_DIR || 'uploads',
    maxSize: parseInt(process.env.MAX_FILE_SIZE) || 50 * 1024 * 1024,
    allowedTypes: ['.pdf', '.docx']
  },
  admin: {
    username: process.env.ADMIN_USERNAME || 'admin',
    password: process.env.ADMIN_PASSWORD || 'admin123'
  },
  database: {
    path: process.env.DB_PATH || './data.db'
  },
  crypto: {
    key: process.env.CRYPTO_KEY || 'wx-file-crypto-key-2024-aes256'
  }
};
