from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio import create_async_engine

from lib import DATABASE_URL


class AsyncSessionWithSchema(AsyncSession):
    def __init__(self, *args, schema_name: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._schema_name = schema_name

    async def set_schema(self, schema_name: str):
        self._schema_name = schema_name
        await self.execute(text(f'SET search_path TO "{schema_name}", "public"'))

    async def __aenter__(self):
        await super().__aenter__()
        if self._schema_name:
            await self.set_schema(self._schema_name)
        return self


engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSessionWithSchema,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
