from enum import Enum
import uuid
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.base import Base
from lib.mixins import TimestampMixin

from .schemas import ChannelConfigType, ChannelStatus


class ChannelModel(Base, TimestampMixin):
    __tablename__ = "channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    type = Column(Enum(ChannelConfigType), nullable=False)
    config = Column(JSONB, nullable=False)
    status = Column(Enum(ChannelStatus), default=ChannelStatus.ACTIVE, nullable=False)
    name = Column(String, default="", nullable=False)

    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    agent = relationship("AgentModel", back_populates="channels")

    connections = relationship("ConnectionModel", back_populates="channel")

    operator_id = Column(UUID(as_uuid=True), ForeignKey("operators.id"), nullable=True)
    operator = relationship("OperatorModel", back_populates="channels")
