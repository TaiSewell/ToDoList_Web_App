"""
***********************************************
Developer: Tai Sewell

File: users.py

Description: File that contains all user related
endpoints/routes.
***********************************************
"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..app.hashing import hash_password
from ..app.auth import get_current_user
from ..app.database import get_db
from ..app.models import User

router = APIRouter()

@router.post("/login")
async def login_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    password = user_data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


"""
***********************************************
Method: create_user()


Description: This method is used to create a user
in the database.

returns: The created user object.
***********************************************
"""
@tdlapp.post("/users/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    password = user_data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""
***********************************************
Method: read_users()

Description: This method is used to fetch all 
users.

returns: A list of users.
***********************************************
"""
@tdlapp.get("/users/")
def read_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return users

"""
***********************************************
Method: read_user()


Description: This method is used to retrieve a user
based on the user_id from the database.

returns: A user object.
***********************************************
"""
@tdlapp.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

"""
***********************************************
Method: delete_user()

Description: This method is used to delete a 
user from the database by their ID.

returns: A message indicating the result.
***********************************************
"""
@tdlapp.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    user_count = db.query(models.User).count()
    if user_count == 0:
        db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1"))
        db.commit()
    
    return {"detail": "User deleted"}


"""
***********************************************
Method: update_user()

Description: This method is used to update a 
user's information.

returns: The updated user details.
***********************************************
"""
@tdlapp.put("/users/{user_id}")
async def update_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    hashed_password = user_data.get("hashed_password")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username:
        user.username = username
    if hashed_password:
        user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)
    return user
