from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from Database.src import database, models

# Load environment variables from .env file
load_dotenv()

# Import get_db function
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Secret key for signing JWTs (use a secure key in production)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set in the environment variables")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
***********************************************
Method: hash_password()

Description: This method is used to hash a plain 
password using the bcrypt hashing algorithm. The 
hashed password is stored securely in the database.

Parameters:
- password (str): The plain text password to be hashed.

returns: A hashed version of the password.
***********************************************
"""
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


"""
***********************************************
Method: verify_password()

Description: This method is used to verify if a 
plain text password matches its hashed counterpart.

Parameters:
- plain_password (str): The plain text password provided by the user.
- hashed_password (str): The hashed password stored in the database.

returns: A boolean indicating whether the passwords match.
***********************************************
"""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""
***********************************************
Method: create_access_token()

Description: This method is used to create a JWT 
access token for an authenticated user. The token 
contains user-specific data (e.g., username) and 
an expiration time.

Parameters:
- data (dict): The payload data to include in the token (e.g., {"sub": username}).
- expires_delta (Optional[timedelta]): The duration for which the token is valid. 
  If not provided, the default expiration time is used.

returns: A JWT access token as a string.
***********************************************
"""
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

"""
***********************************************
Method: decode_access_token()

Description: This method is used to decode and 
verify a JWT access token. It ensures the token 
is valid and has not expired.

Parameters:
- token (str): The JWT token to decode and verify.

returns: The decoded payload of the token if valid.

raises: 
- HTTPException (401): If the token is invalid or expired.
***********************************************
"""
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""
***********************************************
Method: get_current_user()

Description: This method is a dependency used to 
retrieve the currently authenticated user based 
on the provided JWT token. It validates the token 
and fetches the user from the database.

Parameters:
- token (str): The JWT token provided in the 
  Authorization header (automatically extracted 
  by FastAPI's dependency injection).
- db (Session): The database session used to query 
  the user.

returns: The user object corresponding to the token.

raises:
- HTTPException (401): If the token is invalid or expired.
- HTTPException (404): If the user is not found in the database.
***********************************************
"""
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user