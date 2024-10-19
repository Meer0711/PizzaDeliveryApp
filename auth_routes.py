from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_db
from schemas import SignupModel,Token,UserResponse
from models import User
from sqlalchemy.orm import Session
from utils import get_password_hash, verify_password
from oauth2 import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.get("/")
async def hello():
    return {"message": "Hello World"}

@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"user_id": new_user.id})

    # Return user data without password
    return UserResponse(
        username=new_user.username,
        email=new_user.email,
        access_token=access_token,
        token_type="bearer"
    )
@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Verify user by username
    user = db.query(User).filter(User.username == form_data.username).first()

    # If user is not found or password is incorrect, raise an error
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Token expiration setup
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create access token with user_id
    access_token = create_access_token(
        data={"user_id": user.id},  # Pass the user_id in the token
        expires_delta=access_token_expires  # Use the calculated expiration time
    )

    # Return the token to the user
    return {"access_token": access_token, "token_type": "bearer"}