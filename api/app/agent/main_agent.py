import logging
import select
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from chat.channel.models import Channel as ChannelModel
from chat.connection.models import Connection as ConnectionModel
from db.conn import AsyncSessionWithSchema

from .rag_agent import rag_agent, RagResult
from .schemas import Agent
from .models import AgentModel


logger = logging.getLogger(__name__)


class MainDeps(BaseModel):
    session: AsyncSessionWithSchema
    connection_id: int


main_agent = Agent(
    "openai:gpt-4o",
    deps_type=MainDeps,
    result_type=str,
    system_prompt=("You need to help the customer with their issue."),
)


@main_agent.system_prompt
async def inject_system_prompt(ctx: RunContext[MainDeps]) -> str:
    async with ctx.deps.session as session:
        result = await session.execute(
            select(ConnectionModel).where(ConnectionModel.id == ctx.deps.connection_id)
        )

        connection = result.scalar_one_or_none()
        logger.debug(connection)

        if connection and connection.channel and connection.channel.agent:
            return connection.channel.agent.static_instruction
        return ""


@main_agent.tool
async def retrieve_knowledge(ctx: RunContext[MainDeps]) -> RagResult:
    """
    Call this function, if you need additional information to help the customer.
    """
    r = await rag_agent.run(f"User query: {ctx.prompt}", deps=ctx.deps)
    return r.data


@main_agent.tool
async def call_operator(ctx: RunContext[MainDeps]) -> str:
    """
    Call this function, if you need to escalate the issue to a human operator.
    For example, if you don't have enough information to help the customer,
    or if the customer explicitly asked to talk to a human 2 or more times.
    """
    logger.info("Escalating to a human operator")

    # find operator for the channel

    return "I will connect you to a human operator."


async def _create_ticket(): ...
