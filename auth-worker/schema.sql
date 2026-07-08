-- hsc-podcast-auth — shared sync DB for the SE + Physics PWAs.
-- One account works across both subjects; progress is namespaced by `subject`.

CREATE TABLE IF NOT EXISTS users (
  username   TEXT PRIMARY KEY,        -- lowercase [a-z0-9_-], 3-40 chars
  salt       TEXT NOT NULL,           -- random, public; lets a new device derive keys
  auth_hash  TEXT NOT NULL,           -- SHA-256(authToken); server never sees the password or enc key
  created_at INTEGER NOT NULL
);

-- Append-only encrypted event log. The server stores opaque ciphertext only.
CREATE TABLE IF NOT EXISTS events (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  username   TEXT NOT NULL,
  subject    TEXT NOT NULL,           -- 'se' | 'phy'
  iv         TEXT NOT NULL,           -- base64 AES-GCM IV
  blob       TEXT NOT NULL,           -- base64 AES-GCM ciphertext (a progress delta)
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_user ON events (username, subject, id);

-- FEATURE-12: plaintext usage telemetry (Fred-readable analytics; NOT E2E-encrypted).
CREATE TABLE IF NOT EXISTS telemetry (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  ts         INTEGER NOT NULL,
  session    TEXT,                    -- random per-load id (not an account)
  event      TEXT NOT NULL,           -- e.g. 'subject_open','play','quiz_grade'
  props      TEXT,                    -- JSON blob of event details
  standalone INTEGER,                 -- 1 = installed PWA, 0 = browser tab
  origin     TEXT
);
CREATE INDEX IF NOT EXISTS idx_telemetry_event ON telemetry (event, ts);

-- FEATURE-13: free-text feedback (Fred-readable).
CREATE TABLE IF NOT EXISTS feedback (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ts       INTEGER NOT NULL,
  username TEXT,                      -- optional (if logged in)
  text     TEXT NOT NULL,
  origin   TEXT,
  ua       TEXT
);
