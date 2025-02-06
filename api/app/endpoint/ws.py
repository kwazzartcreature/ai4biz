from fastapi import WebSocket

from auth.utils import decode_token
from lib import ExpiredTokenException, InvalidTokenException


async def validate_websocket_request(websocket: WebSocket, token: str):
    try:
        payload = decode_token(token)
        host = payload.get("host")

        # if host not in ALLOWED_HOSTS:
        # await websocket.close(code=4001)

    except ExpiredTokenException:
        await websocket.close(code=4002)
    except InvalidTokenException:
        await websocket.close(code=4003)
    except Exception:
        await websocket.close(code=4000)
