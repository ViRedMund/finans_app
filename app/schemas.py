from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    # Валидатор для проверки положительной суммы
    @field_validator('amount')
    def amount_most_be_positive(cls, v: Decimal) -> Decimal:
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
    initial_balance: Decimal = 0

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