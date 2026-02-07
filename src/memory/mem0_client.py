"""
mem0 Memory Client

Integrates mem0.ai for long-term user memory.
mem0 automatically extracts facts from conversations and stores them,
enabling personalized AI experiences across sessions.

HOW IT WORKS:
1. After each conversation, we pass messages to mem0
2. mem0 uses an LLM to extract facts (e.g., "User prefers Python")
3. Facts are stored in a vector database for semantic retrieval
4. Before responding, we retrieve relevant memories for context
"""

from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger("mem0-client")


# Memory client instance
_memory_client = None
_initialized = False


async def initialize_memory() -> None:
    """Initialize the mem0 memory client."""
    global _memory_client, _initialized
    
    if _initialized:
        logger.debug("Memory already initialized")
        return
    
    config = get_config()
    
    if not config.memory.enabled:
        logger.info("Memory system is disabled")
        return
    
    if not config.memory.api_key:
        logger.warning("MEM0_API_KEY not configured, memory features disabled")
        return
    
    try:
        logger.info("Initializing mem0 cloud client...")
        
        # Import mem0
        from mem0 import MemoryClient
        
        _memory_client = MemoryClient(api_key=config.memory.api_key)
        _initialized = True
        
        logger.info("✅ mem0 cloud client initialized")
    except ImportError:
        logger.error("mem0ai package not installed. Run: pip install mem0ai")
        _initialized = False
    except Exception as e:
        logger.error(f"Failed to initialize mem0: {e}")
        _initialized = False


async def add_memory(
    messages: list[dict],
    user_id: int,
    metadata: Optional[dict] = None
) -> list[dict]:
    """
    Add memories from a conversation.
    mem0 will automatically extract facts from the messages.
    
    Args:
        messages: List of {"role": "user"|"assistant", "content": "..."}
        user_id: Telegram user ID
        metadata: Optional metadata
    
    Returns:
        List of extracted memories
    """
    if not _initialized or not _memory_client:
        logger.debug("Memory not initialized, skipping add")
        return []
    
    try:
        logger.debug(f"Adding memories for user {user_id}")
        
        result = _memory_client.add(
            messages,
            user_id=str(user_id),
            metadata={
                "source": "telegram",
                **(metadata or {})
            }
        )
        
        memories = result.get("results", []) if isinstance(result, dict) else result or []
        
        if memories:
            logger.info(f"Stored {len(memories)} memories for user {user_id}")
            for m in memories:
                if isinstance(m, dict):
                    logger.debug(f"  - {m.get('memory', m)}")
        
        return memories
    except Exception as e:
        logger.error(f"Failed to add memory: {e}")
        return []


async def search_memory(
    query: str,
    user_id: int,
    limit: int = 5
) -> list[dict]:
    """
    Search for relevant memories.
    
    Args:
        query: Search query
        user_id: Telegram user ID
        limit: Max results
    
    Returns:
        List of relevant memories with scores
    """
    if not _initialized or not _memory_client:
        logger.debug("Memory not initialized, skipping search")
        return []
    
    try:
        logger.debug(f"Searching memories for user {user_id}: \"{query[:50]}...\"")
        
        result = _memory_client.search(
            query,
            user_id=str(user_id),
            limit=limit,
            filters={"AND": [{"user_id": str(user_id)}]},
        )
        
        memories = result.get("results", []) if isinstance(result, dict) else result or []
        
        logger.debug(f"Found {len(memories)} relevant memories")
        return memories
    except Exception as e:
        logger.error(f"Failed to search memory: {e}")
        return []


async def get_all_memories(user_id: int) -> list[dict]:
    """Get all memories for a user."""
    if not _initialized or not _memory_client:
        return []
    
    try:
        logger.debug(f"Getting all memories for user {user_id}")
        
        result = _memory_client.get_all(user_id=str(user_id))
        memories = result.get("results", []) if isinstance(result, dict) else result or []
        
        logger.debug(f"User {user_id} has {len(memories)} memories")
        return memories
    except Exception as e:
        logger.error(f"Failed to get memories: {e}")
        return []


async def delete_all_memories(user_id: int) -> bool:
    """Delete all memories for a user."""
    if not _initialized or not _memory_client:
        return False
    
    try:
        logger.debug(f"Deleting all memories for user {user_id}")
        _memory_client.delete_all(user_id=str(user_id))
        logger.info(f"Deleted all memories for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete memories: {e}")
        return False


def build_memory_context(memories: list[dict]) -> str:
    """
    Build a context string from memories for the LLM.
    
    Args:
        memories: Array of memory objects
    
    Returns:
        Formatted context string
    """
    if not memories:
        return ""
    
    header = "## What I Remember About You\n\n"
    
    items = []
    for i, m in enumerate(memories, 1):
        if isinstance(m, dict):
            memory_text = m.get("memory", str(m))
        else:
            memory_text = str(m)
        items.append(f"{i}. {memory_text}")
    
    footer = "\n\nUse this context to personalize your responses."
    
    return header + "\n".join(items) + footer


def is_memory_enabled() -> bool:
    """Check if memory is initialized and available."""
    return _initialized and _memory_client is not None
