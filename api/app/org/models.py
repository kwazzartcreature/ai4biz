from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from db.base import Base
from lib import TimestampMixin


class OrgModel(Base, TimestampMixin):
    __tablename__ = "orgs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    schema_name = Column(String, default="", nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
