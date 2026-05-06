const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const response = require('../utils/response');
const { authMiddleware } = require('../middleware/auth');
const fileService = require('../services/fileService');

router.get('/', (req, res) => {
  try {
    const { page = 1, pageSize = 10, keyword = '', fileType = '' } = req.query;
    const result = fileService.getFileList({ page: parseInt(page), pageSize: parseInt(pageSize), keyword, fileType });
    res.json(response.success(response.paginate(result.list, result.total, page, pageSize)));
  } catch (e) {
    res.status(500).json(response.error('获取文件列表失败: ' + e.message));
  }
});

router.get('/:id', (req, res) => {
  try {
    const file = fileService.getFileById(req.params.id);
    if (!file || file.status !== 1) {
      return res.status(404).json(response.error('文件不存在'));
    }
    fileService.incrementViewCount(file.id);
    res.json(response.success(file));
  } catch (e) {
    res.status(500).json(response.error('获取文件详情失败: ' + e.message));
  }
});

router.get('/:id/preview', authMiddleware, (req, res) => {
  try {
    const file = fileService.getFileById(req.params.id);
    if (!file || file.status !== 1) {
      return res.status(404).json(response.error('文件不存在'));
    }

    const hasPurchased = fileService.checkUserPermission(req.user.id, file.id);
    const previewContent = fileService.getPreviewContent(file, hasPurchased);

    if (!previewContent) {
      return res.status(404).json(response.error('文件内容不可用'));
    }

    fileService.incrementViewCount(file.id);
    res.json(response.success(previewContent));
  } catch (e) {
    res.status(500).json(response.error('获取预览内容失败: ' + e.message));
  }
});

router.get('/:id/download', authMiddleware, (req, res) => {
  try {
    const file = fileService.getFileById(req.params.id);
    if (!file || file.status !== 1) {
      return res.status(404).json(response.error('文件不存在'));
    }

    const hasPermission = fileService.checkUserPermission(req.user.id, file.id);
    if (!hasPermission) {
      return res.status(403).json(response.error('无下载权限，请先购买'));
    }

    const filePath = fileService.getDownloadStream(file);
    if (!filePath) {
      return res.status(404).json(response.error('文件不存在'));
    }

    fileService.incrementDownloadCount(file.id);

    const ext = path.extname(filePath);
    const mimeType = ext === '.pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

    res.setHeader('Content-Type', mimeType);
    res.setHeader('Content-Disposition', `attachment; filename="${encodeURIComponent(file.title + ext)}"`);
    const fileStream = fs.createReadStream(filePath);
    fileStream.pipe(res);
  } catch (e) {
    res.status(500).json(response.error('下载失败: ' + e.message));
  }
});

module.exports = router;
