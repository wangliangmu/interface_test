function success(data, message) {
  return {
    code: 0,
    message: message || 'success',
    data: data || null
  };
}

function error(message, code) {
  return {
    code: code || -1,
    message: message || 'error',
    data: null
  };
}

function paginate(list, total, page, pageSize) {
  return {
    list,
    total,
    page: parseInt(page),
    pageSize: parseInt(pageSize),
    totalPages: Math.ceil(total / pageSize)
  };
}

module.exports = { success, error, paginate };
