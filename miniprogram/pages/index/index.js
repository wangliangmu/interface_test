var request = require('../../utils/request.js')
var auth = require('../../utils/auth.js')

Page({
  data: {
    files: [],
    keyword: '',
    typeFilter: 'all',
    filters: [
      { key: 'all', label: '全部' },
      { key: 'pdf', label: 'PDF' },
      { key: 'docx', label: 'DOCX' }
    ],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false,
    refreshing: false,
    isEmpty: false
  },

  onLoad: function () {
    this.loadFiles()
  },

  onShow: function () {
    if (this.data.files.length > 0) {
      this.setData({ page: 1, hasMore: true })
      this.loadFiles(true)
    }
  },

  onPullDownRefresh: function () {
    this.setData({ page: 1, hasMore: true, refreshing: true })
    this.loadFiles(true)
  },

  onReachBottom: function () {
    if (this.data.hasMore && !this.data.loading) {
      this.loadFiles()
    }
  },

  loadFiles: function (reset) {
    var that = this
    if (this.data.loading) return

    var page = reset ? 1 : this.data.page
    this.setData({ loading: true })

    var params = {
      page: page,
      pageSize: this.data.pageSize
    }
    if (this.data.keyword) {
      params.keyword = this.data.keyword
    }
    if (this.data.typeFilter !== 'all') {
      params.type = this.data.typeFilter
    }

    request.get('/files', params).then(function (res) {
      var list = res.data && res.data.list ? res.data.list : []
      var total = res.data && res.data.total ? res.data.total : 0
      var files = reset ? list : that.data.files.concat(list)
      var hasMore = files.length < total

      that.setData({
        files: files,
        page: page + 1,
        hasMore: hasMore,
        loading: false,
        refreshing: false,
        isEmpty: files.length === 0
      })

      if (that.data.refreshing) {
        wx.stopPullDownRefresh()
      }
    }).catch(function () {
      that.setData({
        loading: false,
        refreshing: false
      })
      if (that.data.refreshing) {
        wx.stopPullDownRefresh()
      }
    })
  },

  onSearchInput: function (e) {
    this.setData({ keyword: e.detail.value })
  },

  onSearch: function () {
    this.setData({ page: 1, hasMore: true })
    this.loadFiles(true)
  },

  onClearSearch: function () {
    this.setData({ keyword: '', page: 1, hasMore: true })
    this.loadFiles(true)
  },

  onFilterTap: function (e) {
    var key = e.currentTarget.dataset.key
    this.setData({ typeFilter: key, page: 1, hasMore: true })
    this.loadFiles(true)
  },

  onFileTap: function (e) {
    var file = e.detail.file
    if (file && file._id) {
      wx.navigateTo({
        url: '/pages/detail/index?id=' + file._id
      })
    }
  }
})
