from sqlalchemy.orm import Session
from app.db import models, schemas
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.db.models import User

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_token(user: models.User):
    token_data = {"user_id": user.id, "is_admin": user.is_admin}
    return create_access_token(token_data)



def verify_token(db: Session, token: str):
    """
    Decode JWT token and return the corresponding user from DB.
    """
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return user
    except Exception:
        return None


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()