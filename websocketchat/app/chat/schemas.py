from pydantic import BaseModel, Field


class MessageRead(BaseModel):
    id: int = Field(..., description="ID")
    sender_id: int = Field(..., description="ID отправителя")
    recipient_id: int = Field(..., description="ID получателя")
    content: str = Field(..., description="Содержимое сообщения")


class MessageCreate(BaseModel):
    recipient_id: int = Field(..., description="ID получателя")
    content: str = Field(..., description="Содержимое сообщения")
