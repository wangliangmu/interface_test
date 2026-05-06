App({
  globalData: {
    userInfo: null,
    token: null,
    baseUrl: 'http://localhost:3000/api'
  },

  onLaunch: function () {
    var token = wx.getStorageSync('token')
    if (token) {
      this.globalData.token = token
    }
    var userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.globalData.userInfo = userInfo
    }
  },

  login: function () {
    var that = this
    return new Promise(function (resolve, reject) {
      wx.login({
        success: function (res) {
          if (res.code) {
            wx.request({
              url: that.globalData.baseUrl + '/auth/login',
              method: 'POST',
              data: { code: res.code },
              success: function (response) {
                if (response.data && response.data.token) {
                  that.globalData.token = response.data.token
                  that.globalData.userInfo = response.data.user
                  wx.setStorageSync('token', response.data.token)
                  wx.setStorageSync('userInfo', response.data.user)
                  resolve(response.data)
                } else {
                  reject(new Error('登录失败'))
                }
              },
              fail: function (err) {
                reject(err)
              }
            })
          } else {
            reject(new Error('wx.login 失败'))
          }
        },
        fail: function (err) {
          reject(err)
        }
      })
    })
  }
})
