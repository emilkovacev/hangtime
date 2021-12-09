import base64
import hashlib


def generate_key(key: str) -> str:
    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    hashed_key: bytes = hashlib.sha1(key.encode() + GUID.encode()).digest()
    encoded_key = base64.b64encode(hashed_key)
    return encoded_key.decode()

