import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.base import Base
from lib import TimestampMixin


class AgentModel(Base, TimestampMixin):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, default="", nullable=False)
    description = Column(String, nullable=True)

    static_instruction = Column(String, default="", nullable=False)
    config = Column(JSONB, default="{}", nullable=False)

    channels = relationship("ChannelModel", back_populates="agent")
