from fastapi import HTTPException


from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest
from app.database import SessionLocal

def get_wallet(wallet_name: str | None = None):
    db = SessionLocal()
    try:
        # Если имя кошелька не указанно, считаем общий баланс
        if wallet_name is None:
            wallets = wallets_repository.get_all_wallets(db)
            return {"total_balance": sum([w.balance for w in wallets])}

        # Проверяем существует ли запрашиваемый кошелёк 
        if not wallets_repository.is_wallet_exist(db, wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_name}' not found"
            )

        # Возврощаем баланс конкретного кошелька
        wallet = wallets_repository.get_wallet_balance_by_name(db, wallet_name)
        return {"wallet": wallet.name, "balance": wallet.balance}
    finally:
        db.close()


def create_wallet(wallet: CreateWalletRequest):
    db = SessionLocal()
    try:
        # Проверяем не существует ли уже такоей кошелёк 
        if wallets_repository.is_wallet_exist(db, wallet.name):
            raise HTTPException(
                status_code=400, 
                detail=f"Wallet {wallet.name} it already exists."
            )

        # Создаём новый кошелёк с начальным балансом
        wallet = wallets_repository.create_wallet(db, wallet.name, wallet.initial_balance)

        db.commit

        # Возвращаем информаию о созданном кошельке 
        return {
            "massage": f"Wallet {wallet.name} created",
            "Wallet": wallet.name, 
            "opening balance": wallet.balance
        }
    finally:
        db.close()