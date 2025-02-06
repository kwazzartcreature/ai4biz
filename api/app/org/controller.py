import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.future import select

from auth.middleware import auth_super, auth_org
from auth.schemas import AuthPayload
from auth.utils import hash_password
from db.conn import async_session_maker
from db.schema_init import init_org_schema
from lib import WORKING_BASE

from .models import OrgModel
from .schemas import OrgCreate, Org
import os

org_router = APIRouter(prefix="/orgs")


@org_router.post(
    "/",
    response_model=Org,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_super)],
)
async def create_org(org_data: OrgCreate):
    org = OrgModel(
        name=org_data.name,
        password_hash=hash_password(org_data.password),
    )

    try:
        async with async_session_maker() as session:
            session.add(org)
            await session.flush()

            schema_name = f"org_{org.id}"
            org.schema_name = schema_name

            await session.commit()

        await init_org_schema(org.schema_name)
        os.makedirs(os.path.join(WORKING_BASE, org.schema_name), exist_ok=True)
        return org
    except Exception as e:
        logging.error(f"Ошибка при создании организации: {e}")
        raise HTTPException(status_code=400, detail="Ошибка при создании организации")


@org_router.delete("/{org_id}", dependencies=[Depends(auth_super)])
async def delete_org(org_id: int):
    async with async_session_maker() as session:
        org = await session.execute(select(OrgModel).where(OrgModel.id == org_id))
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
            )

        org = org.scalars().first()
        await session.execute(text(f"DROP SCHEMA {org.schema_name} CASCADE"))
        await session.delete(org)
        await session.commit()
        os.rmdir(os.path.join(WORKING_BASE, org.schema_name))

    return {"message": f"Organization {org.id} deleted"}


@org_router.get("/", response_model=list[Org], dependencies=[Depends(auth_super)])
async def get_orgs(skip: int = 0, limit: int = -1):
    query = select(OrgModel)
    query = query.order_by(OrgModel.id).offset(skip)
    if limit > 0:
        query = query.limit(limit)

    async with async_session_maker() as session:
        result = await session.execute(query)

    return result.scalars().all()


@org_router.get("/{org_id}", response_model=Org)
async def get_org(org_id: int, payload: AuthPayload = Depends(auth_org)):
    if payload.id != org_id and not payload.super:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    async with async_session_maker() as session:
        org = await session.execute(select(OrgModel).where(OrgModel.id == org_id))

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return org.scalars().first()
