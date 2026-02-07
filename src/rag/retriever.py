"""
Retriever Module

Semantic search over indexed messages.
Transforms user queries into relevant context for the LLM.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config
from .embeddings import create_embedding, preprocess_text
from .vectorstore import search, SearchResult, init_vectorstore

logger = get_logger("retriever")


@dataclass
class RetrievedDocument:
    """Retrieved document with formatted content."""
    text: str
    score: float
    user_name: str
    timestamp: str
    message_id: int
    formatted: str


@dataclass
class RetrievalResponse:
    """Retrieval response with metadata."""
    query: str
    results: list[RetrievedDocument]
    total_found: int
    search_time_ms: int


async def retrieve(
    query: str,
    limit: int = 10,
    min_score: float = 0.3,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
) -> RetrievalResponse:
    """
    Retrieve relevant documents for a query.
    
    Args:
        query: User's natural language query
        limit: Max results
        min_score: Minimum similarity score
        chat_id: Optional filter by chat
        user_id: Optional filter by user
    
    Returns:
        Retrieved documents with relevance scores
    """
    start_time = datetime.now()
    
    config = get_config()
    if not config.rag.enabled:
        return RetrievalResponse(
            query=query,
            results=[],
            total_found=0,
            search_time_ms=0,
        )
    
    init_vectorstore()
    
    logger.info(f"Retrieving for query: \"{query[:50]}...\"")
    
    try:
        # Preprocess and embed query
        processed_query = preprocess_text(query) or query
        query_embedding = await create_embedding(processed_query)
        
        # Search vector store
        search_results = await search(
            query_embedding,
            limit=limit * 2,  # Get extra for filtering
            chat_id=chat_id,
            user_id=user_id,
        )
        
        # Filter by minimum score
        filtered_results = [r for r in search_results if r.score >= min_score]
        
        # Transform to retrieved documents
        retrieved_docs = []
        for result in filtered_results[:limit]:
            doc = RetrievedDocument(
                text=result.text,
                score=result.score,
                user_name=result.metadata.get("user_name", "Unknown"),
                timestamp=result.metadata.get("timestamp", ""),
                message_id=result.metadata.get("message_id", 0),
                formatted=_format_for_llm(result),
            )
            retrieved_docs.append(doc)
        
        search_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents in {search_time_ms}ms")
        
        return RetrievalResponse(
            query=query,
            results=retrieved_docs,
            total_found=len(filtered_results),
            search_time_ms=search_time_ms,
        )
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        raise


def _format_for_llm(result: SearchResult) -> str:
    """Format a search result for LLM context."""
    timestamp = result.metadata.get("timestamp", "")
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp)
            date_str = dt.strftime("%b %d")
        except:
            date_str = "Unknown"
    else:
        date_str = "Unknown"
    
    user_name = result.metadata.get("user_name", "Unknown")
    
    return f"[{date_str}] {user_name}: {result.text}"


def build_context_string(docs: list[RetrievedDocument]) -> str:
    """
    Build context string for LLM from retrieved documents.
    
    Args:
        docs: Retrieved documents
    
    Returns:
        Formatted context string
    """
    if not docs:
        return ""
    
    header = "## Relevant Chat History\n\nThe following messages may be relevant:\n\n"
    
    messages = []
    for i, doc in enumerate(docs, 1):
        messages.append(f"{i}. {doc.formatted}")
    
    footer = "\n\n---\nUse this context to inform your response."
    
    return header + "\n".join(messages) + footer


def should_use_rag(query: str) -> bool:
    """
    Determine if a query would benefit from RAG.
    
    Args:
        query: User query
    
    Returns:
        Whether RAG should be used
    """
    lower_query = query.lower()
    
    # Indicators that RAG would help
    rag_indicators = [
        "what did",
        "who said",
        "when did",
        "why did",
        "how did",
        "discussed",
        "mentioned",
        "talked about",
        "remember when",
        "last time",
        "before",
        "previously",
        "what was",
        "find messages",
        "search for",
    ]
    
    # Indicators that RAG is not needed
    no_rag_indicators = [
        "remind me",
        "set reminder",
        "hello",
        "hi",
        "hey",
        "thanks",
        "help",
        "/",  # Commands
    ]
    
    # Check for no-RAG indicators first
    for indicator in no_rag_indicators:
        if lower_query.startswith(indicator) or indicator in lower_query:
            return False
    
    # Check for RAG indicators
    for indicator in rag_indicators:
        if indicator in lower_query:
            return True
    
    # Default: use RAG for questions
    return "?" in lower_query or any(
        lower_query.startswith(q)
        for q in ["what ", "who ", "when ", "where ", "why ", "how "]
    )
