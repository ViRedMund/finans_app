from fastapi import HTTPException

from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Добавляем сумму к балансу кошелька
    new_balance = wallets_repository.add_income(operation.wallet_name, operation.amount)

    # Возвращаем информацию об операции
    return {
        "massage": f"income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": new_balance 
    }

def add_expense(operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Проверяем достаточно ли средств на кошельке для данной операции
    balance = wallets_repository.get_wallet_balance_by_name(operation.wallet_name)
    if  balance < operation.amount:
        raise HTTPException(
            status_code=404,
            detail=f"Insufficient funds in the wallet for this transaction. Available: {balance}"
        )

    # Вычитаем расход из баланса кошелька
    new_balance = wallets_repository.add_expense(operation.wallet_name, operation.amount)

    # Возвращаем информацию об операции
    return {
        "massage": f"expense added.",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": new_balance
        }