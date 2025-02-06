import logging
from fastapi import Request, HTTPException


from .utils import decode_token
from .schemas import AuthPayload


async def auth_super(request: Request):
    token = request.headers.get("Authorization")
    payload = decode_token(token)

    if not payload or not payload.get("super"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    logging.info("Super user authorized")
    return payload


async def auth_org(request: Request):
    token = request.headers.get("Authorization")
    try:
        payload = decode_token(token)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    logging.debug(f"Org user authorized: {payload}")
    return AuthPayload.model_validate(payload)
