from fastapi import HTTPException


from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest

def get_wallet(wallet_name: str | None = None):
    # Если имя кошелька не указанно, считаем общий баланс
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets()
        return {"total_balance": sum(wallets.values())}

    # Проверяем существует ли запрашиваемый кошелёк 
    if not wallets_repository.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    # Возврощаем баланс конкретного кошелька
    return wallets_repository.get_wallet_balance_by_name(wallet_name)


def create_wallet(wallet: CreateWalletRequest):
    # Проверяем не существует ли уже такоей кошелёк 
    if wallets_repository.is_wallet_exist(wallet.name):
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {wallet.name} it already exists."
        )

    # Создаём новый кошелёк с начальным балансом
    new_balance = wallets_repository.create_wallet(wallet.name, wallet.initial_balance)

    # Возвращаем информаию о созданном кошельке 
    return {
        "massage": f"Wallet {wallet.name} created",
        "Wallet": wallet.name, 
        "opening balance": new_balance
    }