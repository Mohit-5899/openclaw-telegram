"""
AI Agent

Core agent logic for processing messages with RAG, Memory, MCP, and Telegram tool integration.
Uses Anthropic Claude (Opus 4.6) for conversation.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Optional

from anthropic import Anthropic

from ..utils.logger import get_logger
from ..config import get_config
from ..memory.database import get_session_history, add_message, get_user_tasks
from ..memory.mem0_client import (
    search_memory,
    add_memory,
    build_memory_context,
    is_memory_enabled,
)
from ..rag import retrieve, build_context_string, should_use_rag
from ..mcp import get_all_tools, execute_tool
from ..mcp.client import is_mcp_tool
from ..mcp.tool_converter import format_mcp_result
from ..tools.telegram_actions import (
    TELEGRAM_TOOLS,
    get_user_info,
    get_chat_info,
    send_message as tg_send_message,
    get_chat_member_count,
    get_chat_administrators,
    forward_message,
    pin_message,
    unpin_message,
)
from ..tools.scheduler import task_scheduler, parse_relative_time

logger = get_logger("agent")


# System prompt with tool usage rules
SYSTEM_PROMPT = """You are a helpful AI assistant integrated into Telegram.

## CAPABILITIES:
- Answer questions and have conversations
- Search knowledge base for relevant context (when RAG is enabled)
- Remember user preferences across sessions (when Memory is enabled)
- Use external tools like GitHub and Notion (when MCP is configured)
- Manage Telegram operations (send messages, get user/chat info, etc.)
- Set reminders and scheduled tasks

## TELEGRAM TOOLS:
You have access to Telegram-specific tools:
- `send_message` - Send messages to any chat
- `get_user_info` - Get information about a user
- `get_chat_info` - Get information about a chat/group
- `get_chat_member_count` - Count members in a group
- `get_chat_administrators` - List group admins
- `forward_message` - Forward messages between chats
- `pin_message` / `unpin_message` - Pin/unpin messages
- `schedule_reminder` - Set reminders (e.g., "in 5 minutes", "tomorrow at 9am")
- `list_reminders` - View scheduled reminders
- `cancel_reminder` - Cancel a reminder by ID

## MCP TOOLS:

### GitHub Rules (ALWAYS FOLLOW):
- User mentions "repos", "repositories", "GitHub", "issues", "PR", "code" → CALL a github_* tool
- NEVER say "I don't have access to GitHub" - you DO have access via tools

### Notion Rules (ALWAYS FOLLOW):
- User mentions "Notion", "pages", "docs", "notes", "database" → CALL a notion_* tool
- NEVER say "I don't have access to Notion" - you DO have access via tools

## CONVERSATION STYLE:
- Be helpful, friendly, and concise
- Use Markdown formatting for better readability
- For reminders, confirm what you scheduled

## CRITICAL INSTRUCTION:
When in doubt, USE THE TOOL. Never refuse by saying you don't have access.
"""


@dataclass
class AgentContext:
    """Context for agent processing."""
    user_id: int
    chat_id: int
    session_id: str
    user_name: str = "User"
    chat_type: str = "private"


@dataclass
class AgentResponse:
    """Response from the agent."""
    content: str
    tool_calls: list[dict] = field(default_factory=list)
    memories_retrieved: int = 0
    rag_results: int = 0


# Anthropic client
_client: Optional[Anthropic] = None


def _get_client() -> Anthropic:
    """Get the Anthropic client."""
    global _client
    if _client is None:
        config = get_config()
        _client = Anthropic(api_key=config.ai.anthropic_api_key)
    return _client


# Built-in tools for the agent (Anthropic format)
BUILT_IN_TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search the knowledge base for relevant past messages and conversations",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]


def _get_all_tools() -> list[dict]:
    """Get all available tools (built-in + Telegram + MCP)."""
    tools = BUILT_IN_TOOLS.copy()
    tools.extend(TELEGRAM_TOOLS)
    mcp_tools = get_all_tools()
    tools.extend(mcp_tools)
    return tools


async def _execute_tool(
    name: str,
    args: dict,
    context: AgentContext
) -> str:
    """Execute a tool and return the result."""
    logger.info(f"Executing tool: {name}")

    # ============================================
    # Built-in RAG Tool
    # ============================================
    if name == "search_knowledge_base":
        query = args.get("query", "")
        result = await retrieve(query, chat_id=context.chat_id)

        if not result.results:
            return "No relevant messages found in the knowledge base."

        formatted = []
        for doc in result.results:
            formatted.append(f"- [{doc.user_name}]: {doc.text}")

        return "Found relevant messages:\n" + "\n".join(formatted)

    # ============================================
    # Telegram Tools
    # ============================================
    if name == "send_message":
        chat_id = args.get("chat_id")
        text = args.get("text")
        result = await tg_send_message(chat_id, text)
        if result:
            return f"Message sent to chat {chat_id}"
        return "Failed to send message"

    if name == "get_user_info":
        user_id = args.get("user_id")
        user = await get_user_info(user_id)
        if user:
            return f"User Info:\n- ID: {user.id}\n- Username: @{user.username or 'N/A'}\n- Name: {user.first_name} {user.last_name or ''}"
        return "User not found or not accessible"

    if name == "get_chat_info":
        chat_id = args.get("chat_id")
        chat = await get_chat_info(chat_id)
        if chat:
            return f"Chat Info:\n- ID: {chat.id}\n- Type: {chat.type}\n- Title: {chat.title or 'N/A'}\n- Username: @{chat.username or 'N/A'}"
        return "Chat not found or not accessible"

    if name == "get_chat_member_count":
        chat_id = args.get("chat_id")
        count = await get_chat_member_count(chat_id)
        return f"Chat {chat_id} has {count} members"

    if name == "get_chat_administrators":
        chat_id = args.get("chat_id")
        admins = await get_chat_administrators(chat_id)
        if admins:
            admin_list = "\n".join([f"- {a.first_name} (@{a.username or 'N/A'})" for a in admins])
            return f"Administrators ({len(admins)}):\n{admin_list}"
        return "No administrators found or not accessible"

    if name == "forward_message":
        from_chat = args.get("from_chat_id")
        to_chat = args.get("to_chat_id")
        message_id = args.get("message_id")
        result = await forward_message(from_chat, to_chat, message_id)
        if result:
            return f"Message forwarded to chat {to_chat}"
        return "Failed to forward message"

    if name == "pin_message":
        chat_id = args.get("chat_id")
        message_id = args.get("message_id")
        success = await pin_message(chat_id, message_id)
        if success:
            return f"Message {message_id} pinned"
        return "Failed to pin message"

    if name == "unpin_message":
        chat_id = args.get("chat_id")
        message_id = args.get("message_id")
        success = await unpin_message(chat_id, message_id)
        if success:
            return "Message unpinned"
        return "Failed to unpin message"

    # ============================================
    # Reminder/Scheduler Tools
    # ============================================
    if name == "schedule_reminder":
        reminder_text = args.get("reminder_text")
        time_expr = args.get("time_expression")

        scheduled_time = parse_relative_time(time_expr)
        if not scheduled_time:
            return f"Could not parse time: '{time_expr}'. Try 'in 5 minutes', 'tomorrow at 9am', or 'at 3pm'."

        task = await task_scheduler.schedule_task(
            user_id=context.user_id,
            chat_id=context.chat_id,
            description=reminder_text,
            scheduled_time=scheduled_time,
        )

        return f"Reminder scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M')}:\n\"{reminder_text}\"\n\nReminder ID: #{task.id}"

    if name == "list_reminders":
        tasks = get_user_tasks(context.user_id)
        pending = [t for t in tasks if t.status == "pending"]

        if not pending:
            return "No pending reminders."

        lines = ["**Your Reminders:**"]
        for t in pending[:10]:
            lines.append(f"- #{t.id}: {t.task_description}")

        return "\n".join(lines)

    if name == "cancel_reminder":
        reminder_id = args.get("reminder_id")
        success = task_scheduler.cancel_task(reminder_id, context.user_id)
        if success:
            return f"Reminder #{reminder_id} cancelled"
        return f"Could not cancel reminder #{reminder_id}. It may not exist or already be completed."

    # ============================================
    # MCP Tools
    # ============================================
    if is_mcp_tool(name):
        try:
            result = await execute_tool(name, args)
            return format_mcp_result(result)
        except Exception as e:
            logger.error(f"MCP tool failed: {e}")
            return f"Tool error: {e}"

    return f"Unknown tool: {name}"


async def process_message(
    user_message: str,
    context: AgentContext
) -> AgentResponse:
    """
    Process a user message and generate a response.

    Args:
        user_message: The user's message
        context: Agent context with user/chat info

    Returns:
        Agent response with content and metadata
    """
    config = get_config()
    client = _get_client()

    # Initialize response metadata
    memories_retrieved = 0
    rag_results = 0
    tool_calls_made = []

    # Build system prompt with additional context
    system_parts = [SYSTEM_PROMPT]

    # 1. Retrieve relevant memories
    if is_memory_enabled():
        try:
            memories = await search_memory(user_message, context.user_id)
            if memories:
                memories_retrieved = len(memories)
                memory_context = build_memory_context(memories)
                system_parts.append(memory_context)
                logger.info(f"Retrieved {memories_retrieved} memories")
        except Exception as e:
            logger.error(f"Memory retrieval failed: {e}")

    # 2. Retrieve RAG context (if appropriate)
    if config.rag.enabled and should_use_rag(user_message):
        try:
            rag_response = await retrieve(user_message, chat_id=context.chat_id)
            if rag_response.results:
                rag_results = len(rag_response.results)
                rag_context = build_context_string(rag_response.results)
                system_parts.append(rag_context)
                logger.info(f"Retrieved {rag_results} RAG results")
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")

    # Combined system prompt
    system_prompt = "\n\n".join(system_parts)

    # 3. Build messages list from conversation history
    messages = []
    history = get_session_history(context.session_id, config.app.max_history_messages)
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    # 4. Add current message
    messages.append({"role": "user", "content": user_message})

    # 5. Get all available tools
    tools = _get_all_tools()

    logger.info(f"Calling Claude with {len(tools)} tools")

    # 6. Call Anthropic
    response = client.messages.create(
        model=config.ai.model,
        max_tokens=config.ai.max_tokens,
        system=system_prompt,
        messages=messages,
        tools=tools if tools else [],
    )

    # 7. Handle tool calls in a loop
    while response.stop_reason == "tool_use":
        # Extract text and tool_use blocks from assistant response
        assistant_content = response.content

        # Add assistant message
        messages.append({"role": "assistant", "content": assistant_content})

        # Execute each tool call and collect results
        tool_results = []
        for block in assistant_content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_args = block.input
                tool_id = block.id

                logger.info(f"Tool call: {tool_name}({tool_args})")
                tool_calls_made.append({"name": tool_name, "args": tool_args})

                # Execute the tool
                tool_result = await _execute_tool(tool_name, tool_args, context)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": tool_result,
                })

        # Add tool results as a user message (Anthropic format)
        messages.append({"role": "user", "content": tool_results})

        # Continue the conversation
        response = client.messages.create(
            model=config.ai.model,
            max_tokens=config.ai.max_tokens,
            system=system_prompt,
            messages=messages,
            tools=tools if tools else [],
        )

    # Extract final text content
    content = ""
    for block in response.content:
        if hasattr(block, "text"):
            content += block.text

    if not content:
        content = "I encountered an error processing your request."

    # 8. Store conversation in database
    add_message(context.session_id, "user", user_message)
    add_message(context.session_id, "assistant", content)

    # 9. Store new memories (async, don't wait)
    if is_memory_enabled():
        asyncio.create_task(_store_memories(user_message, content, context))

    return AgentResponse(
        content=content,
        tool_calls=tool_calls_made,
        memories_retrieved=memories_retrieved,
        rag_results=rag_results,
    )


async def _store_memories(user_message: str, assistant_response: str, context: AgentContext) -> None:
    """Store memories from the conversation (async background task)."""
    try:
        await add_memory(
            [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response}
            ],
            context.user_id
        )
    except Exception as e:
        logger.error(f"Failed to store memories: {e}")
