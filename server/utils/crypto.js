const CryptoJS = require('crypto-js');
const config = require('../config');

const KEY = config.crypto.key;

function encrypt(text) {
  return CryptoJS.AES.encrypt(text, KEY).toString();
}

function decrypt(ciphertext) {
  const bytes = CryptoJS.AES.decrypt(ciphertext, KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
}

module.exports = { encrypt, decrypt };
