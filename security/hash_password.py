from passlib.context import CryptContext


# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)