from datetime import datetime
import uuid
from pydantic import BaseModel, Field
from enum import Enum


class KnowledgeStatus(Enum):
    RAW = "raw"
    INDEXED = "indexed"


class KnowledgeType(Enum):
    DOMAIN = "domain"
    SITE = "site"
    FILE = "file"


class Knowledge(BaseModel):
    id: uuid.UUID
    type: KnowledgeType
    status: KnowledgeStatus
    name: str
    url: str
    namespace: str
    last_indexed: datetime

    model_config = {"arbitrary_types_allowed": True}


class KnowledgeCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    status: KnowledgeStatus = KnowledgeStatus.RAW
    name: str = ""
    url: str
    type: KnowledgeType
    namespace: str

    model_config = {"arbitrary_types_allowed": True}


# CHUNKS
class KnowledgeChunk(BaseModel): ...
