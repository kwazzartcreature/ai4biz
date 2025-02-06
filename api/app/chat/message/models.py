import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.base import Base
from lib.mixins import TimestampMixin


class MessageModel(Base, TimestampMixin):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    content = Column(String, nullable=False)
    meta_data = Column("metadata", JSONB, default=lambda: {}, nullable=False)

    connection_id = Column(UUID(as_uuid=True), ForeignKey("connections.id"))
    connection = relationship("ConnectionModel")

    ticket = relationship("TicketModel", back_populates="message", uselist=False)
