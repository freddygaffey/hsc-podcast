#!/usr/bin/env python3
"""Encrypt set-text study content so a casual visitor can't read it.

Build step for deploy.sh. Takes the plaintext JSON under a text folder and writes
`<name>.json.enc` next to it in dist/, plus a `gate.json` holding the public salt and
KDF parameters so the browser can derive the same key.

    python3 tools/encrypt_content.py --passphrase SECRET \
        --src content/english-standard/past-the-shallows \
        --out dist/content/english-standard/past-the-shallows

Crypto matches auth.js so the browser can mirror it with WebCrypto:
    key = PBKDF2-HMAC-SHA256(passphrase, salt, 150_000) -> 32 bytes -> AES-256-GCM
    payload = iv(12) || ciphertext || tag(16), base64

THIS IS OBFUSCATION, NOT SECURITY. The ciphertext is public and the passphrase is
short and shared; anyone who learns it can decrypt everything. It exists to stop a
passer-by reading personal study notes, nothing more. Do not put anything genuinely
sensitive behind it.
"""
import argparse, base64, hashlib, json, os, secrets, sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit("ERROR: pip install cryptography")

ITERATIONS = 150_000
FILES = ["scenes.json", "quotes.json", "quiz.json"]


def derive(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, ITERATIONS, dklen=32)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--passphrase", required=True, help="the unlock phrase (e.g. your username)")
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--salt", help="hex salt to reuse; omit to generate a fresh one")
    args = ap.parse_args()

    if not args.src.is_dir():
        sys.exit(f"ERROR: no such folder: {args.src}")

    salt = bytes.fromhex(args.salt) if args.salt else secrets.token_bytes(16)
    key = derive(args.passphrase, salt)
    aes = AESGCM(key)
    args.out.mkdir(parents=True, exist_ok=True)

    written = []
    for name in FILES:
        p = args.src / name
        if not p.exists():
            continue
        plaintext = p.read_bytes()
        iv = secrets.token_bytes(12)
        blob = iv + aes.encrypt(iv, plaintext, None)
        dest = args.out / (name + ".enc")
        dest.write_text(base64.b64encode(blob).decode("ascii"))
        written.append((name, len(plaintext), dest))
        # Never let the plaintext ship alongside the ciphertext.
        stale = args.out / name
        if stale.exists():
            stale.unlink()

    (args.out / "gate.json").write_text(json.dumps({
        "kdf": "PBKDF2-HMAC-SHA256",
        "iterations": ITERATIONS,
        "salt": base64.b64encode(salt).decode("ascii"),
        "cipher": "AES-256-GCM",
        "layout": "base64(iv[12] || ciphertext || tag[16])",
        "files": [n + ".enc" for n, _, _ in written],
        "note": "Obfuscation only - the ciphertext is public and the passphrase is shared.",
    }, indent=1))

    for name, size, dest in written:
        print(f"  {name:14s} {size:7d} B -> {dest}")
    print(f"  salt (hex, reuse with --salt): {salt.hex()}")
    if not written:
        print("  WARNING: nothing encrypted - no matching files found", file=sys.stderr)


if __name__ == "__main__":
    main()
