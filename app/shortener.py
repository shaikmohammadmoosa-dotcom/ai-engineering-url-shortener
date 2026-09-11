import hashlib
import string

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()
    return "".join(arr)


def generate_short_code(url: str, length: int = 7) -> str:
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex[:10], 16)
    short_code = encode_base62(hash_int)[:length]
    return short_code