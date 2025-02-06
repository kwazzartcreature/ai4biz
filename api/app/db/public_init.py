import logging
import lib
from org.models import OrgModel

from db.conn import engine


async def create_tables():
    def create_tables_sync(conn):
        OrgModel.__table__.create(conn, checkfirst=True)

    async with engine.begin() as session:
        await session.run_sync(create_tables_sync)

    logging.info(f"Tables are created")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
