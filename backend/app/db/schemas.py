from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from enum import Enum

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6, max_length=72)

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AccountType(str, Enum):
    savings = "savings"
    current = "current"
    fd = "fd"

class AccountCreate(BaseModel):
    account_type: AccountType
    initial_deposit: Optional[float] = 0.0

class AccountOut(BaseModel):
    id: int
    account_number: str
    balance: float
    account_type: AccountType
    user_id: int

    class Config:
        orm_mode = True


class WithdrawRequest(BaseModel):
    account_id: int
    amount: float = Field(..., gt=0, description="Amount to withdraw")


class MoneyRequest(BaseModel):
    account_id: int
    amount: float

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_number: str
    amount: float