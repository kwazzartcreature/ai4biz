import enum
import uuid
from pydantic import BaseModel


class ChannelStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ChannelConfigType(enum.Enum):
    WS = "ws"
    TG = "tg"
    EMAIL = "email"


class WSConfig(BaseModel):
    host: str
    token: str


class TGConfig(BaseModel):
    token: str


class WSConfig(BaseModel):
    host: str


class EmailConfig(BaseModel):
    email: str


class CustomConfig(BaseModel):
    key: str = ""


class Channel(BaseModel):
    id: uuid.UUID
    type: ChannelConfigType
    config: TGConfig | WSConfig | EmailConfig | CustomConfig
    status: ChannelStatus
    name: str
    agent_id: int | None


class ChannelCreate(BaseModel):
    type: ChannelConfigType
    agent_id: int | None = None
    name: str = ""
    config: TGConfig | WSConfig | EmailConfig | CustomConfig = CustomConfig()
    status: ChannelStatus = ChannelStatus.ACTIVE


class ChannelUpdate(BaseModel):
    name: str | None = None
    config: TGConfig | WSConfig | EmailConfig | CustomConfig | None = None
    status: ChannelStatus | None = None
    agent_id: int | None = None
