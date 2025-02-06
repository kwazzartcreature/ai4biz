from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def set_schema(cls, schema_name: str):
        cls.__table_args__ = {"schema": schema_name}
