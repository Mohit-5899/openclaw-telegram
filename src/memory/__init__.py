"""Memory module - Database and mem0 integration."""

from .database import (
    init_database,
    close_database,
    get_or_create_session,
    add_message,
    get_session_history,
    clear_session_history,
    create_scheduled_task,
    get_pending_tasks,
    update_task_status,
    get_user_tasks,
    cancel_task,
)
from .mem0_client import (
    initialize_memory,
    add_memory,
    search_memory,
    get_all_memories,
    delete_all_memories,
    build_memory_context,
    is_memory_enabled,
)

__all__ = [
    # Database
    "init_database",
    "close_database",
    "get_or_create_session",
    "add_message",
    "get_session_history",
    "clear_session_history",
    "create_scheduled_task",
    "get_pending_tasks",
    "update_task_status",
    "get_user_tasks",
    "cancel_task",
    # mem0
    "initialize_memory",
    "add_memory",
    "search_memory",
    "get_all_memories",
    "delete_all_memories",
    "build_memory_context",
    "is_memory_enabled",
]
