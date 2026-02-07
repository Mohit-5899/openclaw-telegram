"""
Telegram Action Tools

Provides Telegram API operations as tools for the AI agent.
Mirrors the functionality of Slack-ClawdBot's slack-actions.ts.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from telegram import Bot
from telegram.error import TelegramError

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger("telegram-actions")


@dataclass
class TelegramUser:
    """Telegram user info."""
    id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    is_bot: bool


@dataclass
class TelegramChat:
    """Telegram chat info."""
    id: int
    type: str  # 'private', 'group', 'supergroup', 'channel'
    title: Optional[str]
    username: Optional[str]


@dataclass
class TelegramMessage:
    """Telegram message info."""
    message_id: int
    chat_id: int
    user_id: Optional[int]
    text: Optional[str]
    date: datetime


# Bot instance (set during initialization)
_bot: Optional[Bot] = None


def set_bot(bot: Bot) -> None:
    """Set the bot instance for API calls."""
    global _bot
    _bot = bot


def _get_bot() -> Bot:
    """Get the bot instance."""
    if _bot is None:
        raise RuntimeError("Bot not initialized. Call set_bot() first.")
    return _bot


# ============================================
# User Operations
# ============================================

async def get_user_info(user_id: int) -> Optional[TelegramUser]:
    """
    Get user info by ID.
    Note: Telegram API requires prior interaction to get user info.
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        User info or None if not found
    """
    try:
        bot = _get_bot()
        # Telegram doesn't have a direct getUser API like Slack
        # We can only get user info from chat or messages
        chat = await bot.get_chat(user_id)
        
        return TelegramUser(
            id=chat.id,
            username=chat.username,
            first_name=chat.first_name or "",
            last_name=chat.last_name,
            is_bot=False,
        )
    except TelegramError as e:
        logger.error(f"Failed to get user info for {user_id}: {e}")
        return None


async def get_chat_info(chat_id: int) -> Optional[TelegramChat]:
    """
    Get chat/channel info by ID.
    
    Args:
        chat_id: Telegram chat ID
    
    Returns:
        Chat info or None if not found
    """
    try:
        bot = _get_bot()
        chat = await bot.get_chat(chat_id)
        
        return TelegramChat(
            id=chat.id,
            type=chat.type,
            title=chat.title,
            username=chat.username,
        )
    except TelegramError as e:
        logger.error(f"Failed to get chat info for {chat_id}: {e}")
        return None


# ============================================
# Message Operations
# ============================================

async def send_message(
    chat_id: int,
    text: str,
    reply_to_message_id: Optional[int] = None,
    parse_mode: str = "Markdown"
) -> Optional[TelegramMessage]:
    """
    Send a message to a chat.
    
    Args:
        chat_id: Target chat ID
        text: Message text
        reply_to_message_id: Optional message to reply to
        parse_mode: Markdown or HTML
    
    Returns:
        Sent message info or None on error
    """
    try:
        bot = _get_bot()
        
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            parse_mode=parse_mode,
        )
        
        logger.info(f"Sent message to {chat_id}")
        
        return TelegramMessage(
            message_id=message.message_id,
            chat_id=message.chat_id,
            user_id=message.from_user.id if message.from_user else None,
            text=message.text,
            date=message.date,
        )
    except TelegramError as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return None


async def send_direct_message(
    user_id: int,
    text: str,
    parse_mode: str = "Markdown"
) -> Optional[TelegramMessage]:
    """
    Send a direct message to a user.
    Note: User must have started a conversation with the bot first.
    
    Args:
        user_id: Target user ID
        text: Message text
        parse_mode: Markdown or HTML
    
    Returns:
        Sent message info or None on error
    """
    return await send_message(user_id, text, parse_mode=parse_mode)


async def reply_to_message(
    chat_id: int,
    message_id: int,
    text: str,
    parse_mode: str = "Markdown"
) -> Optional[TelegramMessage]:
    """
    Reply to a specific message (thread reply).
    
    Args:
        chat_id: Chat ID
        message_id: Message ID to reply to
        text: Reply text
        parse_mode: Markdown or HTML
    
    Returns:
        Sent message info or None on error
    """
    return await send_message(chat_id, text, reply_to_message_id=message_id, parse_mode=parse_mode)


async def edit_message(
    chat_id: int,
    message_id: int,
    text: str,
    parse_mode: str = "Markdown"
) -> bool:
    """
    Edit an existing message.
    
    Args:
        chat_id: Chat ID
        message_id: Message ID to edit
        text: New text
        parse_mode: Markdown or HTML
    
    Returns:
        True if successful
    """
    try:
        bot = _get_bot()
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode,
        )
        logger.info(f"Edited message {message_id} in {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to edit message: {e}")
        return False


async def delete_message(chat_id: int, message_id: int) -> bool:
    """
    Delete a message.
    
    Args:
        chat_id: Chat ID
        message_id: Message ID to delete
    
    Returns:
        True if successful
    """
    try:
        bot = _get_bot()
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Deleted message {message_id} in {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to delete message: {e}")
        return False


async def forward_message(
    from_chat_id: int,
    to_chat_id: int,
    message_id: int
) -> Optional[TelegramMessage]:
    """
    Forward a message to another chat.
    
    Args:
        from_chat_id: Source chat ID
        to_chat_id: Target chat ID
        message_id: Message ID to forward
    
    Returns:
        Forwarded message info or None on error
    """
    try:
        bot = _get_bot()
        message = await bot.forward_message(
            chat_id=to_chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
        )
        
        logger.info(f"Forwarded message {message_id} from {from_chat_id} to {to_chat_id}")
        
        return TelegramMessage(
            message_id=message.message_id,
            chat_id=message.chat_id,
            user_id=message.from_user.id if message.from_user else None,
            text=message.text,
            date=message.date,
        )
    except TelegramError as e:
        logger.error(f"Failed to forward message: {e}")
        return None


# ============================================
# Chat Administration
# ============================================

async def get_chat_member_count(chat_id: int) -> int:
    """
    Get the number of members in a chat.
    
    Args:
        chat_id: Chat ID
    
    Returns:
        Member count or 0 on error
    """
    try:
        bot = _get_bot()
        count = await bot.get_chat_member_count(chat_id)
        return count
    except TelegramError as e:
        logger.error(f"Failed to get member count: {e}")
        return 0


async def get_chat_administrators(chat_id: int) -> list[TelegramUser]:
    """
    Get list of administrators in a chat.
    
    Args:
        chat_id: Chat ID
    
    Returns:
        List of admin users
    """
    try:
        bot = _get_bot()
        admins = await bot.get_chat_administrators(chat_id)
        
        return [
            TelegramUser(
                id=admin.user.id,
                username=admin.user.username,
                first_name=admin.user.first_name,
                last_name=admin.user.last_name,
                is_bot=admin.user.is_bot,
            )
            for admin in admins
        ]
    except TelegramError as e:
        logger.error(f"Failed to get administrators: {e}")
        return []


async def pin_message(chat_id: int, message_id: int, disable_notification: bool = False) -> bool:
    """
    Pin a message in a chat.
    
    Args:
        chat_id: Chat ID
        message_id: Message ID to pin
        disable_notification: Whether to send notification
    
    Returns:
        True if successful
    """
    try:
        bot = _get_bot()
        await bot.pin_chat_message(
            chat_id=chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        )
        logger.info(f"Pinned message {message_id} in {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to pin message: {e}")
        return False


async def unpin_message(chat_id: int, message_id: Optional[int] = None) -> bool:
    """
    Unpin a message or all messages in a chat.
    
    Args:
        chat_id: Chat ID
        message_id: Specific message to unpin, or None for most recent
    
    Returns:
        True if successful
    """
    try:
        bot = _get_bot()
        if message_id:
            await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
        else:
            await bot.unpin_chat_message(chat_id=chat_id)
        logger.info(f"Unpinned message in {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to unpin message: {e}")
        return False


# ============================================
# Bot Info
# ============================================

async def get_bot_info() -> Optional[TelegramUser]:
    """
    Get information about the bot itself.
    
    Returns:
        Bot user info
    """
    try:
        bot = _get_bot()
        me = await bot.get_me()
        
        return TelegramUser(
            id=me.id,
            username=me.username,
            first_name=me.first_name,
            last_name=me.last_name,
            is_bot=me.is_bot,
        )
    except TelegramError as e:
        logger.error(f"Failed to get bot info: {e}")
        return None


# ============================================
# Tool Definitions for OpenAI
# ============================================

TELEGRAM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "send_message",
            "description": "Send a message to a Telegram chat or user",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID to send the message to"
                    },
                    "text": {
                        "type": "string",
                        "description": "The message text to send"
                    }
                },
                "required": ["chat_id", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_info",
            "description": "Get information about a Telegram user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The user ID to get info for"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_chat_info",
            "description": "Get information about a Telegram chat or group",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID to get info for"
                    }
                },
                "required": ["chat_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_chat_member_count",
            "description": "Get the number of members in a Telegram group or channel",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID to count members for"
                    }
                },
                "required": ["chat_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_chat_administrators",
            "description": "Get the list of administrators in a Telegram group",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID to get admins for"
                    }
                },
                "required": ["chat_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forward_message",
            "description": "Forward a message from one chat to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_chat_id": {
                        "type": "integer",
                        "description": "The source chat ID"
                    },
                    "to_chat_id": {
                        "type": "integer",
                        "description": "The target chat ID"
                    },
                    "message_id": {
                        "type": "integer",
                        "description": "The message ID to forward"
                    }
                },
                "required": ["from_chat_id", "to_chat_id", "message_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pin_message",
            "description": "Pin a message in a Telegram chat",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID"
                    },
                    "message_id": {
                        "type": "integer",
                        "description": "The message ID to pin"
                    }
                },
                "required": ["chat_id", "message_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unpin_message",
            "description": "Unpin a message in a Telegram chat",
            "parameters": {
                "type": "object",
                "properties": {
                    "chat_id": {
                        "type": "integer",
                        "description": "The chat ID"
                    },
                    "message_id": {
                        "type": "integer",
                        "description": "Optional specific message ID to unpin"
                    }
                },
                "required": ["chat_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_reminder",
            "description": "Schedule a reminder to be sent at a specific time. Use natural language like 'in 5 minutes', 'tomorrow at 9am', etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_text": {
                        "type": "string",
                        "description": "The reminder message"
                    },
                    "time_expression": {
                        "type": "string",
                        "description": "When to send the reminder (e.g., 'in 5 minutes', 'tomorrow at 9am', 'at 3pm')"
                    }
                },
                "required": ["reminder_text", "time_expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_reminders",
            "description": "List all scheduled reminders for the current user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_reminder",
            "description": "Cancel a scheduled reminder by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_id": {
                        "type": "integer",
                        "description": "The reminder ID to cancel"
                    }
                },
                "required": ["reminder_id"]
            }
        }
    }
]
