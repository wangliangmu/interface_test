const express = require('express');
const router = express.Router();
const response = require('../utils/response');
const { authMiddleware } = require('../middleware/auth');
const paymentService = require('../services/paymentService');
const fileService = require('../services/fileService');

router.post('/', authMiddleware, (req, res) => {
  try {
    const { file_id } = req.body;
    if (!file_id) {
      return res.status(400).json(response.error('缺少file_id参数'));
    }

    const file = fileService.getFileById(file_id);
    if (!file || file.status !== 1) {
      return res.status(404).json(response.error('文件不存在'));
    }

    const hasPermission = fileService.checkUserPermission(req.user.id, file_id);
    if (hasPermission) {
      return res.json(response.error('您已购买此文件', 10001));
    }

    const result = paymentService.createOrder(req.user.id, file_id);
    if (result.existing) {
      return res.json(response.success(result.order, '您已购买此文件'));
    }

    res.json(response.success(result.order));
  } catch (e) {
    res.status(500).json(response.error('创建订单失败: ' + e.message));
  }
});

router.get('/', authMiddleware, (req, res) => {
  try {
    const { page = 1, pageSize = 10 } = req.query;
    const result = paymentService.getOrdersByUserId(req.user.id, { page: parseInt(page), pageSize: parseInt(pageSize) });
    res.json(response.success(response.paginate(result.list, result.total, page, pageSize)));
  } catch (e) {
    res.status(500).json(response.error('获取订单列表失败: ' + e.message));
  }
});

router.get('/:id', authMiddleware, (req, res) => {
  try {
    const order = paymentService.getOrderById(req.params.id);
    if (!order) {
      return res.status(404).json(response.error('订单不存在'));
    }
    if (order.user_id !== req.user.id && !req.user.isAdmin) {
      return res.status(403).json(response.error('无权查看此订单'));
    }
    res.json(response.success(order));
  } catch (e) {
    res.status(500).json(response.error('获取订单详情失败: ' + e.message));
  }
});

router.post('/:id/pay', authMiddleware, (req, res) => {
  try {
    const result = paymentService.simulatePayment(parseInt(req.params.id), req.user.id);
    if (result.success) {
      res.json(response.success({ transaction_id: result.transactionId }, '支付成功'));
    } else {
      res.status(400).json(response.error(result.message));
    }
  } catch (e) {
    res.status(500).json(response.error('支付失败: ' + e.message));
  }
});

router.post('/:id/callback', (req, res) => {
  try {
    const result = paymentService.paymentCallback(parseInt(req.params.id), req.body);
    if (result.success) {
      res.json(response.success(null, '回调处理成功'));
    } else {
      res.status(400).json(response.error(result.message));
    }
  } catch (e) {
    res.status(500).json(response.error('回调处理失败: ' + e.message));
  }
});

module.exports = router;
