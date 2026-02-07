"""
Telegram Bot Setup

Creates and configures the Telegram bot application.
"""

from telegram.ext import Application

from ..utils.logger import get_logger
from ..config import get_config
from .handlers import setup_handlers

logger = get_logger("telegram-bot")


def create_application() -> Application:
    """Create and configure the Telegram bot application."""
    config = get_config()
    
    logger.info("Creating Telegram application...")
    
    # Build the application
    application = Application.builder().token(config.telegram.bot_token).build()
    
    # Set up handlers
    setup_handlers(application)
    
    logger.info("Telegram application created")
    return application


async def run_bot(application: Application) -> None:
    """Run the bot using polling."""
    logger.info("Starting bot polling...")
    
    # Initialize the application
    await application.initialize()
    
    # Start receiving updates
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    logger.info("🚀 Bot is running!")


async def stop_bot(application: Application) -> None:
    """Stop the bot gracefully."""
    logger.info("Stopping bot...")
    
    await application.updater.stop()
    await application.stop()
    await application.shutdown()
    
    logger.info("Bot stopped")
