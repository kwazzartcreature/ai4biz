from enum import Enum
import uuid
from pydantic import BaseModel


class OperatorType(str, Enum):
    tg = "tg"
    custom = "custom"


class TGOperator(BaseModel):
    tg_user_id: str


class CustomOperator(BaseModel):
    password_hash: str


class Operator(BaseModel):
    id: uuid.UUID
    login: str
    type: OperatorType
    config: TGOperator | CustomOperator


class OperatorCreate(BaseModel):
    login: str
    type: OperatorType
    config: TGOperator | CustomOperator
