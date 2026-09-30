from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.models import User
from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest
from app.database import SessionLocal

def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    # Если имя кошелька не указанно, считаем общий баланс
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        return {"total_balance": sum([w.balance for w in wallets])}

    # Проверяем существует ли запрашиваемый кошелёк 
    if not wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    # Возврощаем баланс конкретного кошелька
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, wallet_name)
    return {"wallet": wallet.name, "balance": wallet.balance}



def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):
    # Проверяем не существует ли уже такоей кошелёк 
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {wallet.name} already exists."
        )

    # Создаём новый кошелёк с начальным балансом
    wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance)

    db.commit()

    # Возвращаем информаию о созданном кошельке 
    return {
        "message": f"Wallet {wallet.name} created",
        "Wallet": wallet.name, 
        "opening balance": wallet.balance
    }
