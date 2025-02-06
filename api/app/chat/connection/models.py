import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base
from lib.mixins import TimestampMixin


class ConnectionModel(Base, TimestampMixin):
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # context = Column(String, nullable=False)

    user_id = Column(UUID(as_uuid=True), nullable=True)

    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"))
    channel = relationship("ChannelModel", back_populates="connections")
