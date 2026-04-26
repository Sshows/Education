import hashlib
import hmac
import json
from urllib.parse import parse_qsl


def parse_telegram_init_data(init_data: str) -> dict[str, str]:
    return dict(parse_qsl(init_data, keep_blank_values=True))


def build_data_check_string(pairs: dict[str, str]) -> str:
    clean_pairs = {key: value for key, value in pairs.items() if key != "hash"}
    return "\n".join(f"{key}={value}" for key, value in sorted(clean_pairs.items()))


def validate_telegram_init_data(init_data: str, bot_token: str) -> bool:
    if not init_data or not bot_token:
        return False

    pairs = parse_telegram_init_data(init_data)
    hash_value = pairs.get("hash")
    if not hash_value:
        return False

    data_check_string = build_data_check_string(pairs)
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    signature = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, hash_value)


def parse_telegram_user(init_data: str) -> dict:
    pairs = parse_telegram_init_data(init_data)
    raw_user = pairs.get("user")
    if not raw_user:
        return {}
    try:
        user = json.loads(raw_user)
    except json.JSONDecodeError:
        return {}
    return user if isinstance(user, dict) else {}
