import hashlib
import jwt

SECRET = 'AxbQPRC95NT20VfJ4T6xjfSCDfbNvJJ4WOnyBu95'


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(email):
    encoded = jwt.encode({"email": email}, SECRET, algorithm='HS256').decode("utf-8")
    return encoded


def decode_token(encoded_token):
    return jwt.decode(encoded_token, SECRET, algorithms=['HS256'])

