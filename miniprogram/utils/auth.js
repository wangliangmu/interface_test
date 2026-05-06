var app = getApp()

function login() {
  return app.login()
}

function logout() {
  app.globalData.token = null
  app.globalData.userInfo = null
  wx.removeStorageSync('token')
  wx.removeStorageSync('userInfo')
  wx.removeStorageSync('isAdmin')
}

function isLoggedIn() {
  var token = app.globalData.token || wx.getStorageSync('token')
  return !!token
}

function getToken() {
  return app.globalData.token || wx.getStorageSync('token')
}

function getUserInfo() {
  return app.globalData.userInfo || wx.getStorageSync('userInfo')
}

function isAdmin() {
  var userInfo = getUserInfo()
  return userInfo && userInfo.role === 'admin'
}

function checkLogin() {
  return new Promise(function (resolve, reject) {
    if (isLoggedIn()) {
      resolve(getToken())
    } else {
      login().then(function (data) {
        resolve(data.token)
      }).catch(function (err) {
        reject(err)
      })
    }
  })
}

module.exports = {
  login: login,
  logout: logout,
  isLoggedIn: isLoggedIn,
  getToken: getToken,
  getUserInfo: getUserInfo,
  isAdmin: isAdmin,
  checkLogin: checkLogin
}
