from app.database import SessionLocal
from app.models import Wallet

from sqlalchemy.orm import Session
from decimal import Decimal

def is_wallet_exist(db: Session, wallet_name: str) -> bool:
    # Проверяем существует ли кошелек
        return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None


def add_income(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    # Добавление баланса к кошельку
        wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
        wallet.balance += amount
        return wallet


def add_expense(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    # Вычет расходов из баланса кошелька
        wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
        wallet.balance -= amount
        return wallet

def get_wallet_balance_by_name(db: Session, wallet_name: str) -> Wallet:
        return db.query(Wallet).filter(Wallet.name == wallet_name).first()


def get_all_wallets(db: Session) -> list[Wallet]:
        return db.query(Wallet).all()


def create_wallet(db: Session, wallet_name: str, initial_balanc: Decimal = 0) -> Wallet:
    # Создаем новый кошелек с указанным начальным балансом
        wallet = Wallet(name=wallet_name, balance=initial_balanc)
        db.add(wallet)
        db.flush()
        return wallet
