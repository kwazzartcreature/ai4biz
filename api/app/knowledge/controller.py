import logging
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import text
from sqlalchemy.future import select

from auth.schemas import AuthPayload
from auth.middleware import auth_org
from db.conn import async_session_maker

from .models import KnowledgeModel
from .schemas import Knowledge, KnowledgeCreate, KnowledgeType
from .indexer import Indexer

knowledge_router = APIRouter(prefix="/knowledge")

logger = logging.getLogger(__name__)


@knowledge_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Knowledge
)
async def create_knowledge(
    dto: KnowledgeCreate,
    file: UploadFile = File(None),
    org: AuthPayload = Depends(auth_org),
    to_index: bool = Query(False),
):
    namespace = dto.namespace if dto.namespace else org.schema_name

    if file is not None:
        ...

    knowledge = KnowledgeModel(
        name=dto.name,
        type=dto.type,
        status=dto.status,
        url=dto.url,
        namespace=namespace,
    )

    async with async_session_maker(schema_name=org.schema_name) as session:
        session.add(knowledge)
        await session.commit()

    logger.info(f"Knowledge {knowledge.id} created")

    if not to_index:
        return knowledge

    if dto.type == KnowledgeType.DOMAIN:
        await Indexer.index_domain(knowledge.id, namespace, dto.url)
    elif dto.type == KnowledgeType.PAGE:
        await Indexer.index_page(knowledge.id, namespace, dto.url)
    elif dto.type == KnowledgeType.FILE:
        logger.error("File type is not supported yet")
        # await Indexer.index_file(knowledge.id, namespace, dto.url)
