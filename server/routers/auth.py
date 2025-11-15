"""Authentication routers."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from controllers.auth_controller import AuthController
from middleware.auth import get_current_active_user
from models.user import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    user = AuthController.register_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = AuthController.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    return AuthController.create_token(user.username)


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info."""
    return current_user
