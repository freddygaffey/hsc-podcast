-- Schema for hsc-podcast-private-audio.
-- Applies to the SAME D1 database as auth-worker (hsc-podcast-auth).

-- Single-row PIN record. The PIN itself is never stored: only PBKDF2(pin, salt).
CREATE TABLE IF NOT EXISTS pin_auth (
  id        INTEGER PRIMARY KEY CHECK (id = 1),
  pin_hash  TEXT NOT NULL,
  salt      TEXT NOT NULL,
  created   INTEGER NOT NULL
);

-- Failed PIN attempts. A 4-digit PIN is only 10,000 possibilities, so this table is
-- what actually secures it — the Worker counts rows here before checking the PIN.
CREATE TABLE IF NOT EXISTS pin_attempts (
  id  INTEGER PRIMARY KEY AUTOINCREMENT,
  ip  TEXT NOT NULL,
  ts  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_pin_attempts_ip_ts ON pin_attempts (ip, ts);
CREATE INDEX IF NOT EXISTS idx_pin_attempts_ts    ON pin_attempts (ts);
