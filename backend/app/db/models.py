import random
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    # Add this relationship to fix the mapper error
    accounts = relationship("Account", back_populates="owner")


# ------------------ Account Model ------------------
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="accounts")

    # Add this to fix the Transaction relationship
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

    # Automatically generate a random 10-digit account number
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.account_number:
            self.account_number = str(random.randint(10**9, 10**10 - 1))



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    type = Column(String)  # 'withdraw' or 'deposit' or 'transfer'
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="transactions")
