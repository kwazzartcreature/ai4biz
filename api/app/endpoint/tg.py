import asyncio
import time
import httpx
import requests


# WEBHOOKS
def set_webhook(bot_token: str, webhook_url: str):
    telegram_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    response = requests.post(telegram_url, json={"url": webhook_url})
    response.raise_for_status()
    return response.json()


def get_webhook_info(bot_token: str):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    response = requests.get(url)
    return response.json()


# POLLING
async def start_polling(bot_token: str):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    offset = 0
    print(f"Starting polling for bot: {bot_token}")

    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, params={"offset": offset, "timeout": 30}
                )
                updates = response.json().get("result", [])

            for update in updates:
                offset = update["update_id"] + 1
                print(f"Received update for bot {bot_token}: {update}")

                if "message" in update:
                    proccess_message(bot_token, update["message"])

        except Exception as e:
            print(f"Polling error for bot {bot_token}: {e}")

        await asyncio.sleep(1)


# TELEGRAM CHAT
def send_message(
    bot_token: str, chat_id: int, text: str, reply_to_message_id: int | None = None
):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_to_message_id": reply_to_message_id,
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")


def proccess_message(bot_token: str, message: dict):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    message_id = message["message_id"]

    if text.startswith("/start"):
        send_message(bot_token, chat_id, "Добро пожаловать! Я ваш бот.")
    else:
        send_message(
            bot_token,
            chat_id,
            f"Вы написали: {text}",
            reply_to_message_id=message_id,
        )
