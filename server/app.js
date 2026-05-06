const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const path = require('path');
const fs = require('fs');
const config = require('./config');

const app = express();

const uploadsDir = path.resolve(config.upload.dir);
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

app.use(helmet({ crossOriginResourcePolicy: { policy: 'cross-origin' } }));
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 500,
  message: { code: -1, message: '请求过于频繁，请稍后再试', data: null }
});
app.use(globalLimiter);

const apiLimiter = rateLimit({
  windowMs: 1 * 60 * 1000,
  max: 60,
  message: { code: -1, message: 'API请求过于频繁，请稍后再试', data: null }
});
app.use('/api/', apiLimiter);

require('./models');

const authRoutes = require('./routes/auth');
const fileRoutes = require('./routes/files');
const orderRoutes = require('./routes/orders');
const adminRoutes = require('./routes/admin');

app.use('/api/auth', authRoutes);
app.use('/api/files', fileRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/admin', adminRoutes);

app.use('/uploads', express.static(uploadsDir));

app.use((err, req, res, next) => {
  if (err.name === 'MulterError') {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ code: -1, message: '文件大小超出限制', data: null });
    }
    return res.status(400).json({ code: -1, message: `上传错误: ${err.message}`, data: null });
  }
  if (err.message && err.message.includes('不支持的文件类型')) {
    return res.status(400).json({ code: -1, message: err.message, data: null });
  }
  console.error(err);
  res.status(500).json({ code: -1, message: '服务器内部错误', data: null });
});

app.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});

module.exports = app;
