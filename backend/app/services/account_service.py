from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime, timedelta

DAILY_LIMIT = 100000  # Set daily limit


def create_account(db: Session, user_id: int, account_data):
    """
    Create a new account for a user.
    account_data should have account_type and optional initial_deposit
    """
    initial_balance = getattr(account_data, "initial_deposit", 0.0)

    # Create the account
    account = models.Account(
        user_id=user_id,
        account_type=account_data.account_type,
        balance=initial_balance
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    # If initial deposit > 0, log it as a transaction
    if initial_balance > 0:
        transaction = models.Transaction(
            account_id=account.id,
            type="deposit",
            amount=initial_balance
        )
        db.add(transaction)
        db.commit()

    return account

# ---------------- Withdraw ----------------
def withdraw_money(db: Session, user_id: int, account_id: int, amount: float):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")

    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == user_id
    ).first()
    if not account:
        raise ValueError("Account not found")

    # Check daily withdrawal limit
    today = datetime.utcnow()
    start_of_day = datetime(today.year, today.month, today.day)
    daily_withdrawals = db.query(models.Transaction).filter(
        models.Transaction.account_id == account_id,
        models.Transaction.type == "withdraw",
        models.Transaction.created_at >= start_of_day
    ).all()
    total_today = sum(tx.amount for tx in daily_withdrawals)
    if total_today + amount > DAILY_LIMIT:
        raise ValueError("Daily withdrawal limit exceeded")

    if account.balance < amount:
        raise ValueError("Insufficient balance")

    account.balance -= amount
    transaction = models.Transaction(
        account_id=account.id,
        type="withdraw",
        amount=amount
    )
    db.add(account)
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account


# ---------------- Deposit ----------------
def deposit_money(db: Session, user_id: int, account_id: int, amount: float):
    """
    Deposit money into a user's account and log the transaction.
    """
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")

    # Fetch the account for the user
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == user_id
    ).first()

    if not account:
        raise ValueError("Account not found")

    # Update balance
    account.balance += amount

    # Log transaction
    transaction = models.Transaction(
        account_id=account.id,
        type="deposit",
        amount=amount
    )

    # Commit changes
    db.add(account)
    db.add(transaction)
    db.commit()
    db.refresh(account)

    return account

# ---------------- Transfer ----------------
def transfer_money(db: Session, user_id: int, from_account_id: int, to_account_number: str, amount: float):
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    from_account = db.query(models.Account).filter(
        models.Account.id == from_account_id,
        models.Account.user_id == user_id
    ).first()
    if not from_account:
        raise ValueError("Source account not found")

    to_account = db.query(models.Account).filter(
        models.Account.account_number == to_account_number
    ).first()
    if not to_account:
        raise ValueError("Recipient account not found")

    # Daily limit for transfers
    today = datetime.utcnow()
    start_of_day = datetime(today.year, today.month, today.day)
    daily_transfers = db.query(models.Transaction).filter(
        models.Transaction.account_id == from_account_id,
        models.Transaction.type == "transfer",
        models.Transaction.created_at >= start_of_day
    ).all()
    total_today = sum(tx.amount for tx in daily_transfers)
    if total_today + amount > DAILY_LIMIT:
        raise ValueError("Daily transfer limit exceeded")

    if from_account.balance < amount:
        raise ValueError("Insufficient balance")

    # Perform transfer
    from_account.balance -= amount
    to_account.balance += amount

    # Create transactions
    tx_out = models.Transaction(
        account_id=from_account.id,
        type="transfer",
        amount=amount
    )
    tx_in = models.Transaction(
        account_id=to_account.id,
        type="deposit",
        amount=amount
    )

    db.add_all([from_account, to_account, tx_out, tx_in])
    db.commit()
    db.refresh(from_account)
    return from_account
    
def get_accounts_by_user(db: Session, user_id: int):
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()