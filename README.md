# Telegram ClawdBot 🤖

An AI-powered Telegram assistant with advanced capabilities including RAG (Retrieval Augmented Generation), long-term memory (mem0), and MCP (Model Context Protocol) tool integration.

## Features

| Feature | Description |
|---------|-------------|
| 🧠 **Memory** | Long-term memory using mem0.ai - remembers user preferences across sessions |
| 🔍 **RAG** | Semantic search over chat history using vector embeddings |
| 🔧 **MCP Tools** | GitHub and Notion integration via Model Context Protocol |
| ⏰ **Scheduler** | Task scheduling with reminders |
| 💬 **Multi-Model** | Supports OpenAI GPT models |

## Quick Start

### 1. Clone and Install

```bash
cd telegram-clawdbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
OPENAI_API_KEY=your_openai_api_key

# Optional - Memory
MEM0_API_KEY=your_mem0_api_key

# Optional - MCP Tools
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
NOTION_API_TOKEN=your_notion_token
```

### 3. Run

```bash
python -m src.main
```

## Project Structure

```
telegram-clawdbot/
├── src/
│   ├── main.py              # Entry point
│   ├── config.py            # Pydantic configuration
│   ├── agents/
│   │   └── agent.py         # AI agent with tool calling
│   ├── bot/
│   │   ├── handlers.py      # Telegram command/message handlers
│   │   └── telegram_bot.py  # Bot initialization
│   ├── rag/
│   │   ├── embeddings.py    # OpenAI embeddings
│   │   ├── vectorstore.py   # Vector storage
│   │   ├── indexer.py       # Message indexing
│   │   └── retriever.py     # Semantic search
│   ├── memory/
│   │   ├── database.py      # SQLite database
│   │   └── mem0_client.py   # mem0 integration
│   ├── mcp/
│   │   ├── client.py        # MCP server connections
│   │   ├── config.py        # MCP configuration
│   │   └── tool_converter.py # Tool format conversion
│   └── tools/
│       └── scheduler.py     # Task scheduling
├── data/                    # Database and vectors
├── logs/                    # Log files
├── requirements.txt
└── .env.example
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | List all commands |
| `/status` | Bot status and features |
| `/reset` | Clear conversation history |
| `/forget` | Delete all memories |
| `/tasks` | List scheduled tasks |
| `/cancel <id>` | Cancel a task |

## Architecture

```
User Message → Telegram Bot → Agent
                                ↓
                    ┌───────────────────────┐
                    │ 1. Retrieve memories  │
                    │ 2. Retrieve RAG docs  │
                    │ 3. Build context      │
                    │ 4. Call LLM           │
                    │ 5. Execute tools      │
                    │ 6. Store memories     │
                    └───────────────────────┘
                                ↓
                    Response → User
```

## Configuration Options

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `OPENAI_API_KEY` | ✅ | OpenAI API key |
| `AI_MODEL` | ❌ | Model name (default: gpt-4o) |
| `MEM0_API_KEY` | ❌ | mem0.ai API key for memory |
| `MEMORY_ENABLED` | ❌ | Enable/disable memory (default: true) |
| `RAG_ENABLED` | ❌ | Enable/disable RAG (default: true) |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | ❌ | GitHub token for MCP |
| `NOTION_API_TOKEN` | ❌ | Notion token for MCP |
| `LOG_LEVEL` | ❌ | Logging level (default: info) |

## Getting API Keys

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow prompts
3. Copy the token

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an API key

### mem0 API Key
1. Go to [mem0.ai](https://mem0.ai)
2. Sign up and get API key

### GitHub Token
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Generate a token with `repo` scope

### Notion Token
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create an integration

## License

MIT
