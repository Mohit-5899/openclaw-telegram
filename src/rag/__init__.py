"""RAG (Retrieval Augmented Generation) module."""

from .embeddings import create_embedding, create_embeddings, cosine_similarity, preprocess_text
from .vectorstore import (
    init_vectorstore,
    add_documents,
    search,
    get_document_count,
    document_exists,
    clear_all,
)
from .indexer import start_indexer, stop_indexer, index_single_message, get_indexer_status
from .retriever import retrieve, build_context_string, should_use_rag

__all__ = [
    # Embeddings
    "create_embedding",
    "create_embeddings",
    "cosine_similarity",
    "preprocess_text",
    # Vector Store
    "init_vectorstore",
    "add_documents",
    "search",
    "get_document_count",
    "document_exists",
    "clear_all",
    # Indexer
    "start_indexer",
    "stop_indexer",
    "index_single_message",
    "get_indexer_status",
    # Retriever
    "retrieve",
    "build_context_string",
    "should_use_rag",
]
