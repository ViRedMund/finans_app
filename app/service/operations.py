from fastapi import HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session

from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(db: Session, operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Добавляем сумму к балансу кошелька
    wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)

    db.commit()

    # Возвращаем информацию об операции
    return {
        "message": f"income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": wallet.balance
    }


def add_expense(db: Session, operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Проверяем достаточно ли средств на кошельке для данной операции
    wallet = wallets_repository.get_wallet_balance_by_name(db, operation.wallet_name)
    if  wallet.balance < operation.amount:
        raise HTTPException(
            status_code=404,
            detail=f"Insufficient funds in the wallet for this transaction. Available: {wallet.balance}"
        )

    # Вычитаем расход из баланса кошелька
    wallet = wallets_repository.add_expense(db, operation.wallet_name, operation.amount)

    db.commit()

    # Возвращаем информацию об операции
    return {
        "message": f"expense added.",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": wallet.balance
        }
