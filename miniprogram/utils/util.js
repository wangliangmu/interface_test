function formatTime(date) {
  if (!date) return ''
  var d = new Date(date)
  var year = d.getFullYear()
  var month = padZero(d.getMonth() + 1)
  var day = padZero(d.getDate())
  var hour = padZero(d.getHours())
  var minute = padZero(d.getMinutes())
  var second = padZero(d.getSeconds())
  return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
}

function formatDate(date) {
  if (!date) return ''
  var d = new Date(date)
  var year = d.getFullYear()
  var month = padZero(d.getMonth() + 1)
  var day = padZero(d.getDate())
  return year + '-' + month + '-' + day
}

function padZero(num) {
  return num < 10 ? '0' + num : '' + num
}

function formatPrice(price) {
  if (price === undefined || price === null) return '0.00'
  var num = parseFloat(price)
  if (isNaN(num)) return '0.00'
  return num.toFixed(2)
}

function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B'
  var units = ['B', 'KB', 'MB', 'GB', 'TB']
  var k = 1024
  var i = Math.floor(Math.log(bytes) / Math.log(k))
  var size = bytes / Math.pow(k, i)
  return size.toFixed(2) + ' ' + units[i]
}

function getFileType(filename) {
  if (!filename) return ''
  var ext = filename.split('.').pop().toLowerCase()
  return ext
}

function getFileIcon(type) {
  var icons = {
    pdf: '📄',
    doc: '📝',
    docx: '📝',
    xls: '📊',
    xlsx: '📊',
    ppt: '📑',
    pptx: '📑',
    txt: '📃',
    png: '🖼️',
    jpg: '🖼️',
    jpeg: '🖼️'
  }
  return icons[type] || '📁'
}

function getFileTypeLabel(type) {
  var labels = {
    pdf: 'PDF',
    doc: 'DOC',
    docx: 'DOCX',
    xls: 'XLS',
    xlsx: 'XLSX',
    ppt: 'PPT',
    pptx: 'PPTX',
    txt: 'TXT',
    png: 'PNG',
    jpg: 'JPG',
    jpeg: 'JPEG'
  }
  return labels[type] || type.toUpperCase()
}

module.exports = {
  formatTime: formatTime,
  formatDate: formatDate,
  formatPrice: formatPrice,
  formatFileSize: formatFileSize,
  getFileType: getFileType,
  getFileIcon: getFileIcon,
  getFileTypeLabel: getFileTypeLabel
}
