from pydantic import BaseModel


class TelegramUpdate(BaseModel):
    update_id: int
    message: dict | None = None
    callback_query: dict | None = None


class Message(BaseModel):
    content: str
    sentAt: str
    role: str
