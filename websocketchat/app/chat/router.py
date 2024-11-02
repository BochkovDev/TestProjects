import asyncio
from typing import List, Dict, Literal

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse

from core.jinja2 import templates
from users.models import User
from users.dao import UsersDAO
from users.dependencies import get_current_user
from services.tasks import send_telegram_notification_task
from main_bot import notify_user
from .dao import MessagesDAO
from .schemas import MessageRead, MessageCreate


router = APIRouter(prefix='/chat', tags=['Chat'])
active_connections: Dict[int, WebSocket] = {}


async def notify_user(user_id: int, message: dict) -> bool:
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)
        return True
    return False

@router.get('/', response_class=HTMLResponse, summary='Chat Page')
async def chat(request: Request, user: User = Depends(get_current_user)):
    users = await UsersDAO.find_all()
    return templates.TemplateResponse('chat.html', {'request': request, 'user': user, 'users': users})

@router.post('/messages', response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    await MessagesDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id,
    )

    message_data = {
        'sender_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
    }

    is_notified = await notify_user(message.recipient_id, message_data)
    if not is_notified:
        send_telegram_notification_task.delay(message.recipient_id, current_user.username)
    await notify_user(current_user.id, message_data)

    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}

@router.get('/messages/{user_id}', response_model=List[MessageRead])
async def messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessagesDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


@router.websocket('/ws/{user_id}')
async def websocket_user_connect(websocket: WebSocket, user_id: int):
    await websocket.accept()
    
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)