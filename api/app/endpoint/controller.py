import asyncio
import json
import logging
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    BackgroundTasks,
)

from lib import USE_TG_WEBHOOK, API_HOST, API_PORT, ENDPOINT_PREFIX, API_PREFIX

from .schemas import TelegramUpdate
from .tg import proccess_message, set_webhook, start_polling
from .ws import validate_websocket_request

TG_PREFIX = "/tg/webhook"

endpoint_router = APIRouter(prefix=ENDPOINT_PREFIX)

bot_clients = set(["7862898890:AAE5RaOY1X73U4jos-dTjxwAraMVP-rcHwA"])


async def on_startup():
    logging.info("Chat router started")
    webhook_base = (
        f"https://{API_HOST}:{API_PORT}{API_PREFIX}{ENDPOINT_PREFIX}{TG_PREFIX}"
    )
    logging.debug("TG_WEBHOOK: ", webhook_base)

    if USE_TG_WEBHOOK:
        for bot_token in bot_clients:
            set_webhook(bot_token, webhook_base)
    else:
        for bot_token in bot_clients:
            asyncio.create_task(start_polling(bot_token))


@endpoint_router.post(TG_PREFIX)
async def webhook_handler(
    background_tasks: BackgroundTasks,
    update: TelegramUpdate,
    org_id=Query(None),
    channel_id=Query(None),
):
    if channel_id not in bot_clients:
        raise HTTPException(status_code=404, detail="Bot not found")

    if update.message:
        proccess_message(channel_id, update.message)

    elif update.callback_query:
        print(f"Callback Query: {update.callback_query}")

    return {"status": "ok"}


@endpoint_router.websocket("/ws")
async def websocket_endpoint(background_tasks: BackgroundTasks, websocket: WebSocket):
    token = websocket.cookies.get("token")
    print("TOKEN: ", token)

    try:
        await validate_websocket_request(websocket, token)
        await websocket.accept()
    except:
        return

    agent = None

    try:
        init_data = await websocket.receive_text()
        try:
            history = json.loads(init_data)
            # agent = init_agent(history)
        except (json.JSONDecodeError, KeyError):
            await websocket.close(code=4004)
            return

        while True:
            raw_message = await websocket.receive_text()
            answer = await agent.send_message(raw_message)

            await websocket.send_text(answer.model_dump_json())

    except WebSocketDisconnect:
        print("Client disconnected")
