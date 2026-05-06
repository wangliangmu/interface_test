const multer = require('multer');
const path = require('path');
const crypto = require('../utils/crypto');
const config = require('../config');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, config.upload.dir);
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname);
    const basename = path.basename(file.originalname, ext);
    const timestamp = Date.now();
    const randomStr = Math.random().toString(36).substring(2, 8);
    cb(null, `${basename}_${timestamp}_${randomStr}${ext}`);
  }
});

function fileFilter(req, file, cb) {
  const ext = path.extname(file.originalname).toLowerCase();
  if (config.upload.allowedTypes.includes(ext)) {
    cb(null, true);
  } else {
    cb(new Error(`不支持的文件类型，仅允许: ${config.upload.allowedTypes.join(', ')}`));
  }
}

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: config.upload.maxSize
  }
});

module.exports = upload;
