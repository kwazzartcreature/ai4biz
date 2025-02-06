import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.future import select

from auth.schemas import AuthPayload
from auth.middleware import auth_org
from db.conn import async_session_maker

from .models import ChannelModel
from .schemas import Channel, ChannelCreate, ChannelUpdate

channel_router = APIRouter(prefix="/channels")


@channel_router.post("/", response_model=Channel, status_code=status.HTTP_201_CREATED)
async def create_channel(dto: ChannelCreate, org: AuthPayload = Depends(auth_org)):
    channel = ChannelModel(
        name=dto.name,
        config=dto.config.model_dump(),
        type=dto.type,
        status=dto.status,
    )

    async with async_session_maker(schema_name=org.schema_name) as session:
        session.add(channel)
        await session.flush()

        result = await session.execute(
            select(ChannelModel).where(ChannelModel.id == channel.id)
        )
        channel = result.scalars().first()
        await session.commit()

    logging.info(f"Channel {channel.id} created")
    return channel


@channel_router.get("/", response_model=list[Channel])
async def list_channels(org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(select(ChannelModel))
        channels = result.scalars().all()
    return channels


@channel_router.get("/{channel_id}", response_model=Channel)
async def get_channel(channel_id: int, org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(
            select(ChannelModel).where(ChannelModel.id == channel_id)
        )
        channel = result.scalars().first()
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )
    return channel


@channel_router.put("/{channel_id}", response_model=Channel)
async def update_channel(
    channel_id: int, dto: ChannelUpdate, org: AuthPayload = Depends(auth_org)
):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(
            select(ChannelModel).where(ChannelModel.id == channel_id)
        )
        channel = result.scalars().first()
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )

        if dto.name is not None:
            channel.name = dto.name
        if dto.config is not None:
            channel.config = dto.config.model_dump()
        if dto.type is not None:
            channel.type = dto.type
        if dto.status is not None:
            channel.status = dto.status

        await session.commit()
    return channel


@channel_router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(channel_id: int, org: AuthPayload = Depends(auth_org)):
    async with async_session_maker(schema_name=org.schema_name) as session:
        result = await session.execute(
            select(ChannelModel).where(ChannelModel.id == channel_id)
        )
        channel = result.scalars().first()
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found"
            )

        await session.delete(channel)
        await session.commit()
    return None
