from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

#Инициализация FastAPI проекта
app = FastAPI()


# Словарь для хранение баланса
# Ключ - название кошелька, значение - баланс кошелька
BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    # Валидатор для проверки положительной суммы
    @field_validator('amount')
    def amount_most_be_positive(cls, v: float) -> float:
        # Проверяем что значение больше 0 или рейзим ошибку
        if v <= 0:
            raise ValueError("Amount most be positive")

        # Возвращаем значение
        return v

    # Валидатор для проверки корректного имени кошелька
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        # Убираем пробелы по карям
        v = v.strip()

        # Проверяем что имя не пустое
        if not v:
            raise ValueError("Wallet name cannot be empty")

        # Возвращаем имя
        return v



class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    # Валидатор для проверки корректного имени кошелька
    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        # Убираем пробелы по карям
        v = v.strip()

        # Проверяем что имя не пустое
        if not v:
            raise ValueError("Wallet name cannot be empty")

        # Возвращаем имя
        return v

    # Валидатор для проверки положительной суммы
    @field_validator('initial_balance')
    def initial_balance_not_negative(cls, v: float) -> float:
        # Проверяем что значение больше 0 или рейзим ошибку
        if v < 0:
            raise ValueError("Initial balance cannot be negative")

        # Возвращаем значение
        return v


@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    # Если имя кошелька не указанно, считаем общий баланс
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}

    # Проверяем существует ли запрашиваемый кошелёк 
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    # Возврощаем баланс конкретного кошелька
    return {"Wallet": wallet_name, "balance": BALANCE[wallet_name]}

@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    # Проверяем не существует ли уже такоей кошелёк 
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {wallet.name} it already exists."
        )

    # Создаём новый кошелёк с начальным балансом
    BALANCE[wallet.name] = wallet.initial_balance

    # Возвращаем информаию о созданном кошельке 
    return {
        "massage": f"Wallet {wallet.name} created",
        "Wallet": wallet.name, 
        "opening balance": BALANCE[wallet.name]
    }

@app.post("/balance/income")
def add_income(operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Добавляем сумму к балансу кошелька
    BALANCE[operation.wallet_name] += operation.amount

    # Возвращаем информацию об операции
    return {
        "massage": f"income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": BALANCE[operation.wallet_name]
    }



@app.post("/balance/expense")
def add_expence(operation: OperationRequest):
    # Проверяем существует ли такой кошелёк
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404, 
            detail=f"A wallet with the name {operation.wallet_name} does not exist."
        )

    # Проверяем достаточно ли средств на кошельке для данной операции
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=404,
            detail=f"Insufficient funds in the wallet for this transaction. Available: {BALANCE[operation.wallet_name]}"
        )

    # Вычитаем расход из баланса кошелька
    BALANCE[operation.wallet_name] -= operation.amount

    # Возвращаем информацию об операции
    return {
        "massage": f"expense added.",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "wallet balance": BALANCE[operation.wallet_name]
    }

