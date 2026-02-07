"""
SQLite Database Module

Handles all persistent storage:
- Sessions: Track conversation sessions per user/chat
- Messages: Store conversation history
- Scheduled Tasks: Reminders and recurring tasks
"""

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..utils.logger import get_logger
from ..config import get_config

logger = get_logger("database")

# Database connection
_connection: Optional[sqlite3.Connection] = None


@dataclass
class Session:
    """Conversation session."""
    id: str
    user_id: int
    chat_id: int
    session_type: str  # 'private', 'group', 'supergroup'
    created_at: int
    last_activity: int


@dataclass
class Message:
    """Stored message."""
    id: int
    session_id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    message_id: Optional[int]
    created_at: int


@dataclass
class ScheduledTask:
    """Scheduled task/reminder."""
    id: int
    user_id: int
    chat_id: int
    task_description: str
    cron_expression: Optional[str]
    scheduled_time: Optional[int]
    status: str  # 'pending', 'running', 'completed', 'failed', 'cancelled'
    created_at: int
    executed_at: Optional[int]


def init_database() -> None:
    """Initialize the database and create tables."""
    global _connection
    
    config = get_config()
    db_path = Path(config.app.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Initializing database at {db_path}")
    
    _connection = sqlite3.connect(str(db_path), check_same_thread=False)
    _connection.row_factory = sqlite3.Row
    
    # Enable foreign keys
    _connection.execute("PRAGMA foreign_keys = ON")
    
    # Create tables
    _connection.executescript("""
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            session_type TEXT NOT NULL DEFAULT 'private',
            created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            last_activity INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
        );
        
        -- Messages table
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            message_id INTEGER,
            created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );
        
        -- Scheduled tasks table
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            task_description TEXT NOT NULL,
            cron_expression TEXT,
            scheduled_time INTEGER,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            executed_at INTEGER
        );
        
        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
        CREATE INDEX IF NOT EXISTS idx_messages_created ON messages(created_at);
        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_chat ON sessions(chat_id);
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_status ON scheduled_tasks(status);
    """)
    
    _connection.commit()
    logger.info("Database initialized successfully")


def close_database() -> None:
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None
        logger.info("Database connection closed")


def _get_connection() -> sqlite3.Connection:
    """Get the database connection."""
    if _connection is None:
        init_database()
    return _connection


# ============================================
# Session Management
# ============================================

def get_or_create_session(user_id: int, chat_id: int, chat_type: str = "private") -> Session:
    """Get or create a session for a user/chat combination."""
    conn = _get_connection()
    
    # Generate session ID based on context
    if chat_type == "private":
        session_id = f"private:{user_id}"
    else:
        session_id = f"group:{chat_id}"
    
    # Check if session exists
    cursor = conn.execute(
        "SELECT * FROM sessions WHERE id = ?",
        (session_id,)
    )
    row = cursor.fetchone()
    
    if row:
        # Update last activity
        conn.execute(
            "UPDATE sessions SET last_activity = strftime('%s', 'now') WHERE id = ?",
            (session_id,)
        )
        conn.commit()
        
        return Session(
            id=row["id"],
            user_id=row["user_id"],
            chat_id=row["chat_id"],
            session_type=row["session_type"],
            created_at=row["created_at"],
            last_activity=row["last_activity"],
        )
    
    # Create new session
    now = int(datetime.now().timestamp())
    conn.execute(
        "INSERT INTO sessions (id, user_id, chat_id, session_type) VALUES (?, ?, ?, ?)",
        (session_id, user_id, chat_id, chat_type)
    )
    conn.commit()
    
    return Session(
        id=session_id,
        user_id=user_id,
        chat_id=chat_id,
        session_type=chat_type,
        created_at=now,
        last_activity=now,
    )


# ============================================
# Message History
# ============================================

def add_message(
    session_id: str,
    role: str,
    content: str,
    message_id: Optional[int] = None
) -> Message:
    """Add a message to the session history."""
    conn = _get_connection()
    
    cursor = conn.execute(
        "INSERT INTO messages (session_id, role, content, message_id) VALUES (?, ?, ?, ?)",
        (session_id, role, content, message_id)
    )
    conn.commit()
    
    now = int(datetime.now().timestamp())
    return Message(
        id=cursor.lastrowid,
        session_id=session_id,
        role=role,
        content=content,
        message_id=message_id,
        created_at=now,
    )


def get_session_history(session_id: str, limit: int = 20) -> list[Message]:
    """Get the message history for a session."""
    conn = _get_connection()
    
    cursor = conn.execute(
        """
        SELECT * FROM messages
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (session_id, limit)
    )
    
    messages = []
    for row in cursor.fetchall():
        messages.append(Message(
            id=row["id"],
            session_id=row["session_id"],
            role=row["role"],
            content=row["content"],
            message_id=row["message_id"],
            created_at=row["created_at"],
        ))
    
    # Return in chronological order (oldest first)
    return list(reversed(messages))


def clear_session_history(session_id: str) -> None:
    """Clear all messages for a session."""
    conn = _get_connection()
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    logger.info(f"Cleared history for session: {session_id}")


# ============================================
# Scheduled Tasks
# ============================================

def create_scheduled_task(
    user_id: int,
    chat_id: int,
    task_description: str,
    scheduled_time: Optional[int] = None,
    cron_expression: Optional[str] = None,
) -> ScheduledTask:
    """Create a new scheduled task."""
    conn = _get_connection()
    
    cursor = conn.execute(
        """
        INSERT INTO scheduled_tasks (user_id, chat_id, task_description, scheduled_time, cron_expression)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, chat_id, task_description, scheduled_time, cron_expression)
    )
    conn.commit()
    
    now = int(datetime.now().timestamp())
    return ScheduledTask(
        id=cursor.lastrowid,
        user_id=user_id,
        chat_id=chat_id,
        task_description=task_description,
        cron_expression=cron_expression,
        scheduled_time=scheduled_time,
        status="pending",
        created_at=now,
        executed_at=None,
    )


def get_pending_tasks() -> list[ScheduledTask]:
    """Get all pending tasks that are due."""
    conn = _get_connection()
    now = int(datetime.now().timestamp())
    
    cursor = conn.execute(
        """
        SELECT * FROM scheduled_tasks
        WHERE status = 'pending'
        AND (scheduled_time IS NULL OR scheduled_time <= ?)
        ORDER BY scheduled_time ASC
        """,
        (now,)
    )
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append(ScheduledTask(
            id=row["id"],
            user_id=row["user_id"],
            chat_id=row["chat_id"],
            task_description=row["task_description"],
            cron_expression=row["cron_expression"],
            scheduled_time=row["scheduled_time"],
            status=row["status"],
            created_at=row["created_at"],
            executed_at=row["executed_at"],
        ))
    
    return tasks


def update_task_status(task_id: int, status: str) -> None:
    """Update the status of a task."""
    conn = _get_connection()
    
    if status in ("completed", "failed"):
        conn.execute(
            "UPDATE scheduled_tasks SET status = ?, executed_at = strftime('%s', 'now') WHERE id = ?",
            (status, task_id)
        )
    else:
        conn.execute(
            "UPDATE scheduled_tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )
    
    conn.commit()


def get_user_tasks(user_id: int) -> list[ScheduledTask]:
    """Get all tasks for a user."""
    conn = _get_connection()
    
    cursor = conn.execute(
        "SELECT * FROM scheduled_tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT 20",
        (user_id,)
    )
    
    tasks = []
    for row in cursor.fetchall():
        tasks.append(ScheduledTask(
            id=row["id"],
            user_id=row["user_id"],
            chat_id=row["chat_id"],
            task_description=row["task_description"],
            cron_expression=row["cron_expression"],
            scheduled_time=row["scheduled_time"],
            status=row["status"],
            created_at=row["created_at"],
            executed_at=row["executed_at"],
        ))
    
    return tasks


def cancel_task(task_id: int, user_id: int) -> bool:
    """Cancel a pending task."""
    conn = _get_connection()
    
    cursor = conn.execute(
        "UPDATE scheduled_tasks SET status = 'cancelled' WHERE id = ? AND user_id = ? AND status = 'pending'",
        (task_id, user_id)
    )
    conn.commit()
    
    return cursor.rowcount > 0
