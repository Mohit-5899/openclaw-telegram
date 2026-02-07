"""
Telegram ClawdBot - Main Entry Point

AI-powered Telegram assistant with RAG, Memory, and MCP integration.
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from src.config import load_config, get_config
from src.utils.logger import setup_logging, get_logger
from src.memory.database import init_database, close_database
from src.memory.mem0_client import initialize_memory
from src.rag import init_vectorstore, start_indexer, stop_indexer
from src.mcp import initialize_mcp, shutdown_mcp
from src.tools.scheduler import task_scheduler
from src.tools.telegram_actions import set_bot
from src.bot.telegram_bot import create_application, stop_bot


# Global application reference for shutdown
_application = None


async def main():
    """Main entry point."""
    global _application
    
    print("=" * 50)
    print("Starting Telegram ClawdBot")
    print("=" * 50)
    
    try:
        # 1. Load configuration
        config = load_config()
        
        # 2. Set up logging
        setup_logging(level=config.app.log_level)
        logger = get_logger("main")
        
        logger.info("Configuration loaded")
        
        # 3. Initialize database
        logger.info("Initializing database...")
        init_database()
        
        # 4. Initialize RAG if enabled
        if config.rag.enabled:
            logger.info("Initializing RAG system...")
            init_vectorstore()
            start_indexer()
        
        # 5. Initialize Memory if enabled
        if config.memory.enabled and config.memory.api_key:
            logger.info("Initializing Memory system...")
            await initialize_memory()
        
        # 6. Initialize MCP if configured
        if config.mcp.github_token or config.mcp.notion_token:
            logger.info("Initializing MCP servers...")
            await initialize_mcp()
        
        # 7. Start task scheduler
        logger.info("Starting task scheduler...")
        task_scheduler.start()
        
        # Set up scheduler callback for sending messages
        async def send_reminder(chat_id: int, message: str):
            if _application:
                await _application.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="Markdown"
                )
        
        task_scheduler.set_message_callback(send_reminder)
        
        # 8. Create and run bot
        logger.info("Creating Telegram bot...")
        _application = create_application()
        
        # Set bot instance for telegram_actions tools
        set_bot(_application.bot)
        
        # Log enabled features
        logger.info("=" * 50)
        logger.info("🚀 Telegram ClawdBot is running!")
        logger.info("=" * 50)
        logger.info(f"  Model: {config.ai.model}")
        logger.info(f"  RAG: {'✅ Enabled' if config.rag.enabled else '❌ Disabled'}")
        logger.info(f"  Memory: {'✅ Enabled' if config.memory.enabled else '❌ Disabled'}")
        logger.info(f"  GitHub MCP: {'✅' if config.mcp.github_token else '❌'}")
        logger.info(f"  Notion MCP: {'✅' if config.mcp.notion_token else '❌'}")
        logger.info("=" * 50)
        
        # Run the bot
        await _application.initialize()
        await _application.start()
        await _application.updater.start_polling(drop_pending_updates=True)
        
        # Keep running until interrupted
        stop_event = asyncio.Event()
        
        def signal_handler():
            stop_event.set()
        
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)
        
        await stop_event.wait()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Failed to start: {e}")
        raise
    finally:
        await shutdown()


async def shutdown():
    """Graceful shutdown."""
    logger = get_logger("main")
    logger.info("Shutting down...")
    
    # Stop bot
    if _application:
        try:
            await _application.updater.stop()
            await _application.stop()
            await _application.shutdown()
        except Exception as e:
            logger.warning(f"Error stopping bot: {e}")
    
    # Stop scheduler
    task_scheduler.stop()
    
    # Stop indexer
    stop_indexer()
    
    # Shutdown MCP
    await shutdown_mcp()
    
    # Close database
    close_database()
    
    logger.info("Goodbye! 👋")


if __name__ == "__main__":
    asyncio.run(main())
