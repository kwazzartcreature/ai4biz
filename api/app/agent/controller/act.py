import logging
from fastapi import Depends

from agent.schemas import AgentAct
from agent.main_agent import main_agent, MainDeps
from chat.history.history import RedisHistory, redis_history
from chat.history.adapter import HistoryAdapter
from db.conn import async_session_maker
from chat.message.schemas import Role

REQ_ROLES = {Role.user, Role.system}
RES_ROLES = {Role.assistant, Role.tool}

logger = logging.getLogger(__name__)


async def act(data: AgentAct, history: RedisHistory = redis_history):
    stored = await history.get(data.connection_id)
    ai_history = HistoryAdapter.wrap(stored)
    logger.debug(
        "Retrieved %d messages from history. Steps for pydantic_ai created: %d",
        len(stored),
        len(ai_history),
    )

    async with async_session_maker(schema_name=data.schema) as session:
        result = await main_agent.arun(
            data.prompt,
            deps=MainDeps(session=session, connection_id=data.connection_id),
            message_history=ai_history,
        )

    new_messages = HistoryAdapter.unwrap(result.new_messages(), data.connection_id)
    logger.debug(
        "Generated %d new messages from Steps: %d",
        len(new_messages),
        len(result.new_messages()),
    )
    history.update(data.connection_id, new_messages)
