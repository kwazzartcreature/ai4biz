import logging
import pytest

from chat.history.history import redis_history, RedisHistory
from chat.message.schemas import Message, CreateMessage, MessageMetadata

logger = logging.getLogger(__name__)


@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize(
    "data",
    [
        CreateMessage(
            content="Hello! Who are you?",
            meta_data=MessageMetadata(role="user"),
            connection_id=1,
        ),
        [
            CreateMessage(
                content="Hello! Who are you?",
                meta_data=MessageMetadata(role="user"),
                connection_id=1,
            ),
            CreateMessage(
                content="I am your helper!",
                meta_data=MessageMetadata(role="assistant"),
                connection_id=1,
            ),
        ],
    ],
)
async def test_update(
    data: CreateMessage | list[CreateMessage], history: RedisHistory = redis_history
):
    await history.update(1, data)

    stored = await history.get(1)
    logger.info("Stored messages: %s", stored)

    assert isinstance(stored, list), "History should be a list"
    assert stored, "History should not be empty"
    assert isinstance(stored[0], Message), "History should contain Message objects"

    await history.invalidate_connection(1)


@pytest.mark.asyncio(loop_scope="module")
async def test_capacity(history: RedisHistory = redis_history):
    await history.update(
        2,
        [
            CreateMessage(
                content="Hello! Hello! Hello! Hello! Hello! Hello! Hello! Hello! Hello! Hello!",
                meta_data=MessageMetadata(role="user"),
                connection_id=2,
            ),
            CreateMessage(
                content="Yes! Yes! Yes! Yes! Yes! Yes! Yes! Yes! Yes! Yes! Yes! Yes!",
                meta_data=MessageMetadata(role="assistant"),
                connection_id=2,
            ),
        ]
        * 200,
    )

    stored = await history.get(2)
    logger.info("Stored messages: %s", history._count_tokens(stored))

    assert (
        history._count_tokens(stored) <= history._capacity
    ), "History should be truncated to capacity"

    await history.invalidate_connection(2)
