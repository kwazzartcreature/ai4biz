from sqlalchemy import select, text

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from agent.crawler.crawler import crawl_urls
from knowledge.models import KnowledgeChunkModel
from db.conn import AsyncSessionWithSchema
from llm.call import call_llm
from lib import OPENAI_API_KEY


class RagDeps(BaseModel):
    session: AsyncSessionWithSchema


class RagResult(BaseModel):
    knowledge: str = Field(..., description="The knowledge retrieved by the RAG agent.")
    enough_relevant: bool = Field(
        ...,
        description="Whether the retrieved knowledge is enough to help the customer, and no need to rentrieve more.",
    )


rag_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=RagDeps,
    result_type=RagResult,
    retries=3,
    system_prompt=(
        "You need to retrieve relevant information to help the customer."
        "After total retrieval process you need to specify, if there enough relevant information"
        "to help the customer or not."
    ),
)


@rag_agent.system_prompt
async def initial_retrieval(ctx: RunContext[RagDeps]) -> str:
    query_vector = []

    stmt = (
        select(KnowledgeChunkModel).order_by(text("vector <=> :query_vector")).limit(30)
    )
    res = await ctx.deps.session.execute(stmt, {"query_vector": query_vector})
    chunks = res.scalars().all()
    chunks = "\n\n".join(
        [
            f"\nCONTENT:\n{chunk.content}\nMETADATA:\n{chunk.metadata}"
            for chunk in chunks
        ]
    )
    # maybe we need to select only relevant ones
    return chunks


@rag_agent.tool()
async def retrieve_urls_content(ctx: RunContext[RagDeps], urls: list[str]) -> list[str]:
    """
    Call this function, if you need additional information to help the customer.
    Arguments:
        - urls: list of urls to crawl. Use if you want fetch additional information based on chunk content.
    """
    return await crawl_urls(urls)
