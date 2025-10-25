from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import schemas, database
from app.services import user_service
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(user_service.models.User).filter(user_service.models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db, user)

@router.post("/login", response_model=TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    auth_user = user_service.authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = user_service.create_token(auth_user)  # make sure this uses user.email or id
    return {"access_token": token, "token_type": "bearer"}
