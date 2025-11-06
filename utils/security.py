from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(hash_: str, password: str) -> bool:
    return bcrypt.verify(password, hash_)
