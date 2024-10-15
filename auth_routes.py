from fastapi import APIRouter,HTTPException,status,Depends
from database import SessionLocal,engine,get_db
from schemas import SignupModel
from models import User
from sqlalchemy.orm import Session
from utils import hash_password

# from werkzeug.security import generate_password_hash,check_password_hash

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.get("/")
async def hello():
    return {"message":"Hello World"}

@auth_router.post("/signup", response_model=SignupModel, status_code=status.HTTP_201_CREATED)
def signup(user: SignupModel, db: Session = Depends(get_db)):
    # Check if email exists
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the email already exists")
    
    # Check if username exists
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with the username already exists")

    # Create new user
    new_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password=hash_password(user.password),  # Hash the password
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user