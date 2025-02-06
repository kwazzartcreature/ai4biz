import uuid
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.base import Base
from lib.mixins import TimestampMixin

from .schemas import OperatorType


class OperatorModel(Base, TimestampMixin):
    __tablename__ = "operators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    login = Column(String, nullable=False, unique=True)
    type = Column(Enum(OperatorType), nullable=False)
    meta_data = Column("metadata", JSONB, default=lambda: {}, nullable=False)

    channels = relationship("ChannelModel", back_populates="operator")
