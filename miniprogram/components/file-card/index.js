var util = require('../../utils/util.js')

Component({
  properties: {
    file: {
      type: Object,
      value: {}
    }
  },

  data: {
    fileType: '',
    fileIcon: '',
    typeLabel: '',
    priceText: '',
    sizeText: '',
    isPurchased: false
  },

  observers: {
    'file': function (file) {
      if (!file) return
      var ext = util.getFileType(file.filename || file.title || '')
      var icon = util.getFileIcon(ext)
      var label = util.getFileTypeLabel(ext)
      var price = file.price === 0 ? '免费' : '¥' + util.formatPrice(file.price)
      var size = util.formatFileSize(file.size || 0)
      this.setData({
        fileType: ext,
        fileIcon: icon,
        typeLabel: label,
        priceText: price,
        sizeText: size,
        isPurchased: !!file.isPurchased
      })
    }
  },

  methods: {
    onTap: function () {
      var file = this.properties.file
      if (file && file._id) {
        wx.navigateTo({
          url: '/pages/detail/index?id=' + file._id
        })
      }
      this.triggerEvent('tap', { file: file })
    }
  }
})
