"""
***********************************************
Developer: Tai Sewell

File: hashing.py

Description: File that holds all the password
hashing utilities.
***********************************************
"""
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
***********************************************
Method: hash_password()

args: password(str) - The password to be hashed.

Description: This method hashes the password
that is passed into it.
***********************************************
"""
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

"""
***********************************************
Method: verify_password()

args: plai_password(str) - The password to be verified.
      hashed_password(str) - The hashed password.

Description: This method hashes the password
that is passed into it.
***********************************************
"""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
