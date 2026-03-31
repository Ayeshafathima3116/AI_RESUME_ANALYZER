"""
Pinecone vector database manager.
Handles index creation, upserting job embeddings, and similarity queries.
"""

from pinecone import Pinecone, ServerlessSpec
import config


def get_pinecone_client() -> Pinecone:
    """Get an initialized Pinecone client."""
    return Pinecone(api_key=config.PINECONE_API_KEY)


def init_index():
    """Create the Pinecone index if it doesn't exist. Returns the Index object."""
    pc = get_pinecone_client()
    index_name = config.PINECONE_INDEX_NAME

    # Check if index already exists
    existing = [idx.name for idx in pc.list_indexes()]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=config.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=config.PINECONE_CLOUD,
                region=config.PINECONE_REGION,
            ),
        )

    return pc.Index(index_name)


def get_index():
    """Get a reference to the existing Pinecone index."""
    pc = get_pinecone_client()
    return pc.Index(config.PINECONE_INDEX_NAME)


def upsert_job(index, job_id: str, embedding: list[float], metadata: dict):
    """Upsert a single job embedding into Pinecone."""
    index.upsert(vectors=[(job_id, embedding, metadata)])


def upsert_jobs_batch(index, vectors: list[tuple]):
    """
    Upsert a batch of job embeddings.
    vectors: list of (job_id, embedding, metadata) tuples
    """
    # Pinecone recommends batches of 100
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        index.upsert(vectors=batch)


def query_similar(index, embedding: list[float], top_k: int = 5) -> list[dict]:
    """Query Pinecone for the top-k most similar vectors."""
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return results.get("matches", [])


def delete_job(index, job_id: str):
    """Delete a job from the index."""
    index.delete(ids=[job_id])


def get_index_stats(index) -> dict:
    """Get statistics about the index."""
    return index.describe_index_stats()
