"""
Embeddings Module

Converts text into vector embeddings using OpenAI's embedding API.
Embeddings are numerical representations of text that capture semantic meaning.
"""

import re
from typing import Optional

import numpy as np
from openai import OpenAI

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger("embeddings")

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
MAX_BATCH_SIZE = 100

# OpenAI client
_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Get the OpenAI client."""
    global _client
    if _client is None:
        config = get_config()
        _client = OpenAI(api_key=config.ai.openai_api_key)
    return _client


async def create_embedding(text: str) -> list[float]:
    """
    Create an embedding for a single text string.
    
    Args:
        text: The text to embed
    
    Returns:
        A vector of floating-point numbers (1536 dimensions)
    """
    if not text or not text.strip():
        logger.warning("Attempted to embed empty text")
        return [0.0] * EMBEDDING_DIMENSIONS
    
    try:
        client = _get_client()
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        
        embedding = response.data[0].embedding
        logger.debug(f"Created embedding for text ({len(text)} chars)")
        
        return embedding
    except Exception as e:
        logger.error(f"Failed to create embedding: {e}")
        raise


async def create_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Create embeddings for multiple texts in a batch.
    
    Args:
        texts: Array of texts to embed
    
    Returns:
        Array of embeddings in the same order as inputs
    """
    if not texts:
        return []
    
    # Filter out empty texts but track their positions
    valid_texts = []
    valid_indices = []
    
    for i, text in enumerate(texts):
        if text and text.strip():
            valid_texts.append(text)
            valid_indices.append(i)
    
    if not valid_texts:
        return [[0.0] * EMBEDDING_DIMENSIONS for _ in texts]
    
    results = [None] * len(texts)
    client = _get_client()
    
    # Process in batches
    for i in range(0, len(valid_texts), MAX_BATCH_SIZE):
        batch = valid_texts[i:i + MAX_BATCH_SIZE]
        batch_indices = valid_indices[i:i + MAX_BATCH_SIZE]
        
        try:
            logger.info(f"Processing embedding batch {i // MAX_BATCH_SIZE + 1}")
            
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch
            )
            
            for j, item in enumerate(response.data):
                original_index = batch_indices[j]
                results[original_index] = item.embedding
                
        except Exception as e:
            logger.error(f"Batch embedding failed: {e}")
            raise
    
    # Fill in zeros for empty texts
    for i in range(len(results)):
        if results[i] is None:
            results[i] = [0.0] * EMBEDDING_DIMENSIONS
    
    logger.info(f"Created {len(valid_texts)} embeddings")
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Returns:
        Similarity score between -1 and 1 (higher is more similar)
    """
    a_arr = np.array(a)
    b_arr = np.array(b)
    
    dot_product = np.dot(a_arr, b_arr)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(dot_product / (norm_a * norm_b))


def preprocess_text(text: str) -> str:
    """
    Prepare text for embedding by cleaning and normalizing.
    
    Args:
        text: Raw text from message
    
    Returns:
        Cleaned text ready for embedding
    """
    processed = text
    
    # Remove Telegram bot commands
    processed = re.sub(r'^/\w+\s*', '', processed)
    
    # Remove @mentions
    processed = re.sub(r'@\w+', '@user', processed)
    
    # Remove URLs
    processed = re.sub(r'https?://\S+', '[link]', processed)
    
    # Remove emoji codes (Telegram uses actual Unicode emojis mostly)
    # Remove excess whitespace
    processed = re.sub(r'\s+', ' ', processed).strip()
    
    # Skip very short messages
    if len(processed) < 10:
        return ""
    
    return processed
