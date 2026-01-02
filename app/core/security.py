import hashlib, bcrypt, secrets


def _prehash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    prehashed = _prehash_password(password)
    pwd_bytes = prehashed.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = _prehash_password(plain_password)
    pwd_bytes = prehashed.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def generate_token() -> str:
    return secrets.token_hex(32)
