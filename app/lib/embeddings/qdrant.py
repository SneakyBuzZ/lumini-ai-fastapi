from pydoc import cli
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.models import VectorParams
from app._core.config import settings
from app.lib.embeddings.sentence_transformer import generate_files_embeddings
from app._core.logger import logger

client = AsyncQdrantClient(url=settings.QDRANT_URL)

async def setup_qdrant():
    collections = await client.get_collections()
    existing = [c.name for c in collections.collections]
    if "labfile_collection" not in existing:
        await client.create_collection(
            collection_name="labfile_collection",
            vectors_config=VectorParams(size=384, distance="Cosine"),
        )
        logger.info("Created 'labfile_collection' in Qdrant.")
    else:
        logger.info("'labfile_collection' already exists in Qdrant.")

async def store_embeddings(files : list[dict],lab_id : str) -> None:
    files_with_embeddings = generate_files_embeddings(files, lab_id)
    await client.upsert(
        collection_name="labfile_collection",
        points=files_with_embeddings
    )

async def get_similar_files(query_embedding: list[float], lab_id: str, top_k: int = 5) -> list[dict]:
    filter_condition = Filter(
        must=[FieldCondition(key="lab_id", match=MatchValue(value=lab_id))]
    )
    results = await client.search(
        collection_name="labfile_collection",
        query_vector=query_embedding,
        limit=top_k,
        query_filter=filter_condition
    )
    similar_files = [r.payload for r in results]
    return similar_files