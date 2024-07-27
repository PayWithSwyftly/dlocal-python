import hashlib
import hmac

def generate_hmac_sha256_signature(payload: str, secret_key: str):
    key_bytes = bytes(secret_key, 'utf-8')
    payload_bytes = bytes(payload, 'utf-8')

    return hmac.new(key_bytes, payload_bytes, hashlib.sha256).hexdigest()
