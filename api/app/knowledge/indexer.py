import asyncio
import logging
import uuid
import tiktoken

from db.conn import async_session_maker
from agent.crawler.crawler import Crawler
from agent.llm.call import call_llm
from agent.vectorizer.vectorizer import Vectorizer
from lib import OPENAI_API_KEY

from .models import KnowledgeChunkModel
from .parser import Parser

logger = logging.getLogger(__name__)


class Indexer:
    _crawler = Crawler
    _encoder = tiktoken.get_encoding("o200k_base")
    _sitemap_parser = Parser
    _max_tokens = 8190

    @classmethod
    async def index_page(
        cls, knowledge_id: uuid.UUID, schema_name: str, url: str, order=0
    ):
        contents = await cls._crawler.crawl_urls(url)
        if len(contents) == 0:
            raise Exception("No content found")

        logger.info(f"Indexed {url}")
        logger.debug(f"Content: {contents[0]}")

        summary = await call_llm(OPENAI_API_KEY, "gpt-4o", f"{contents[0]}")
        logger.info(f"Summary fetch with len: {len(summary)}")
        logger.debug(f"Summary: {summary}")

        tokens_summary = cls._encoder.encode(summary)
        tokens_summary = tokens_summary[: cls._max_tokens]
        summary = cls._encoder.decode(tokens_summary)

        vector = await Vectorizer.vectorize(summary)
        logger.info(f"Vectorized with len: {len(vector)}")

        content_hash = hash(summary)
        chunk = KnowledgeChunkModel(
            content=summary,
            meta_data={
                url: url,
            },
            vector=vector,
            hash=content_hash,
            knowledge_id=knowledge_id,
            order=order,
        )
        async with async_session_maker(schema_name=schema_name) as session:
            session.add(chunk)
            await session.commit()

    @classmethod
    async def index_domain(
        cls, knowledge_id: uuid.UUID, schema_name: str, sitemap_path: str
    ):
        urls = cls._sitemap_parser.parse(sitemap_path)
        tasks = []
        for i, url in enumerate(urls):
            tasks.append(cls.index_page(knowledge_id, schema_name, url, i))

        try:
            results = await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Failed to index domain: {e}")
            return

        return results

    @classmethod
    async def index_file(cls, file_path: str): ...
