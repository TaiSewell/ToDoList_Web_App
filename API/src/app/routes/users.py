"""
***********************************************
Developer: Tai Sewell

File: users.py

Description: File that contains user-related endpoints.
***********************************************
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from Database.src import database, models
from ..auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

# Create a router
router = APIRouter()

# Import get_db function
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
***********************************************
           All User Endpoints/Methods
***********************************************

***********************************************
Method: create_user()


Description: This method is used to create a user
in the database.

returns: The created user object.
***********************************************
"""
@router.post("/users/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    password = user_data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    # Check if the username already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and create the user
    hashed_password = hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

      # Generate a JWT token for the new user
    access_token = create_access_token(data={"sub": new_user.username})

    return {
        "id": new_user.id,
        "username": new_user.username,
        "access_token": access_token,
        "token_type": "bearer",
    }

"""
***********************************************
Method: login_for_access_token()

Description: This method is used to authenticate 
an existing user by verifying their credentials 
(username and password). If the credentials are 
valid, it generates and returns a JWT access token.

returns: A dictionary containing the access token 
and token type.
***********************************************
"""
@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Check if the user exists
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create a JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

"""
***********************************************
Method: read_user()


Description: This method is used to retrieve a users
personal profile.

returns: A user object.
***********************************************
"""
@router.get("/users/me")
def read_user_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        # Add any other fields you want to expose
    }

"""
***********************************************
Method: update_user()

Description: This method is used to update a 
user's information.

returns: The updated user details.
***********************************************
"""
# 4. Update a User
@router.put("/users/{user_id}")
async def update_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    password = user_data.get("password")  # Accept plain password for hashing

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username:
        user.username = username
    if password:
        user.hashed_password = hash_password(password)  # Hash the new password

    db.commit()
    db.refresh(user)
    return user

"""
***********************************************
Method: delete_user()

Description: This method is used to delete a 
user from the database by their ID.

returns: A message indicating the result.
***********************************************
"""
@router.delete("/users/me")
def delete_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Fetch the current user from the database
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    db.delete(user)
    db.commit()

    return {"detail": "Your account has been deleted"}
