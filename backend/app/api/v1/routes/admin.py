from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.services.user_service import get_all_users, get_user_by_id
from app.core.auth import get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)]  # Only admins can access
)

# ---------------- Admin Endpoints ----------------

@router.get("/users")
def read_all_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
