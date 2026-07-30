# hsc-podcast-private-audio

Authenticated streaming from a **private** R2 bucket.

## Why this exists

The normal audio origin (`audio.hsc.pebnum.com`) is a **public** bucket: anyone with the
URL can fetch anything in it, with no auth and no signature. That's fine for generated
episode audio.

It is **not** fine for a personal accessible-format copy of a book you own. That copy has
to stay private to one account — if it sits in the public bucket it is effectively
published, whatever the app's UI says. This Worker is the difference between "private"
and "unlisted".

Objects are namespaced by account (`<username>/...`), so a session can only ever read its
own uploads.

## What it does

- Requires `X-Username` + `Authorization: Bearer <authToken>` — the same scheme
  `auth-worker/` already uses. The password never reaches the server; only
  `SHA-256(authToken)` is compared against the stored row in the shared D1 database.
- Serves `HEAD`, full `GET`, and **`Range` requests** (206 + `Content-Range`).
  Range support is required, not optional: without it `<audio>` cannot seek, and the plot
  map's jump-to-scene does nothing.
- Sends `Cache-Control: private, no-store` so no shared cache retains the bytes.
- Returns 401 on bad auth, 404 on unknown key, 416 on an unsatisfiable range.

## Setup

Run these yourself — nothing here is automated.

```sh
cd audio-worker

# 1. Create the private bucket. Do NOT attach a custom domain or enable r2.dev access;
#    that would defeat the point.
wrangler r2 bucket create hsc-podcast-private

# 2. Point wrangler.toml at the existing auth database.
wrangler d1 list                      # copy the hsc-podcast-auth id
$EDITOR wrangler.toml                 # paste into database_id

# 3. Deploy.
wrangler deploy
```

Verify it actually refuses anonymous reads before you trust it:

```sh
curl -si https://<worker-url>/past-the-shallows/book.m4a | head -1     # expect 401
curl -si -H 'X-Username: you' -H 'Authorization: Bearer <token>' \
     -H 'Range: bytes=0-1023' https://<worker-url>/past-the-shallows/book.m4a | head -3
                                                                        # expect 206
```

## Uploading your own file

```sh
wrangler r2 object put hsc-podcast-private/<username>/past-the-shallows/book.m4a \
  --file /path/to/your-file.m4a --content-type audio/mp4
```

The key must start with your username or the Worker will not serve it to you.

## Limits — read these

- **Anyone who learns your password can stream the file.** Auth is one shared secret, not
  per-device keys. Use a real password here, not your username.
- The Worker authenticates; it does not watermark, rate-limit, or expire sessions.
- This protects a personal accessible-format copy from being publicly readable. It is not
  a licence to share the file, and putting the same object in the public bucket would
  undo all of it.
