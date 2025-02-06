import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from db.base import Base
from lib import TimestampMixin


class TicketModel(Base, TimestampMixin):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    content = Column(String, nullable=False)
    meta_data = Column("metadata", JSONB, default=lambda: {}, nullable=False)

    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=False)
    message = relationship("MessageModel", back_populates="ticket")
