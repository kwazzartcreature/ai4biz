from sqlalchemy import text
from agent.models import AgentModel

from chat.channel.models import ChannelModel
from chat.connection.models import ConnectionModel
from chat.message.models import MessageModel
from chat.ticket.models import TicketModel
from chat.operator.models import OperatorModel

from knowledge.models import KnowledgeModel, KnowledgeChunkModel

from .conn import engine


async def init_org_schema(schema: str):
    def do_create(connection):
        AgentModel.__table__.create(bind=connection, checkfirst=True)
        OperatorModel.__table__.create(bind=connection, checkfirst=True)
        ChannelModel.__table__.create(bind=connection, checkfirst=True)
        ConnectionModel.__table__.create(bind=connection, checkfirst=True)
        MessageModel.__table__.create(bind=connection, checkfirst=True)
        TicketModel.__table__.create(bind=connection, checkfirst=True)

        KnowledgeModel.__table__.create(bind=connection, checkfirst=True)
        KnowledgeChunkModel.__table__.create(bind=connection, checkfirst=True)

    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        await conn.execute(text(f"SET search_path TO {schema}"))
        await conn.run_sync(do_create)
