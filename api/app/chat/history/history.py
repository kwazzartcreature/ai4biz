import logging
from redis.asyncio import ConnectionPool, Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
import tiktoken

from lib.config import REDIS_URL, HISTORY_TOKEN_CAPACITY
from chat.message.schemas import Message, CreateMessage

logger = logging.getLogger(__name__)


class RedisHistory:
    def __init__(self, client: Redis, capacity: int):
        self._client = client
        self._capacity = capacity
        self._encoder = tiktoken.get_encoding("o200k_base")

    async def get(self, connection_id: int) -> list[Message]:
        key = f"conn_history:{connection_id}"
        stored = await self._client.lrange(key, 0, -1)

        stored = [Message.model_validate_json(msg) for msg in stored]
        logger.info(
            "Retrieved %d messages for connection_id %d", len(stored), connection_id
        )
        return stored

    async def update(
        self, connection_id: int, messages: CreateMessage | list[CreateMessage]
    ) -> None:
        if isinstance(messages, CreateMessage):
            messages = [messages]

        key = f"conn_history:{connection_id}"

        messages: list[str] = [msg.model_dump_json() for msg in messages]
        await self._client.rpush(key, *messages)
        logger.info("Appended %d messages to key '%s'", len(messages), key)

        stored = await self.get(connection_id)
        total_tokens = self._count_tokens(stored)
        logger.info(
            "Total tokens after appending: %d (Capacity: %d)",
            total_tokens,
            self._capacity,
        )

        while total_tokens > self._capacity:
            removed = await self._client.lpop(key)
            if removed is None:
                logger.warning("No message to remove from key '%s'", key)
                break
            removed_msg = Message.model_validate_json(removed)
            tokens_removed = self._count_tokens(removed_msg)
            total_tokens -= tokens_removed
            logger.info(
                "Removed a message with %d tokens; new total tokens: %d",
                tokens_removed,
                total_tokens,
            )

    async def invalidate_connection(self, connection_id: int) -> None:
        await self._client.delete(f"conn_history:{connection_id}")
        logger.info("Invalidated history for connection_id %d", connection_id)

    async def close(self):
        await self._client.close()

    def _count_tokens(self, data: Message | list[Message]) -> int:
        if isinstance(data, list):
            return sum(len(self._encoder.encode(msg.content)) for msg in data)
        else:
            return len(self._encoder.encode(data.content))


pool = ConnectionPool.from_url(REDIS_URL)
client = Redis(
    connection_pool=pool,
    retry=Retry(ExponentialBackoff(), 5),
    health_check_interval=10,
    socket_connect_timeout=5,
    retry_on_timeout=True,
    socket_keepalive=True,
)
redis_history = RedisHistory(client, HISTORY_TOKEN_CAPACITY)
logger.info("Initialized RedisHistory with capacity %d", HISTORY_TOKEN_CAPACITY)
