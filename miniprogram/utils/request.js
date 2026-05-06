var app = getApp()

function request(options) {
  var url = app.globalData.baseUrl + options.url
  var method = options.method || 'GET'
  var data = options.data || {}
  var header = options.header || {}

  header['content-type'] = header['content-type'] || 'application/json'

  var token = app.globalData.token || wx.getStorageSync('token')
  if (token) {
    header['Authorization'] = 'Bearer ' + token
  }

  return new Promise(function (resolve, reject) {
    wx.request({
      url: url,
      method: method,
      data: data,
      header: header,
      success: function (res) {
        if (res.statusCode === 401) {
          handleAuthExpired()
          reject({ code: 401, message: '登录已过期，请重新登录' })
          return
        }
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          var message = (res.data && res.data.message) || '请求失败'
          showToast(message)
          reject({ code: res.statusCode, message: message })
        }
      },
      fail: function (err) {
        showToast('网络异常，请稍后重试')
        reject({ code: -1, message: '网络异常' })
      }
    })
  })
}

function handleAuthExpired() {
  app.globalData.token = null
  app.globalData.userInfo = null
  wx.removeStorageSync('token')
  wx.removeStorageSync('userInfo')
  wx.showToast({
    title: '登录已过期',
    icon: 'none',
    duration: 2000
  })
  setTimeout(function () {
    app.login().catch(function () {})
  }, 1500)
}

function showToast(message) {
  wx.showToast({
    title: message,
    icon: 'none',
    duration: 2000
  })
}

function get(url, data) {
  return request({ url: url, method: 'GET', data: data })
}

function post(url, data) {
  return request({ url: url, method: 'POST', data: data })
}

function put(url, data) {
  return request({ url: url, method: 'PUT', data: data })
}

function del(url, data) {
  return request({ url: url, method: 'DELETE', data: data })
}

module.exports = {
  request: request,
  get: get,
  post: post,
  put: put,
  del: del
}
