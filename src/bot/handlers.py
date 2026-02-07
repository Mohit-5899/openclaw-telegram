"""
Telegram Bot Handlers

Message and command handlers for the Telegram bot.
"""

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from ..utils.logger import get_logger
from ..config import get_config
from ..agents.agent import process_message, AgentContext
from ..memory.database import (
    get_or_create_session,
    clear_session_history,
    get_user_tasks,
)
from ..memory.mem0_client import is_memory_enabled, delete_all_memories
from ..rag import index_single_message, get_document_count
from ..tools.scheduler import task_scheduler

logger = get_logger("handlers")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    welcome_message = f"""👋 Hello {user.first_name}!

I'm **ClawdBot**, your AI assistant powered by advanced capabilities:

🧠 **Memory**: I remember our conversations
🔍 **RAG**: I can search through chat history
🔧 **Tools**: I can interact with GitHub, Notion, and more

**Commands:**
• `/help` - Show all commands
• `/status` - Check my status
• `/reset` - Clear conversation history
• `/tasks` - View your scheduled tasks

Just send me a message to start chatting!
"""
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_message = """📚 **Available Commands**

**General:**
• `/start` - Welcome message
• `/help` - This help message
• `/status` - Bot status and features

**Conversation:**
• `/reset` - Clear your conversation history
• `/forget` - Delete all my memories about you

**Tasks:**
• `/tasks` - List your scheduled tasks
• `/cancel <id>` - Cancel a task

**Tips:**
• Ask me to remind you about things
• Ask about your GitHub repos or issues
• Query your Notion pages and databases
• I learn from our conversations!
"""
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    config = get_config()
    
    # Get RAG document count
    try:
        doc_count = await get_document_count()
    except:
        doc_count = 0
    
    status_parts = [
        "🤖 **ClawdBot Status**\n",
        f"• Model: `{config.ai.model}`",
        f"• Memory: {'✅ Enabled' if is_memory_enabled() else '❌ Disabled'}",
        f"• RAG: {'✅ Enabled' if config.rag.enabled else '❌ Disabled'}",
    ]
    
    if config.rag.enabled:
        status_parts.append(f"• Indexed Messages: {doc_count}")
    
    # Check MCP servers
    from ..mcp import get_all_tools
    mcp_tools = get_all_tools()
    if mcp_tools:
        status_parts.append(f"• MCP Tools: {len(mcp_tools)} available")
    else:
        status_parts.append("• MCP: Not configured")
    
    await update.message.reply_text("\n".join(status_parts), parse_mode="Markdown")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset command - clear conversation history."""
    user = update.effective_user
    chat = update.effective_chat
    
    session = get_or_create_session(user.id, chat.id, chat.type)
    clear_session_history(session.id)
    
    await update.message.reply_text(
        "🧹 Conversation history cleared! Let's start fresh."
    )


async def forget_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /forget command - delete all memories."""
    user = update.effective_user
    
    if is_memory_enabled():
        success = await delete_all_memories(user.id)
        if success:
            await update.message.reply_text(
                "🧠 I've forgotten everything about you. We're starting completely fresh!"
            )
        else:
            await update.message.reply_text(
                "❌ Failed to clear memories. Please try again."
            )
    else:
        await update.message.reply_text(
            "Memory system is not enabled."
        )


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tasks command - list user's tasks."""
    user = update.effective_user
    tasks = get_user_tasks(user.id)
    
    if not tasks:
        await update.message.reply_text(
            "📋 You don't have any scheduled tasks.\n\nAsk me to remind you about something!"
        )
        return
    
    lines = ["📋 **Your Scheduled Tasks**\n"]
    
    for task in tasks[:10]:
        status_emoji = {
            "pending": "⏳",
            "running": "🔄",
            "completed": "✅",
            "failed": "❌",
            "cancelled": "🚫",
        }.get(task.status, "❓")
        
        lines.append(f"{status_emoji} `#{task.id}`: {task.task_description}")
    
    lines.append("\nUse `/cancel <id>` to cancel a pending task.")
    
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command - cancel a task."""
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(
            "Usage: `/cancel <task_id>`\n\nUse `/tasks` to see your task IDs.",
            parse_mode="Markdown"
        )
        return
    
    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid task ID. Please provide a number.")
        return
    
    if task_scheduler.cancel_task(task_id, user.id):
        await update.message.reply_text(f"✅ Task #{task_id} cancelled.")
    else:
        await update.message.reply_text(
            f"❌ Could not cancel task #{task_id}. It may not exist or already be completed."
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    user = update.effective_user
    chat = update.effective_chat
    message = update.message
    
    if not message or not message.text:
        return
    
    logger.info(f"Message from {user.first_name} ({user.id}): {message.text[:50]}...")
    
    # Get or create session
    session = get_or_create_session(user.id, chat.id, chat.type)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=chat.id, action="typing")
    
    # Index the message for RAG
    config = get_config()
    if config.rag.enabled:
        user_name = user.full_name or user.first_name or "User"
        await index_single_message(
            message_id=message.message_id,
            chat_id=chat.id,
            user_id=user.id,
            user_name=user_name,
            text=message.text,
        )
    
    # Process through AI agent
    try:
        agent_context = AgentContext(
            user_id=user.id,
            chat_id=chat.id,
            session_id=session.id,
            user_name=user.first_name or "User",
            chat_type=chat.type,
        )
        
        response = await process_message(message.text, agent_context)
        
        # Send response
        # Split long messages if needed (Telegram limit is 4096 chars)
        content = response.content
        if len(content) > 4000:
            # Split into chunks
            chunks = [content[i:i+4000] for i in range(0, len(content), 4000)]
            for chunk in chunks:
                await message.reply_text(chunk, parse_mode="Markdown")
        else:
            await message.reply_text(content, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.reply_text(
            "Sorry, I encountered an error. Please try again."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "An error occurred. Please try again."
        )


def setup_handlers(application: Application) -> None:
    """Set up all handlers for the application."""
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("forget", forget_command))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Message handler (must be last)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    ))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("Handlers registered")
