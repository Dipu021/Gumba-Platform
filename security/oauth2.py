from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timezone,timedelta
from fastapi import Depends,HTTPException
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
# OAuth Setup

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Create Token

def create_token(date:dict):
    to_encode = date.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

# Verify Token
# def verify_token(token:str=Depends(oauth2_schema)):
#     try:
#         payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid Token"
#             )
#         return username
#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Token"
#         )

def verify_token(
    token: str = Depends(oauth2_schema)
):
    print("TOKEN RECEIVED:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD:", payload)

        username = payload.get("sub")

        print("USERNAME:", username)

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return username

    except JWTError as e:
        print("JWT ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )