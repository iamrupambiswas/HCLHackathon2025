# app/api/v1/routes/accounts.py
from sqlalchemy.orm import Session
from app.db import database, schemas
from app.services import account_service
from app.api.v1.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=schemas.AccountOut)
def create_user_account(
    account: schemas.AccountCreate,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(get_current_user)
):
    return account_service.create_account(db, current_user.id, account)

# ------------------- GET API -------------------
@router.get("/", response_model=list[schemas.AccountOut])
def get_user_accounts(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(get_current_user)
):
    return account_service.get_accounts_by_user(db, current_user.id)


@router.post("/withdraw", response_model=schemas.AccountOut)
def withdraw(request: schemas.WithdrawRequest, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
    try:
        account = account_service.withdraw_money(db, current_user.id, request.account_id, request.amount)
        return account
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post("/deposit", response_model=schemas.AccountOut)
def deposit_money(
    request: schemas.MoneyRequest,  # We'll define this schema
    db: Session = Depends(database.get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        account = account_service.deposit_money(db, current_user.id, request.account_id, request.amount)
        return account
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post("/transfer", response_model=schemas.AccountOut)
def transfer_money_endpoint(
    request: schemas.TransferRequest,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        return account_service.transfer_money(
            db, current_user.id,
            request.from_account_id,
            request.to_account_number,
            request.amount
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))