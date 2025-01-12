from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])

def generated_pswd_hash(password: str) -> str:
    hash =  password_context.hash(password) # returns the hashed password
    return hash

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password) # returns True if the password matches the hash
