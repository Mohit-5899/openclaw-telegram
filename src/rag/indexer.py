"""
Indexer Module

Background indexing of Telegram messages into the vector database.
"""

import asyncio
from datetime import datetime
from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config
from .embeddings import create_embedding, preprocess_text
from .vectorstore import add_documents, document_exists, init_vectorstore, Document

logger = get_logger("indexer")

# Indexer state
_is_running = False
_task: Optional[asyncio.Task] = None
_index_interval = 3600  # 1 hour in seconds


def start_indexer() -> None:
    """Start the background indexer."""
    global _is_running, _task
    
    config = get_config()
    if not config.rag.enabled:
        logger.info("RAG is disabled, indexer not started")
        return
    
    if _is_running:
        logger.warning("Indexer already running")
        return
    
    _is_running = True
    logger.info("Indexer started (indexes on-demand via index_single_message)")


def stop_indexer() -> None:
    """Stop the background indexer."""
    global _is_running, _task
    
    _is_running = False
    if _task:
        _task.cancel()
        _task = None
    
    logger.info("Indexer stopped")


async def index_single_message(
    message_id: int,
    chat_id: int,
    user_id: int,
    user_name: str,
    text: str,
) -> bool:
    """
    Index a single message immediately.
    
    Args:
        message_id: Telegram message ID
        chat_id: Chat ID
        user_id: User ID
        user_name: User display name
        text: Message text
    
    Returns:
        True if indexed successfully
    """
    try:
        init_vectorstore()
        
        # Preprocess text
        processed_text = preprocess_text(text)
        if not processed_text or len(processed_text) < 10:
            return False
        
        # Generate document ID
        doc_id = f"{chat_id}:{message_id}"
        
        # Check if already indexed
        if await document_exists(doc_id):
            return False
        
        # Create embedding
        embedding = await create_embedding(processed_text)
        
        # Create document
        now = datetime.now().isoformat()
        document = Document(
            id=doc_id,
            text=processed_text,
            embedding=embedding,
            metadata={
                "chat_id": chat_id,
                "user_id": user_id,
                "user_name": user_name,
                "message_id": message_id,
                "timestamp": now,
                "indexed_at": now,
            }
        )
        
        # Add to vector store
        await add_documents([document])
        
        logger.debug(f"Indexed message: {doc_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to index message: {e}")
        return False


def get_indexer_status() -> dict:
    """Get indexer status."""
    return {
        "is_running": _is_running,
    }
