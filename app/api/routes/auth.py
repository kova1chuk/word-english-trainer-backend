from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserRead, Token
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(
    tags=["Auth"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        400: {"description": "Bad Request"}
    },
)


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "Email already registered",
                "field": "email"
            }
        )
    user = User(email=data.email,
                hashed_password=get_password_hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, email=user.email)


@router.post("/signin", response_model=Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "Incorrect email or password",
                "field": "password" if user else "email"
            }
        )
    token = create_access_token(str(user.id))
    return Token(access_token=token)


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: User = Depends(get_current_user)):
    return UserRead(id=current_user.id, email=current_user.email)
