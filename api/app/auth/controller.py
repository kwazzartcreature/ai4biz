from json import JSONDecodeError
import logging
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)
from fastapi.responses import JSONResponse
from sqlalchemy.future import select

from org.models import OrgModel
from db.conn import async_session_maker
from lib import SUPER_LOGIN, SUPER_PASSWORD

from .schemas import AuthPayload, Login
from .utils import compare_passwords, generate_token

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login")
async def login(login_data: Login):
    logging.debug("Login request")
    try:
        login = login_data.login
        password = login_data.password

        payload = AuthPayload(id=0, super=False, org="", schema_name="")

        if login == SUPER_LOGIN and password == SUPER_PASSWORD:
            payload.super = True
            payload.id = 0
            payload.org = "SUPER"
            payload.schema_name = "public"

        async with async_session_maker() as session:
            org = await session.execute(select(OrgModel).where(OrgModel.name == login))
            org = org.scalars().first()

        if not org and not payload.super:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if org and compare_passwords(password, org.password_hash):
            payload.id = org.id
            payload.org = org.name
            payload.schema_name = org.schema_name

    except JSONDecodeError as e:
        logging.error("ARRR, ERROR!", e)
        raise HTTPException(status_code=400, detail="Bad request")

    token = generate_token(payload.model_dump(), expires=60 * 24 * 7)
    response = JSONResponse(content={"token": token})
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        samesite="None",
        secure=True,
    )

    return response


@auth_router.post("/chat/get-token")
async def get_token(request: Request):
    host = request.headers.get("Host")

    # if host not in ALLOWED_HOSTS:
    # raise HTTPException(status_code=403, detail="Unauthorized domain")

    response = JSONResponse(content={"message": "Token set in cookie"})
    response.set_cookie(
        key="token",
        value=generate_token({"host": host}),
        httponly=True,
        samesite="None",
        secure=True,
    )
    return response
