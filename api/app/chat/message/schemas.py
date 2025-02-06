from datetime import datetime
import uuid
from enum import Enum
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    model_config = {"arbitrary_types_allowed": True}


class Role(str, Enum):
    system = "system"  # instructions and knowledge
    assistant = "assistant"  # agent responses
    user = "user"  # user prompts, inputs
    tool = "tool"  # tool result


class MessageMetadata(BaseModel):
    role: Role
    label: str | None = None
    name: str | None = None


class Message(MessageBase):
    id: uuid.UUID
    content: str
    meta_data: MessageMetadata
    connection_id: int
    created_at: datetime


class CreateMessage(MessageBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    content: str
    meta_data: MessageMetadata
    connection_id: int
    created_at: datetime = Field(default_factory=datetime.now)
