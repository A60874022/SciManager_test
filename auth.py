# auth.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import User

# Константы
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "User One",
        "hashed_password": "fakehashedpassword1",  # Предположим, что это хэшированный пароль
        "disabled": False,
    },
}

# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Получение текущего пользователя на основе переданного токена.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = fake_users_db.get(token)  # Используем токен как имя пользователя
    if user is None:
        raise credentials_exception
    return User(**user)
