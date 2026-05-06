const fs = require('fs');
const path = require('path');
const db = require('../models');
const cryptoUtil = require('../utils/crypto');

function getFileList({ page = 1, pageSize = 10, keyword = '', fileType = '' }) {
  let where = 'WHERE status = 1';
  const params = [];

  if (keyword) {
    where += ' AND (title LIKE ? OR description LIKE ?)';
    params.push(`%${keyword}%`, `%${keyword}%`);
  }
  if (fileType) {
    where += ' AND file_type = ?';
    params.push(fileType);
  }

  const total = db.prepare(`SELECT COUNT(*) as count FROM files ${where}`).get(...params).count;

  const offset = (page - 1) * pageSize;
  const list = db.prepare(`SELECT * FROM files ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`).all(...params, pageSize, offset);

  return { list, total };
}

function getFileById(id) {
  return db.prepare('SELECT * FROM files WHERE id = ?').get(id);
}

function createFile(fileData) {
  const encryptedPath = cryptoUtil.encrypt(fileData.file_path);
  const stmt = db.prepare(`
    INSERT INTO files (title, description, file_type, file_path, file_size, preview_pages, total_pages, price, cover_image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const result = stmt.run(
    fileData.title,
    fileData.description || null,
    fileData.file_type,
    encryptedPath,
    fileData.file_size || 0,
    fileData.preview_pages || 3,
    fileData.total_pages || 0,
    fileData.price || 0,
    fileData.cover_image || null
  );
  return result.lastInsertRowid;
}

function updateFile(id, fileData) {
  const fields = [];
  const params = [];

  const allowedFields = ['title', 'description', 'file_type', 'file_size', 'preview_pages', 'total_pages', 'price', 'cover_image', 'status'];
  for (const field of allowedFields) {
    if (fileData[field] !== undefined) {
      fields.push(`${field} = ?`);
      params.push(fileData[field]);
    }
  }

  if (fields.length === 0) return false;

  fields.push('updated_at = CURRENT_TIMESTAMP');
  params.push(id);

  const stmt = db.prepare(`UPDATE files SET ${fields.join(', ')} WHERE id = ?`);
  const result = stmt.run(...params);
  return result.changes > 0;
}

function deleteFile(id) {
  const file = getFileById(id);
  if (!file) return false;

  try {
    const realPath = cryptoUtil.decrypt(file.file_path);
    const fullPath = path.resolve(realPath);
    if (fs.existsSync(fullPath)) {
      fs.unlinkSync(fullPath);
    }
  } catch (e) {}

  const stmt = db.prepare('UPDATE files SET status = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?');
  const result = stmt.run(id);
  return result.changes > 0;
}

function incrementViewCount(id) {
  db.prepare('UPDATE files SET view_count = view_count + 1 WHERE id = ?').run(id);
}

function incrementDownloadCount(id) {
  db.prepare('UPDATE files SET download_count = download_count + 1 WHERE id = ?').run(id);
}

function getPreviewContent(file, hasPurchased) {
  const realPath = cryptoUtil.decrypt(file.file_path);
  const fullPath = path.resolve(realPath);

  if (!fs.existsSync(fullPath)) {
    return null;
  }

  if (file.file_type === 'pdf') {
    const pdfBuffer = fs.readFileSync(fullPath);
    const base64Pdf = pdfBuffer.toString('base64');
    return {
      type: 'pdf',
      data: base64Pdf,
      previewPages: hasPurchased ? file.total_pages : file.preview_pages,
      totalPages: file.total_pages,
      hasPurchased
    };
  }

  if (file.file_type === 'docx') {
    const docxBuffer = fs.readFileSync(fullPath);
    const base64Docx = docxBuffer.toString('base64');
    return {
      type: 'docx',
      data: base64Docx,
      previewOnly: !hasPurchased,
      hasPurchased
    };
  }

  return null;
}

function getDownloadStream(file) {
  const realPath = cryptoUtil.decrypt(file.file_path);
  const fullPath = path.resolve(realPath);
  if (!fs.existsSync(fullPath)) return null;
  return fullPath;
}

function checkUserPermission(userId, fileId) {
  const row = db.prepare('SELECT * FROM user_files WHERE user_id = ? AND file_id = ? AND can_download = 1').get(userId, fileId);
  return !!row;
}

function grantUserAccess(userId, fileId, orderId) {
  const existing = db.prepare('SELECT * FROM user_files WHERE user_id = ? AND file_id = ?').get(userId, fileId);
  if (existing) {
    db.prepare('UPDATE user_files SET can_preview = 1, can_download = 1 WHERE id = ?').run(existing.id);
    return;
  }
  db.prepare('INSERT INTO user_files (user_id, file_id, order_id, can_preview, can_download) VALUES (?, ?, ?, 1, 1)').run(userId, fileId, orderId);
}

module.exports = {
  getFileList,
  getFileById,
  createFile,
  updateFile,
  deleteFile,
  incrementViewCount,
  incrementDownloadCount,
  getPreviewContent,
  getDownloadStream,
  checkUserPermission,
  grantUserAccess
};
