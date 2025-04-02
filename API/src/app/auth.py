"""
***********************************************
Developer: Tai Sewell

File: auth.py

Description: This file contains the JWT authentication
logic.
***********************************************
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .hashing import verify_password
from .database import get_db
from .models import User
import os

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
***********************************************
Method: get_current_user()

Args: token(str) - The JWT token to be verified.

Description: This file verifies the JWT token and retrieves the
current user.
***********************************************
"""
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
***********************************************
Method: get_current_user()

Args: token(str) - The JWT token to be verified.
      db(Session) - The database session.

Description: This file verifies the JWT token and retrieves the
current user.
***********************************************
"""
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



