import uuid
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from db.base import Base
from lib import TimestampMixin

from .schemas import KnowledgeType, KnowledgeStatus


class KnowledgeModel(Base, TimestampMixin):
    __tablename__ = "knowledge"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, default="", nullable=False)
    type = Column(Enum(KnowledgeType), nullable=False)
    status = Column(Enum(KnowledgeStatus), nullable=False)
    url = Column(String, nullable=False)
    namespace = Column(String, nullable=False)

    last_indexed = Column(DateTime, nullable=True)

    chunks = relationship("KnowledgeChunkModel", back_populates="knowledge")


class KnowledgeChunkModel(Base, TimestampMixin):
    __tablename__ = "knowledge_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    hash = Column(String, nullable=False)
    content = Column(String, default="", nullable=False)
    meta_data = Column("metadata", JSONB, default=lambda: {}, nullable=False)
    order = Column(Integer, nullable=False)

    vector = Column(ARRAY(Float, dimensions=1536), nullable=True)

    knowledge_id = Column(UUID(as_uuid=True), ForeignKey("knowledge.id"))
    knowledge = relationship("KnowledgeModel", back_populates="chunks")
