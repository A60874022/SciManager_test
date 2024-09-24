# models.py

from pydantic import BaseModel

class User(BaseModel):
    """
    Модель пользователя.
    """
    username: str

class Message(BaseModel):
    """
    Модель сообщения.
    """
    room_id: str
    content: str

