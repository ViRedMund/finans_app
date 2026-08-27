from sqlalchemy.orm import Session

from app.models import User

# Получение юзера по логину
def get_user(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).scalar()

# Создание юзера
def create_user(db: Session, login: str) -> User:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user