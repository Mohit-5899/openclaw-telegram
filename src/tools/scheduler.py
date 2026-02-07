"""
Task Scheduler

Handles scheduled reminders and recurring tasks using APScheduler.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from ..utils.logger import get_logger
from ..memory.database import (
    create_scheduled_task,
    get_pending_tasks,
    update_task_status,
    get_user_tasks,
    cancel_task as db_cancel_task,
    ScheduledTask,
)

logger = get_logger("scheduler")


class TaskScheduler:
    """Manages scheduled tasks and reminders."""
    
    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        self._is_running = False
        self._send_message_callback: Optional[Callable] = None
    
    def set_message_callback(self, callback: Callable) -> None:
        """Set the callback for sending reminder messages."""
        self._send_message_callback = callback
    
    def start(self) -> None:
        """Start the scheduler."""
        if self._is_running:
            logger.warning("Scheduler already running")
            return
        
        self._scheduler.start()
        self._is_running = True
        logger.info("Task scheduler started")
        
        # Schedule periodic check for pending tasks
        self._scheduler.add_job(
            self._check_pending_tasks,
            "interval",
            minutes=1,
            id="pending_tasks_check"
        )
    
    def stop(self) -> None:
        """Stop the scheduler."""
        if self._scheduler.running:
            self._scheduler.shutdown()
        self._is_running = False
        logger.info("Task scheduler stopped")
    
    async def schedule_task(
        self,
        user_id: int,
        chat_id: int,
        description: str,
        scheduled_time: Optional[datetime] = None,
        cron_expression: Optional[str] = None,
    ) -> ScheduledTask:
        """
        Schedule a new task.
        
        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            description: Task description
            scheduled_time: One-time schedule
            cron_expression: Recurring schedule
        
        Returns:
            Created task
        """
        logger.info(f"Scheduling task for user {user_id}: {description}")
        
        # Create task in database
        task = create_scheduled_task(
            user_id=user_id,
            chat_id=chat_id,
            task_description=description,
            scheduled_time=int(scheduled_time.timestamp()) if scheduled_time else None,
            cron_expression=cron_expression,
        )
        
        # Schedule the actual job
        if scheduled_time:
            self._scheduler.add_job(
                self._execute_task,
                trigger=DateTrigger(run_date=scheduled_time),
                args=[task.id],
                id=f"task_{task.id}",
            )
        elif cron_expression:
            self._scheduler.add_job(
                self._execute_task,
                trigger=CronTrigger.from_crontab(cron_expression),
                args=[task.id],
                id=f"task_{task.id}",
            )
        
        return task
    
    async def _execute_task(self, task_id: int) -> None:
        """Execute a scheduled task."""
        from ..memory.database import get_user_tasks
        
        # Find the task
        tasks = get_pending_tasks()
        task = next((t for t in get_user_tasks(0) if t.id == task_id), None)
        
        if not task:
            logger.warning(f"Task {task_id} not found")
            return
        
        logger.info(f"Executing task {task_id}: {task.task_description}")
        
        try:
            update_task_status(task_id, "running")
            
            # Send reminder message
            if self._send_message_callback:
                await self._send_message_callback(
                    task.chat_id,
                    f"⏰ *Reminder*: {task.task_description}"
                )
            
            # Mark as completed (unless recurring)
            if not task.cron_expression:
                update_task_status(task_id, "completed")
            else:
                update_task_status(task_id, "pending")
            
            logger.info(f"Task {task_id} executed successfully")
            
        except Exception as e:
            logger.error(f"Failed to execute task {task_id}: {e}")
            update_task_status(task_id, "failed")
    
    async def _check_pending_tasks(self) -> None:
        """Check for pending tasks that are due."""
        tasks = get_pending_tasks()
        
        for task in tasks:
            if task.cron_expression:
                continue  # Cron tasks are handled separately
            
            await self._execute_task(task.id)
    
    def get_user_tasks(self, user_id: int) -> list[ScheduledTask]:
        """Get all tasks for a user."""
        return get_user_tasks(user_id)
    
    def cancel_task(self, task_id: int, user_id: int) -> bool:
        """Cancel a task."""
        # Remove from scheduler
        job_id = f"task_{task_id}"
        job = self._scheduler.get_job(job_id)
        if job:
            job.remove()
        
        return db_cancel_task(task_id, user_id)


# Global scheduler instance
task_scheduler = TaskScheduler()


def parse_relative_time(expression: str) -> Optional[datetime]:
    """
    Parse relative time expressions.
    
    Examples:
        "in 5 minutes" -> datetime 5 minutes from now
        "in 2 hours" -> datetime 2 hours from now
        "tomorrow at 9am" -> datetime for tomorrow 9:00
    
    Returns:
        Parsed datetime or None if not parseable
    """
    now = datetime.now()
    expr = expression.lower().strip()
    
    # Match "in X minutes/hours/days"
    relative_match = re.match(r"in\s+(\d+)\s+(minute|hour|day|week)s?", expr)
    if relative_match:
        amount = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        if unit == "minute":
            return now + timedelta(minutes=amount)
        elif unit == "hour":
            return now + timedelta(hours=amount)
        elif unit == "day":
            return now + timedelta(days=amount)
        elif unit == "week":
            return now + timedelta(weeks=amount)
    
    # Match "tomorrow at HH:MM"
    tomorrow_match = re.match(r"tomorrow\s+at\s+(\d{1,2}):?(\d{2})?\s*(am|pm)?", expr, re.IGNORECASE)
    if tomorrow_match:
        hours = int(tomorrow_match.group(1))
        minutes = int(tomorrow_match.group(2) or "0")
        period = (tomorrow_match.group(3) or "").lower()
        
        if period == "pm" and hours < 12:
            hours += 12
        if period == "am" and hours == 12:
            hours = 0
        
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    
    # Match "at HH:MM"
    at_time_match = re.match(r"at\s+(\d{1,2}):?(\d{2})?\s*(am|pm)?", expr, re.IGNORECASE)
    if at_time_match:
        hours = int(at_time_match.group(1))
        minutes = int(at_time_match.group(2) or "0")
        period = (at_time_match.group(3) or "").lower()
        
        if period == "pm" and hours < 12:
            hours += 12
        if period == "am" and hours == 12:
            hours = 0
        
        target = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        # If time has passed, schedule for tomorrow
        if target <= now:
            target += timedelta(days=1)
        
        return target
    
    return None
