"""
Embedding pipeline using HuggingFace Local Models.
Converts text into vector embeddings for storage and retrieval for free.
"""

from langchain_huggingface import HuggingFaceEmbeddings
import config


def get_embeddings_model() -> HuggingFaceEmbeddings:
    """Get the HuggingFace embeddings model via LangChain."""
    return HuggingFaceEmbeddings(
        model_name=config.HF_EMBEDDING_MODEL,
    )


def embed_text(text: str) -> list[float]:
    """Embed a single text string and return the vector."""
    model = get_embeddings_model()
    return model.embed_query(text)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a batch of text strings and return the vectors."""
    model = get_embeddings_model()
    return model.embed_documents(texts)

