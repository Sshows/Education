from __future__ import annotations

import hashlib
import hmac
import json


def canonical_json(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hmac_sha256(payload: dict | str, secret: str) -> str:
    body = canonical_json(payload) if isinstance(payload, dict) else payload
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


def verify_hmac_sha256(payload: dict | str, signature: str | None, secret: str) -> bool:
    if not signature or not secret:
        return False
    return hmac.compare_digest(hmac_sha256(payload, secret), signature)
