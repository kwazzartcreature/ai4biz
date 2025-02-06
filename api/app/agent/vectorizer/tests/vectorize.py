import pytest

from agent.vectorizer.vectorizer import Vectorizer

from lib import OPENAI_API_KEY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query",
    [
        "The capital of France is Paris.",
        "🚀🔥💡",
        ["The capital of Russia is Moscow.", "🚀🔥💡"],
    ],
)
async def test_vectorization(query: str | list[str]):
    vectors = await Vectorizer.vectorize(
        OPENAI_API_KEY, query, "text-embedding-3-small"
    )

    assert isinstance(vectors, list), "Результат должен быть списком"
    assert isinstance(vectors[0], list), "Вектор должен быть списком чисел"
    assert all(
        isinstance(x, float) for x in vectors[0]
    ), "Все элементы вектора должны быть float"

    print(query, vectors)
