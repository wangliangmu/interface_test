const db = require('../models');
const { v4: uuidv4 } = require('uuid');
const fileService = require('./fileService');

function createOrder(userId, fileId) {
  const file = fileService.getFileById(fileId);
  if (!file) return null;

  const existingOrder = db.prepare(
    "SELECT * FROM orders WHERE user_id = ? AND file_id = ? AND status = 'paid'"
  ).get(userId, fileId);
  if (existingOrder) return { existing: true, order: existingOrder };

  const orderNo = `ORD${Date.now()}${uuidv4().substring(0, 8).replace(/-/g, '')}`.toUpperCase();

  const stmt = db.prepare(
    'INSERT INTO orders (order_no, user_id, file_id, amount, status) VALUES (?, ?, ?, ?, ?)'
  );
  const result = stmt.run(orderNo, userId, fileId, file.price, 'pending');

  return {
    existing: false,
    order: {
      id: result.lastInsertRowid,
      order_no: orderNo,
      user_id: userId,
      file_id: fileId,
      amount: file.price,
      status: 'pending'
    }
  };
}

function getOrderById(id) {
  return db.prepare('SELECT * FROM orders WHERE id = ?').get(id);
}

function getOrdersByUserId(userId, { page = 1, pageSize = 10 }) {
  const total = db.prepare('SELECT COUNT(*) as count FROM orders WHERE user_id = ?').get(userId).count;
  const offset = (page - 1) * pageSize;
  const list = db.prepare('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?').all(userId, pageSize, offset);
  return { list, total };
}

function getAllOrders({ page = 1, pageSize = 10, status = '' }) {
  let where = '';
  const params = [];

  if (status) {
    where = 'WHERE status = ?';
    params.push(status);
  }

  const total = db.prepare(`SELECT COUNT(*) as count FROM orders ${where}`).get(...params).count;
  const offset = (page - 1) * pageSize;
  const list = db.prepare(`SELECT * FROM orders ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`).all(...params, pageSize, offset);
  return { list, total };
}

function simulatePayment(orderId, userId) {
  const order = getOrderById(orderId);
  if (!order) return { success: false, message: '订单不存在' };
  if (order.status === 'paid') return { success: false, message: '订单已支付' };
  if (order.status === 'cancelled') return { success: false, message: '订单已取消' };
  if (order.user_id !== userId) return { success: false, message: '无权操作此订单' };

  const transactionId = `TXN${Date.now()}${Math.random().toString(36).substring(2, 8)}`.toUpperCase();

  const updateOrder = db.prepare(`
    UPDATE orders SET status = 'paid', payment_method = 'wechat', transaction_id = ?, paid_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?
  `);
  updateOrder.run(transactionId, orderId);

  const insertPayment = db.prepare(`
    INSERT INTO payments (order_id, user_id, file_id, amount, payment_type, status, transaction_id, raw_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);
  insertPayment.run(orderId, userId, order.file_id, order.amount, 'wechat', 'success', transactionId, JSON.stringify({ simulated: true }));

  fileService.grantUserAccess(userId, order.file_id, orderId);

  return { success: true, transactionId };
}

function paymentCallback(orderId, callbackData) {
  const order = getOrderById(orderId);
  if (!order) return { success: false, message: '订单不存在' };

  if (callbackData.status === 'success') {
    const updateOrder = db.prepare(`
      UPDATE orders SET status = 'paid', payment_method = ?, transaction_id = ?, paid_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    `);
    updateOrder.run(callbackData.payment_method || 'wechat', callbackData.transaction_id || '', orderId);

    const insertPayment = db.prepare(`
      INSERT INTO payments (order_id, user_id, file_id, amount, payment_type, status, transaction_id, raw_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    insertPayment.run(orderId, order.user_id, order.file_id, order.amount, callbackData.payment_type || 'wechat', 'success', callbackData.transaction_id || '', JSON.stringify(callbackData));

    fileService.grantUserAccess(order.user_id, order.file_id, orderId);
    return { success: true };
  }

  if (callbackData.status === 'failed') {
    db.prepare("UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?").run(orderId);
    const insertPayment = db.prepare(`
      INSERT INTO payments (order_id, user_id, file_id, amount, payment_type, status, transaction_id, raw_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    insertPayment.run(orderId, order.user_id, order.file_id, order.amount, callbackData.payment_type || 'wechat', 'failed', callbackData.transaction_id || '', JSON.stringify(callbackData));
    return { success: false, message: '支付失败' };
  }

  return { success: false, message: '未知回调状态' };
}

module.exports = {
  createOrder,
  getOrderById,
  getOrdersByUserId,
  getAllOrders,
  simulatePayment,
  paymentCallback
};
