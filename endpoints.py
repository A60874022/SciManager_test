# endpoints.py

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from faststream.rabbit.fastapi import RabbitRouter
from models import Message, User
from auth import get_current_user

router = APIRouter()
rabbit_router = RabbitRouter("amqp://guest:guest@localhost:5672/")
rooms: dict[str, list[str]] = {}

@router.post("/message/")
async def post_message(message: Message, user: User = Depends(get_current_user)):
    """
    Отправка сообщения в указанную комнату.
    """
    if message.room_id not in rooms:
        rooms[message.room_id] = []
    rooms[message.room_id].append(message.content)
    await rabbit_router.publish(message.content, routing_key=message.room_id)
    return {"status": "Message sent"}

@router.websocket('/updates/{room_id}')
async def get_updates(websocket: WebSocket, room_id: str, user: User = Depends(get_current_user)):
    """
    Получение обновлений из указанной комнаты через WebSocket.
    """
    await websocket.accept()
    try:
        while True:
            message = await rabbit_router.consume(routing_key=room_id)
            await websocket.send_text(message)
    except WebSocketDisconnect:
        print(f"Client disconnected from room: {room_id}")
