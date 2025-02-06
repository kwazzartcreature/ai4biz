import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.future import select

from auth.schemas import AuthPayload
from auth.middleware import auth_org
from db.conn import async_session_maker

from agent.models import AgentModel
from agent.schemas import Agent, AgentCreate

agent_router = APIRouter(prefix="/agents")


@agent_router.post("/", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(dto: AgentCreate, org: AuthPayload = Depends(auth_org)):
    agent = AgentModel(
        name=dto.name,
        description=dto.description,
        static_instruction=dto.static_instruction,
        config=dto.config.model_dump(),
    )

    async with async_session_maker(schema_name=org.schema_name) as session:
        session.add(agent)
        await session.commit()

    logging.info(f"Agent {agent.id} created")
    return agent


@agent_router.get("/", response_model=list[Agent])
async def get_agents(org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(select(AgentModel))
        agents = result.scalars().all()
    return agents


@agent_router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: int, org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if agent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
            )
    return agent


@agent_router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: int, org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if agent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found"
            )
        await session.delete(agent)
        await session.commit()

        logging.info(f"Agent {agent_id} deleted")
