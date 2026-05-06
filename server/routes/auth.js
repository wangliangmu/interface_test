const express = require('express');
const router = express.Router();
const https = require('https');
const config = require('../config');
const response = require('../utils/response');
const { authMiddleware } = require('../middleware/auth');
const userService = require('../services/userService');

function wxCode2Session(code) {
  return new Promise((resolve, reject) => {
    const url = `https://api.weixin.qq.com/sns/jscode2session?appid=${config.wx.appid}&secret=${config.wx.secret}&js_code=${code}&grant_type=authorization_code`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', (e) => {
      reject(e);
    });
  });
}

router.post('/wx-login', async (req, res) => {
  try {
    const { code, nickname, avatar_url } = req.body;
    if (!code) {
      return res.status(400).json(response.error('缺少code参数'));
    }

    let openid;
    try {
      const wxResult = await wxCode2Session(code);
      if (wxResult.errcode) {
        openid = `wx_dev_${code}`;
      } else {
        openid = wxResult.openid;
      }
    } catch (e) {
      openid = `wx_dev_${code}`;
    }

    if (!openid) {
      return res.status(400).json(response.error('微信登录失败'));
    }

    const user = userService.findOrCreateByOpenid(openid, { nickname, avatar_url });
    const token = userService.generateToken(user);

    res.json(response.success({
      token,
      user: {
        id: user.id,
        nickname: user.nickname,
        avatar_url: user.avatar_url,
        is_admin: user.is_admin
      }
    }));
  } catch (e) {
    res.status(500).json(response.error('登录失败: ' + e.message));
  }
});

router.post('/admin-login', (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json(response.error('用户名和密码不能为空'));
    }

    const admin = userService.adminLogin(username, password);
    if (!admin) {
      return res.status(401).json(response.error('用户名或密码错误'));
    }

    const token = userService.generateToken(admin);
    res.json(response.success({
      token,
      user: {
        id: admin.id,
        nickname: admin.nickname,
        is_admin: admin.is_admin
      }
    }));
  } catch (e) {
    res.status(500).json(response.error('登录失败: ' + e.message));
  }
});

router.get('/profile', authMiddleware, (req, res) => {
  try {
    const user = userService.getUserById(req.user.id);
    if (!user) {
      return res.status(404).json(response.error('用户不存在'));
    }
    res.json(response.success({
      id: user.id,
      openid: user.openid,
      nickname: user.nickname,
      avatar_url: user.avatar_url,
      is_admin: user.is_admin,
      phone: user.phone,
      created_at: user.created_at
    }));
  } catch (e) {
    res.status(500).json(response.error('获取用户信息失败: ' + e.message));
  }
});

module.exports = router;
