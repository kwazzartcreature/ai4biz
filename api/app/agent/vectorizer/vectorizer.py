from openai import AsyncOpenAI


class Vectorizer:
    @staticmethod
    async def vectorize(token: str, queries: str | list[str], model: str) -> list[str]:
        if isinstance(queries, str):
            queries = [queries]

        client = AsyncOpenAI(api_key=token)

        res = await client.embeddings.create(input=queries, model=model)
        vectors = list(map(lambda x: x.embedding, res.data))
        return vectors
