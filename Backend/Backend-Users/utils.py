from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from model import UserInDb, TokenData
import os
from dotenv import load_dotenv
from database import fetch_one_user_by_username

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    username = username.lower()
    user: UserInDb = await fetch_one_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = await fetch_one_user_by_username(username=token_data.username)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(
    current_user: UserInDb = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
