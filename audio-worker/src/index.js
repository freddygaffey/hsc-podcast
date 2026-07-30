// hsc-podcast-private-audio — PIN-authenticated streaming from a PRIVATE R2 bucket.
//
// The rest of the app is public. This Worker guards one thing: a personal
// accessible-format copy of a purchased book, which must stay readable by one account
// only. The public bucket (audio.hsc.pebnum.com) is world-readable by design, so that
// file cannot live there.
//
// Flow:
//   POST /session  {pin}          -> { token, exp }   (rate limited, see below)
//   GET  /<key>    Bearer <token> -> 200 / 206 with Range support
//
// Why a session token rather than sending the PIN each time: seeking an audiobook issues
// many Range requests. Replaying a 4-digit PIN on every one of them would make brute
// force trivial to hide inside normal traffic and would put the secret in far more
// places. The PIN is exchanged once for a short-lived HMAC token.
//
// SECURITY NOTE, PLAINLY: a 4-digit PIN is 10,000 possibilities. Rate limiting is the
// only thing making it viable — without it a script cracks this in seconds. Limits below
// are deliberately strict: 5 attempts per 15 minutes per IP, 20 per hour globally, then
// exponential lockout. Do not raise them.

const ENC = new TextEncoder();

const MAX_PER_IP = 5;              // failures per IP per window
const IP_WINDOW_S = 15 * 60;
const MAX_GLOBAL = 20;             // failures across all IPs per hour (blocks distributed guessing)
const GLOBAL_WINDOW_S = 60 * 60;
const TOKEN_TTL_S = 10 * 365 * 24 * 60 * 60;  // effectively permanent: this is a personal
                                   // study app, and re-entering a PIN mid-run is the real cost.
                                   // Kill switch: rotate SESSION_SECRET to invalidate every token.
const PIN_ITERATIONS = 100000;     // Workers cap PBKDF2 at 100k; rate limiting is the real defence

const ALLOWED_ORIGINS = new Set([
  "https://hsc.pebnum.com",
  "https://hsc-podcast-unified.pages.dev",
  "http://localhost:8765",
]);

function cors(origin) {
  return {
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS.has(origin) ? origin : "",
    "Access-Control-Allow-Methods": "GET, HEAD, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type, Range",
    "Access-Control-Expose-Headers": "Content-Length, Content-Range, Accept-Ranges",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}
const json = (data, status, headers) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { ...headers, "Content-Type": "application/json", "Cache-Control": "no-store" },
  });

const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

function safeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function hashPin(pin, salt) {
  const key = await crypto.subtle.importKey("raw", ENC.encode(pin), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt: ENC.encode(salt), iterations: PIN_ITERATIONS, hash: "SHA-256" },
    key, 256);
  return hex(bits);
}

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey("raw", ENC.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, ENC.encode(msg)));
}

async function issueToken(env) {
  const exp = Math.floor(Date.now() / 1000) + TOKEN_TTL_S;
  const nonce = hex(crypto.getRandomValues(new Uint8Array(8)));
  const body = `${exp}.${nonce}`;
  return { token: `${body}.${await hmac(env.SESSION_SECRET, body)}`, exp };
}

async function verifyToken(env, token) {
  const parts = String(token || "").split(".");
  if (parts.length !== 3) return false;
  const [exp, nonce, sig] = parts;
  if (!/^\d+$/.test(exp) || Number(exp) < Math.floor(Date.now() / 1000)) return false;
  return safeEqual(sig, await hmac(env.SESSION_SECRET, `${exp}.${nonce}`));
}

/* ---------- rate limiting (D1) ---------- */

async function recentFailures(env, ip) {
  const now = Math.floor(Date.now() / 1000);
  const perIp = await env.DB.prepare(
    "SELECT COUNT(*) AS n FROM pin_attempts WHERE ip=? AND ts > ?")
    .bind(ip, now - IP_WINDOW_S).first();
  const global = await env.DB.prepare(
    "SELECT COUNT(*) AS n FROM pin_attempts WHERE ts > ?")
    .bind(now - GLOBAL_WINDOW_S).first();
  return { ip: perIp?.n || 0, global: global?.n || 0 };
}

async function recordFailure(env, ip) {
  await env.DB.prepare("INSERT INTO pin_attempts (ip, ts) VALUES (?, ?)")
    .bind(ip, Math.floor(Date.now() / 1000)).run();
}

async function clearFailures(env, ip) {
  await env.DB.prepare("DELETE FROM pin_attempts WHERE ip=?").bind(ip).run();
}

/* ---------- object keys ---------- */

function keyFor(path) {
  const clean = decodeURIComponent(path).replace(/^\/+/, "").replace(/\.\.+/g, "");
  return clean && !clean.includes("\0") ? clean : null;
}

function parseRange(header, size) {
  const m = /^bytes=(\d*)-(\d*)$/.exec((header || "").trim());
  if (!m) return null;
  const [, s, e] = m;
  if (s === "" && e === "") return null;
  let start, end;
  if (s === "") {
    const n = parseInt(e, 10);
    if (!n) return null;
    start = Math.max(0, size - n); end = size - 1;
  } else {
    start = parseInt(s, 10);
    end = e === "" ? size - 1 : parseInt(e, 10);
  }
  if (!isFinite(start) || !isFinite(end) || start > end || start >= size) return null;
  return { start, end: Math.min(end, size - 1) };
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const headers = cors(origin);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers });

    const url = new URL(req.url);
    const ip = req.headers.get("CF-Connecting-IP") || "0.0.0.0";

    // --- exchange PIN for a session token ---
    if (req.method === "POST" && url.pathname === "/session") {
     try {
      const fails = await recentFailures(env, ip);
      if (fails.ip >= MAX_PER_IP || fails.global >= MAX_GLOBAL) {
        // Exponential backoff past the threshold, capped at the window.
        const over = Math.max(fails.ip - MAX_PER_IP, fails.global - MAX_GLOBAL) + 1;
        const retry = Math.min(IP_WINDOW_S, 30 * Math.pow(2, over));
        return json({ error: "too many attempts" }, 429,
          { ...headers, "Retry-After": String(retry) });
      }

      let pin = "";
      try { pin = String((await req.json()).pin || ""); } catch { /* falls through */ }
      if (!/^\d{4}$/.test(pin)) {
        await recordFailure(env, ip);
        return json({ error: "invalid pin" }, 401, headers);
      }

      const row = await env.DB.prepare("SELECT pin_hash, salt FROM pin_auth WHERE id=1").first();
      if (!row) return json({ error: "not provisioned" }, 500, headers);

      if (!safeEqual(await hashPin(pin, row.salt), row.pin_hash)) {
        await recordFailure(env, ip);
        const left = Math.max(0, MAX_PER_IP - (fails.ip + 1));
        return json({ error: "invalid pin", attemptsRemaining: left }, 401, headers);
      }

      await clearFailures(env, ip);
      return json(await issueToken(env), 200, headers);
     } catch (err) {
       return json({ error: "session failed", detail: String(err && err.message || err) }, 500, headers);
     }
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
      return new Response("method not allowed", { status: 405, headers });
    }

    // --- stream, session token required ---
    // <audio> cannot set an Authorization header, so a short-lived token may also be
    // passed as ?t=. Same signature and expiry; it just rides in the URL instead. That
    // is a real tradeoff (URLs leak into history and logs) accepted so the player can
    // stream and seek natively rather than buffering the whole file into memory.
    const auth = req.headers.get("Authorization") || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : (url.searchParams.get("t") || "");
    if (!(await verifyToken(env, token))) {
      return json({ error: "unauthorized" }, 401,
        { ...headers, "WWW-Authenticate": "Bearer" });
    }

    const key = keyFor(url.pathname);
    if (!key) return new Response("not found", { status: 404, headers });

    const head = await env.AUDIO.head(key);
    if (!head) return new Response("not found", { status: 404, headers });

    const size = head.size;
    const common = {
      ...headers,
      "Accept-Ranges": "bytes",
      "Content-Type": head.httpMetadata?.contentType || "audio/mp4",
      "Cache-Control": "private, no-store",   // never let a shared cache hold this
      ETag: head.httpEtag,
    };

    if (req.method === "HEAD") {
      return new Response(null, { status: 200, headers: { ...common, "Content-Length": String(size) } });
    }

    const rangeHeader = req.headers.get("Range");
    const range = parseRange(rangeHeader, size);
    if (rangeHeader && !range) {
      return new Response("range not satisfiable", {
        status: 416, headers: { ...common, "Content-Range": `bytes */${size}` },
      });
    }

    if (range) {
      const obj = await env.AUDIO.get(key, {
        range: { offset: range.start, length: range.end - range.start + 1 },
      });
      if (!obj) return new Response("not found", { status: 404, headers });
      return new Response(obj.body, {
        status: 206,
        headers: {
          ...common,
          "Content-Range": `bytes ${range.start}-${range.end}/${size}`,
          "Content-Length": String(range.end - range.start + 1),
        },
      });
    }

    const obj = await env.AUDIO.get(key);
    if (!obj) return new Response("not found", { status: 404, headers });
    return new Response(obj.body, {
      status: 200, headers: { ...common, "Content-Length": String(size) },
    });
  },
};
