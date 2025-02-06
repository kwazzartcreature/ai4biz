import datetime
import bcrypt
import jwt

from lib import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    ExpiredTokenException,
    InvalidTokenException,
)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def compare_passwords(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_token(data: dict, expires: int = JWT_EXPIRE_MINUTES) -> str:
    payload = data.copy()
    payload.update(
        {"exp": datetime.datetime.now() + datetime.timedelta(minutes=expires)}
    )
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
