"""
Vector Store Module

Simple in-memory vector store with JSON file persistence.
Stores message embeddings for semantic search.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config
from .embeddings import cosine_similarity

logger = get_logger("vectorstore")


@dataclass
class DocumentMetadata:
    """Metadata stored alongside embeddings."""
    chat_id: int
    user_id: int
    user_name: str
    timestamp: str
    message_id: int
    indexed_at: str


@dataclass
class Document:
    """Document structure for storage."""
    id: str
    text: str
    embedding: list[float]
    metadata: dict


@dataclass
class SearchResult:
    """Search result with similarity score."""
    id: str
    text: str
    score: float
    metadata: dict


# Vector store instance
_documents: dict[str, Document] = {}
_persist_path: Optional[Path] = None
_initialized = False


def init_vectorstore() -> None:
    """Initialize the vector store."""
    global _documents, _persist_path, _initialized
    
    if _initialized:
        return
    
    config = get_config()
    _persist_path = Path(config.rag.vector_db_path) / "vectors.json"
    _persist_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing data
    if _persist_path.exists():
        try:
            with open(_persist_path, "r") as f:
                data = json.load(f)
            
            for doc_id, doc_data in data.items():
                _documents[doc_id] = Document(
                    id=doc_data["id"],
                    text=doc_data["text"],
                    embedding=doc_data["embedding"],
                    metadata=doc_data["metadata"],
                )
            
            logger.info(f"Loaded {len(_documents)} documents from disk")
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
            _documents = {}
    
    _initialized = True
    logger.info("Vector store initialized")


def _persist() -> None:
    """Save documents to disk."""
    if not _persist_path:
        return
    
    try:
        data = {}
        for doc_id, doc in _documents.items():
            data[doc_id] = {
                "id": doc.id,
                "text": doc.text,
                "embedding": doc.embedding,
                "metadata": doc.metadata,
            }
        
        with open(_persist_path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"Failed to persist data: {e}")


async def add_documents(documents: list[Document]) -> None:
    """Add documents to the vector store."""
    if not _initialized:
        init_vectorstore()
    
    if not documents:
        return
    
    for doc in documents:
        _documents[doc.id] = doc
    
    _persist()
    logger.info(f"Added {len(documents)} documents to vector store")


async def search(
    query_embedding: list[float],
    limit: int = 10,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
) -> list[SearchResult]:
    """
    Search for similar documents.
    
    Args:
        query_embedding: Query vector
        limit: Max results
        chat_id: Optional filter by chat
        user_id: Optional filter by user
    
    Returns:
        Sorted list of search results
    """
    if not _initialized:
        init_vectorstore()
    
    results = []
    
    for doc in _documents.values():
        # Apply filters
        if chat_id and doc.metadata.get("chat_id") != chat_id:
            continue
        if user_id and doc.metadata.get("user_id") != user_id:
            continue
        
        # Calculate similarity
        score = cosine_similarity(query_embedding, doc.embedding)
        
        results.append(SearchResult(
            id=doc.id,
            text=doc.text,
            score=score,
            metadata=doc.metadata,
        ))
    
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    
    return results[:limit]


async def get_document_count() -> int:
    """Get the total number of documents."""
    if not _initialized:
        init_vectorstore()
    return len(_documents)


async def document_exists(doc_id: str) -> bool:
    """Check if a document exists."""
    if not _initialized:
        init_vectorstore()
    return doc_id in _documents


async def clear_all() -> None:
    """Clear all documents."""
    global _documents
    _documents = {}
    _persist()
    logger.warning("Cleared all documents from vector store")
