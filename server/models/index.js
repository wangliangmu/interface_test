const Database = require('better-sqlite3');
const path = require('path');
const config = require('../config');

const dbPath = path.resolve(config.database.path);
const db = new Database(dbPath);

db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

function initTables() {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      openid TEXT UNIQUE,
      nickname TEXT,
      avatar_url TEXT,
      is_admin INTEGER DEFAULT 0,
      phone TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      file_type TEXT CHECK(file_type IN ('pdf', 'docx')),
      file_path TEXT NOT NULL,
      file_size INTEGER,
      preview_pages INTEGER DEFAULT 3,
      total_pages INTEGER,
      price REAL,
      cover_image TEXT,
      download_count INTEGER DEFAULT 0,
      view_count INTEGER DEFAULT 0,
      status INTEGER DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      order_no TEXT UNIQUE NOT NULL,
      user_id INTEGER NOT NULL,
      file_id INTEGER NOT NULL,
      amount REAL,
      status TEXT CHECK(status IN ('pending', 'paid', 'refunded', 'cancelled')) DEFAULT 'pending',
      payment_method TEXT,
      transaction_id TEXT,
      paid_at DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS payments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      order_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      file_id INTEGER NOT NULL,
      amount REAL,
      payment_type TEXT,
      status TEXT CHECK(status IN ('success', 'failed', 'refunded')) DEFAULT 'success',
      transaction_id TEXT,
      raw_data TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (order_id) REFERENCES orders(id),
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS user_files (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      file_id INTEGER NOT NULL,
      order_id INTEGER,
      can_preview INTEGER DEFAULT 1,
      can_download INTEGER DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (file_id) REFERENCES files(id),
      FOREIGN KEY (order_id) REFERENCES orders(id)
    );
  `);
}

initTables();

module.exports = db;
