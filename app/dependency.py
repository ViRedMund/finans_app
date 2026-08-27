from typing import Generator
from fastapi import Depends, HTTPException
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm  import Session
from app.repository import users as users_repository
from app.database import SessionLocal

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)):

    login = credentials.credentials

    user = users_repository.get_user(db, login)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
                            )

    return user