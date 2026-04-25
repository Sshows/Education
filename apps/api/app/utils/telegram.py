import hashlib
import hmac
from urllib.parse import parse_qsl


def validate_telegram_init_data(init_data: str, bot_token: str) -> bool:
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_value = pairs.pop("hash", None)
    if not hash_value:
        return False
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    signature = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, hash_value)
