const express = require('express');
const router = express.Router();
const path = require('path');
const response = require('../utils/response');
const { authMiddleware, adminMiddleware } = require('../middleware/auth');
const upload = require('../middleware/upload');
const fileService = require('../services/fileService');
const paymentService = require('../services/paymentService');
const userService = require('../services/userService');
const db = require('../models');

router.get('/dashboard', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const userCount = db.prepare('SELECT COUNT(*) as count FROM users').get().count;
    const fileCount = db.prepare('SELECT COUNT(*) as count FROM files WHERE status = 1').get().count;
    const orderCount = db.prepare('SELECT COUNT(*) as count FROM orders').get().count;
    const totalRevenue = db.prepare("SELECT COALESCE(SUM(amount), 0) as total FROM orders WHERE status = 'paid'").get().total;
    const todayOrders = db.prepare("SELECT COUNT(*) as count FROM orders WHERE date(created_at) = date('now')").get().count;
    const todayRevenue = db.prepare("SELECT COALESCE(SUM(amount), 0) as total FROM orders WHERE status = 'paid' AND date(paid_at) = date('now')").get().total;

    const recentOrders = db.prepare('SELECT o.*, u.nickname, f.title as file_title FROM orders o LEFT JOIN users u ON o.user_id = u.id LEFT JOIN files f ON o.file_id = f.id ORDER BY o.created_at DESC LIMIT 10').all();
    const popularFiles = db.prepare('SELECT * FROM files WHERE status = 1 ORDER BY download_count DESC LIMIT 5').all();

    res.json(response.success({
      stats: { userCount, fileCount, orderCount, totalRevenue, todayOrders, todayRevenue },
      recentOrders,
      popularFiles
    }));
  } catch (e) {
    res.status(500).json(response.error('获取仪表盘数据失败: ' + e.message));
  }
});

router.get('/files', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const { page = 1, pageSize = 10, keyword = '', status = '' } = req.query;
    let where = '';
    const params = [];

    const conditions = [];
    if (keyword) {
      conditions.push('(title LIKE ? OR description LIKE ?)');
      params.push(`%${keyword}%`, `%${keyword}%`);
    }
    if (status !== '') {
      conditions.push('status = ?');
      params.push(parseInt(status));
    }
    if (conditions.length > 0) {
      where = 'WHERE ' + conditions.join(' AND ');
    }

    const total = db.prepare(`SELECT COUNT(*) as count FROM files ${where}`).get(...params).count;
    const offset = (page - 1) * pageSize;
    const list = db.prepare(`SELECT * FROM files ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`).all(...params, parseInt(pageSize), offset);

    res.json(response.success(response.paginate(list, total, page, pageSize)));
  } catch (e) {
    res.status(500).json(response.error('获取文件列表失败: ' + e.message));
  }
});

router.post('/files', authMiddleware, adminMiddleware, upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json(response.error('请上传文件'));
    }

    const { title, description, price, preview_pages, total_pages, cover_image } = req.body;
    const ext = path.extname(req.file.originalname).toLowerCase().replace('.', '');
    const fileData = {
      title: title || req.file.originalname,
      description: description || null,
      file_type: ext,
      file_path: req.file.path,
      file_size: req.file.size,
      preview_pages: preview_pages ? parseInt(preview_pages) : 3,
      total_pages: total_pages ? parseInt(total_pages) : 0,
      price: price ? parseFloat(price) : 0,
      cover_image: cover_image || null
    };

    const id = fileService.createFile(fileData);
    res.json(response.success({ id }, '文件上传成功'));
  } catch (e) {
    res.status(500).json(response.error('上传文件失败: ' + e.message));
  }
});

router.put('/files/:id', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const file = fileService.getFileById(req.params.id);
    if (!file) {
      return res.status(404).json(response.error('文件不存在'));
    }

    const updated = fileService.updateFile(req.params.id, req.body);
    if (updated) {
      res.json(response.success(null, '更新成功'));
    } else {
      res.status(400).json(response.error('更新失败'));
    }
  } catch (e) {
    res.status(500).json(response.error('更新文件失败: ' + e.message));
  }
});

router.delete('/files/:id', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const deleted = fileService.deleteFile(req.params.id);
    if (deleted) {
      res.json(response.success(null, '删除成功'));
    } else {
      res.status(404).json(response.error('文件不存在'));
    }
  } catch (e) {
    res.status(500).json(response.error('删除文件失败: ' + e.message));
  }
});

router.get('/orders', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const { page = 1, pageSize = 10, status = '' } = req.query;
    const result = paymentService.getAllOrders({ page: parseInt(page), pageSize: parseInt(pageSize), status });
    res.json(response.success(response.paginate(result.list, result.total, page, pageSize)));
  } catch (e) {
    res.status(500).json(response.error('获取订单列表失败: ' + e.message));
  }
});

router.get('/users', authMiddleware, adminMiddleware, (req, res) => {
  try {
    const { page = 1, pageSize = 10, keyword = '' } = req.query;
    const result = userService.getAllUsers({ page: parseInt(page), pageSize: parseInt(pageSize), keyword });
    res.json(response.success(response.paginate(result.list, result.total, page, pageSize)));
  } catch (e) {
    res.status(500).json(response.error('获取用户列表失败: ' + e.message));
  }
});

module.exports = router;
