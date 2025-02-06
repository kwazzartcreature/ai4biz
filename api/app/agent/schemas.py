from enum import Enum
import uuid
from pydantic import BaseModel
from datetime import datetime

from chat.channel.schemas import ChannelConfigType


# class Status(Enum):
#     ACTIVE = "active"
#     INACTIVE = "inactive"


class LLMProvider(str, Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    CUSTOM = "custom"


class AgentConfig(BaseModel):
    provider: LLMProvider = LLMProvider.OPENAI
    model: str = ""
    secret: str = ""


class Agent(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    static_instruction: str
    config: AgentConfig
    created_at: datetime
    updated_at: datetime


class AgentCreate(BaseModel):
    name: str = ""
    description: str = ""
    static_instruction: str = ""
    config: AgentConfig = AgentConfig()


class AgentAct(BaseModel):
    prompt: str

    type: ChannelConfigType
    key: str

    schema: str
    connection_id: int
