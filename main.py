from fastapi import FastAPI, HTTPException


#Инициализация FastAPI проекта
app = FastAPI()


# Словарь для хранение баланса
# Ключ - название кошелька, значение - баланс кошелька
BALANCE = {}


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

@app.post("/wallets/{name}")
def receive_mony(name: str, amount: int):
    # Если кошелька с таким именем нет, создаем его с балансом 0
    if name not in BALANCE:
        BALANCE[name] = 0

    # Добавляем сумму к балансу кошелька
    BALANCE[name] += amount

    # Возвращаем информацию об операции
    return {
        "massege": f"Added {amount} to {name}",
        "wallet": name,
        "new_balance": BALANCE[name]
    }