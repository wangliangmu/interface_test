Component({
  properties: {
    show: {
      type: Boolean,
      value: false
    },
    file: {
      type: Object,
      value: {}
    },
    loading: {
      type: Boolean,
      value: false
    }
  },

  data: {
    priceText: ''
  },

  observers: {
    'file': function (file) {
      if (!file) return
      var price = file.price === 0 ? '免费' : '¥' + (file.price || 0).toFixed(2)
      this.setData({ priceText: price })
    }
  },

  methods: {
    onMaskTap: function () {
      if (this.data.loading) return
      this.triggerEvent('close')
    },

    onCancel: function () {
      if (this.data.loading) return
      this.triggerEvent('close')
    },

    onConfirm: function () {
      if (this.data.loading) return
      this.triggerEvent('confirm', { file: this.properties.file })
    },

    preventBubble: function () {}
  }
})
