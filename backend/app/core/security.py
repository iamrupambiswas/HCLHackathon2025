from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from app.core.config import settings
from typing import Optional
from fastapi import HTTPException, status

# Initialize CryptContext with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Validate password length before hashing
    if not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password cannot be empty")
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password too long (max 72 bytes)")
    return pwd_context.hash(password_bytes[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Encode and truncate for verification
    return pwd_context.verify(plain_password.encode("utf-8")[:72], hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decode JWT token and return the payload.
    Raises HTTPException on invalid token.
    """
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )