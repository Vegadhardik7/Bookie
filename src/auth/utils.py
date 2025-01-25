import jwt
import uuid
import logging
from src.config import Config
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

def generated_pswd_hash(password: str) -> str:
    print(f"********generated password before hash : {password}*******")
    hash =  password_context.hash(password) # returns the hashed password
    print(f"********generated password after hash : {hash}*******")
    return hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(f"*****Plain Password: {plain_password}*****")
    print(f"*****Hashed Password: {plain_password}*****")
    return password_context.verify(plain_password, hashed_password) # returns True if the password matches the hash

def create_access_token(user_data: dict, expiry: Optional[timedelta] = None, refresh: bool = False) -> str:
    payload = {}
    payload['user'] = user_data
    expiry_time = str(datetime.now() + (expiry if expiry else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)))
    payload['expire'] = expiry_time
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    encoded_jwt = jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(jwt = token, key = Config.JWT_SECRET, algorithms = [Config.JWT_ALGORITHM])
        return token_data 
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")
        return {}