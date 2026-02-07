# How to Build ClawdBot: An AI-Powered Telegram Assistant

*A comprehensive guide to building an intelligent chatbot with RAG, Memory, and Tool Integration*

---

## Introduction

In this tutorial, we'll build **ClawdBot**, an AI-powered Telegram assistant that goes far beyond simple chatbots. ClawdBot features:

- 🧠 **Long-term Memory** - Remembers user preferences across sessions
- 🔍 **RAG (Retrieval Augmented Generation)** - Searches through conversation history
- 🔧 **Tool Integration** - Connects to GitHub, Notion, and more via MCP
- ⏰ **Smart Scheduling** - Sets reminders with natural language

Whether you're building a personal assistant, a team productivity bot, or a customer support agent, this architecture scales to meet your needs.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Message                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Telegram Bot Handler                      │
│  • Receives messages via python-telegram-bot                 │
│  • Routes commands (/start, /help, /tasks)                  │
│  • Sends responses back to users                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       AI Agent Core                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │   Memory    │ │     RAG     │ │      Tool Executor      ││
│  │   (mem0)    │ │  (Vector)   │ │  (Telegram, MCP, etc)   ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
│                        │                                     │
│                        ▼                                     │
│              ┌─────────────────────┐                        │
│              │   OpenAI GPT-4o    │                        │
│              │   (with tools)      │                        │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Persistence                          │
│  • SQLite: Sessions, Messages, Tasks                         │
│  • Vector Store: Embeddings for semantic search              │
│  • mem0.ai: Long-term user memories                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

Before we start, you'll need:

- **Python 3.10+** installed
- A **Telegram Bot Token** (from [@BotFather](https://t.me/BotFather))
- An **OpenAI API Key**
- (Optional) **mem0.ai API Key** for long-term memory
- (Optional) **GitHub/Notion tokens** for MCP integration

---

## Project Structure

Here's how we'll organize our code:

```
telegram-clawdbot/
├── src/
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration management
│   ├── agents/
│   │   └── agent.py         # Core AI logic with tool calling
│   ├── bot/
│   │   ├── handlers.py      # Telegram command handlers
│   │   └── telegram_bot.py  # Bot initialization
│   ├── rag/
│   │   ├── embeddings.py    # OpenAI embeddings
│   │   ├── vectorstore.py   # Vector database
│   │   ├── indexer.py       # Message indexing
│   │   └── retriever.py     # Semantic search
│   ├── memory/
│   │   ├── database.py      # SQLite for sessions/messages
│   │   └── mem0_client.py   # Long-term memory
│   ├── mcp/
│   │   ├── client.py        # MCP server connections
│   │   └── tool_converter.py # Tool format conversion
│   └── tools/
│       ├── scheduler.py     # Reminders and tasks
│       └── telegram_actions.py # Telegram API tools
├── requirements.txt
├── .env.example
└── README.md
```

---

## Step 1: Set Up the Project

### Install Dependencies

```bash
mkdir telegram-clawdbot && cd telegram-clawdbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install python-telegram-bot openai mem0ai pydantic pydantic-settings \
            python-dotenv apscheduler numpy colorlog
```

### Create Configuration

Create a `.env` file:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_key_here

# Optional - Memory
MEM0_API_KEY=your_mem0_key_here
MEMORY_ENABLED=true

# Optional - RAG
RAG_ENABLED=true

# Optional - MCP Tools
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
NOTION_API_TOKEN=your_notion_token
```

---

## Step 2: Build the Configuration System

We use **Pydantic** for type-safe configuration:

```python
# src/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class TelegramSettings(BaseSettings):
    bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")

class AISettings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    model: str = Field(default="gpt-4o", alias="AI_MODEL")
    max_tokens: int = Field(default=4096, alias="AI_MAX_TOKENS")

class MemorySettings(BaseSettings):
    enabled: bool = Field(default=True, alias="MEMORY_ENABLED")
    api_key: Optional[str] = Field(default=None, alias="MEM0_API_KEY")

class Settings(BaseSettings):
    telegram: TelegramSettings = TelegramSettings()
    ai: AISettings = AISettings()
    memory: MemorySettings = MemorySettings()
    
    class Config:
        env_file = ".env"
        extra = "ignore"

# Singleton pattern
_settings = None

def get_config() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
```

---

## Step 3: Implement the Database Layer

SQLite stores sessions, messages, and scheduled tasks:

```python
# src/memory/database.py
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import uuid

@dataclass
class Session:
    id: str
    user_id: int
    chat_id: int
    chat_type: str
    created_at: datetime

@dataclass
class Message:
    id: str
    session_id: str
    role: str
    content: str
    timestamp: datetime

# Database connection
_conn: Optional[sqlite3.Connection] = None

def init_database():
    """Initialize the database with required tables."""
    global _conn
    _conn = sqlite3.connect("data/clawdbot.db", check_same_thread=False)
    
    _conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            chat_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    _conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)
    
    _conn.commit()

def get_or_create_session(user_id: int, chat_id: int, chat_type: str) -> Session:
    """Get existing session or create a new one."""
    cursor = _conn.execute(
        "SELECT * FROM sessions WHERE user_id = ? AND chat_id = ?",
        (user_id, chat_id)
    )
    row = cursor.fetchone()
    
    if row:
        return Session(id=row[0], user_id=row[1], chat_id=row[2], 
                      chat_type=row[3], created_at=row[4])
    
    # Create new session
    session_id = str(uuid.uuid4())
    _conn.execute(
        "INSERT INTO sessions (id, user_id, chat_id, chat_type) VALUES (?, ?, ?, ?)",
        (session_id, user_id, chat_id, chat_type)
    )
    _conn.commit()
    
    return Session(id=session_id, user_id=user_id, chat_id=chat_id,
                  chat_type=chat_type, created_at=datetime.now())
```

---

## Step 4: Build the RAG System

RAG enables semantic search over conversation history.

### Embeddings

```python
# src/rag/embeddings.py
from openai import OpenAI
from typing import List
import numpy as np

def create_embedding(text: str) -> List[float]:
    """Create an embedding for a piece of text."""
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### Vector Store

```python
# src/rag/vectorstore.py
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Document:
    id: str
    text: str
    embedding: List[float]
    metadata: dict

class VectorStore:
    def __init__(self, path: str = "data/vectors.json"):
        self.path = path
        self.documents: List[Document] = []
        self._load()
    
    def add(self, doc: Document):
        self.documents.append(doc)
        self._save()
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Document]:
        """Find most similar documents."""
        scored = []
        for doc in self.documents:
            score = cosine_similarity(query_embedding, doc.embedding)
            scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]
```

---

## Step 5: Implement Long-Term Memory

Using **mem0.ai** for persistent user memories:

```python
# src/memory/mem0_client.py
from mem0 import MemoryClient
from typing import List, Optional

_client: Optional[MemoryClient] = None

def initialize_memory(api_key: str):
    """Initialize the mem0 client."""
    global _client
    _client = MemoryClient(api_key=api_key)

async def add_memory(messages: List[dict], user_id: int):
    """Extract and store memories from a conversation."""
    if _client is None:
        return
    
    _client.add(messages, user_id=str(user_id))

async def search_memory(query: str, user_id: int, limit: int = 5) -> List[dict]:
    """Search for relevant memories."""
    if _client is None:
        return []
    
    results = _client.search(query, user_id=str(user_id), limit=limit)
    return results.get("results", [])

def build_memory_context(memories: List[dict]) -> str:
    """Format memories for the LLM context."""
    if not memories:
        return ""
    
    lines = ["## Relevant Memories About This User:"]
    for mem in memories:
        lines.append(f"- {mem.get('memory', '')}")
    
    return "\n".join(lines)
```

---

## Step 6: Create the AI Agent

The agent orchestrates everything:

```python
# src/agents/agent.py
from openai import OpenAI
from dataclasses import dataclass
from typing import List

SYSTEM_PROMPT = """You are a helpful AI assistant integrated into Telegram.

## CAPABILITIES:
- Answer questions and have conversations
- Search knowledge base for relevant context
- Remember user preferences across sessions
- Use external tools like GitHub and Notion
- Set reminders with natural language

## TOOLS:
You have access to various tools. Use them when relevant:
- `search_knowledge_base` - Search past conversations
- `schedule_reminder` - Set reminders
- `get_chat_info` - Get chat information
- GitHub and Notion tools for external integrations

Be helpful, concise, and use Markdown formatting.
"""

@dataclass
class AgentContext:
    user_id: int
    chat_id: int
    session_id: str
    user_name: str

async def process_message(user_message: str, context: AgentContext) -> str:
    """Process a user message and generate a response."""
    client = OpenAI()
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # 1. Retrieve memories
    memories = await search_memory(user_message, context.user_id)
    if memories:
        memory_context = build_memory_context(memories)
        messages.append({"role": "system", "content": memory_context})
    
    # 2. Retrieve RAG context
    if should_use_rag(user_message):
        rag_results = await retrieve(user_message, chat_id=context.chat_id)
        if rag_results:
            messages.append({"role": "system", "content": rag_results})
    
    # 3. Add conversation history
    history = get_session_history(context.session_id)
    messages.extend(history)
    
    # 4. Add current message
    messages.append({"role": "user", "content": user_message})
    
    # 5. Call OpenAI with tools
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=get_all_tools(),
        tool_choice="auto"
    )
    
    # 6. Handle tool calls (loop until no more tools)
    assistant_message = response.choices[0].message
    
    while assistant_message.tool_calls:
        # Execute each tool
        for tool_call in assistant_message.tool_calls:
            result = await execute_tool(tool_call.function.name, 
                                        tool_call.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        # Continue conversation
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=get_all_tools()
        )
        assistant_message = response.choices[0].message
    
    # 7. Store memories asynchronously
    asyncio.create_task(add_memory([
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assistant_message.content}
    ], context.user_id))
    
    return assistant_message.content
```

---

## Step 7: Build Telegram Handlers

```python
# src/bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        "I'm **ClawdBot**, your AI assistant with:\n"
        "🧠 Memory - I remember our conversations\n"
        "🔍 RAG - I can search chat history\n"
        "🔧 Tools - I connect to GitHub, Notion & more\n\n"
        "Just send me a message to start chatting!",
        parse_mode="Markdown"
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    user = update.effective_user
    chat = update.effective_chat
    
    # Get session
    session = get_or_create_session(user.id, chat.id, chat.type)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=chat.id, action="typing")
    
    # Process through AI agent
    agent_context = AgentContext(
        user_id=user.id,
        chat_id=chat.id,
        session_id=session.id,
        user_name=user.first_name
    )
    
    response = await process_message(update.message.text, agent_context)
    
    await update.message.reply_text(response, parse_mode="Markdown")

def setup_handlers(application):
    """Register all handlers."""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        message_handler
    ))
```

---

## Step 8: Main Entry Point

```python
# src/main.py
import asyncio
from telegram.ext import Application
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Load configuration
    config = get_config()
    
    # Initialize services
    init_database()
    init_vectorstore()
    
    if config.memory.api_key:
        await initialize_memory(config.memory.api_key)
    
    # Create and run bot
    application = Application.builder() \
        .token(config.telegram.bot_token) \
        .build()
    
    setup_handlers(application)
    
    print("🚀 ClawdBot is running!")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Running Your Bot

```bash
# Make sure you're in the project directory with venv activated
python -m src.main
```

You should see:
```
🚀 ClawdBot is running!
```

Now open Telegram, find your bot, and send `/start`!

---

## Adding MCP Tools

To integrate GitHub and Notion, create `mcp-config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_TOKEN": "${NOTION_API_TOKEN}"
      }
    }
  }
}
```

The MCP client spawns these servers as subprocesses and communicates via JSON-RPC.

---

## Key Takeaways

1. **Modular Architecture** - Each component (RAG, Memory, Tools) is isolated and testable
2. **Async Everything** - Non-blocking I/O for responsive user experience
3. **Tool Calling Loop** - Let the LLM decide which tools to use, execute them, and continue
4. **Memory Layers** - Combine short-term (database) with long-term (mem0) memory
5. **Configuration First** - Use Pydantic for type-safe, validated configuration

---

## Next Steps

- **Add more tools**: Weather, calendar, web search
- **Implement webhooks**: For production deployment instead of polling
- **Add authentication**: Role-based access for team bots
- **Monitor & log**: Track usage, errors, and performance

---

## Resources

- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [mem0.ai Documentation](https://docs.mem0.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

*Built with ❤️ by the ClawdBot team*
