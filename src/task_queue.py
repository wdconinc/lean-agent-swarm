import json
import time
import uuid
from typing import Any

import redis


class TaskQueue:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.q_pending = "queue:pending"
        self.q_active = "queue:active"
        self.q_completed = "queue:completed"
        self.q_failed = "queue:failed"

    def push_task(self, task: dict[str, Any]) -> str:
        """Push a new task to the pending queue."""
        if "task_id" not in task:
            task["task_id"] = str(uuid.uuid4())
        task["status"] = "pending"
        self.redis.rpush(self.q_pending, json.dumps(task))
        return task["task_id"]

    def pop_task(self, timeout: int = 0) -> dict[str, Any] | None:
        """Pop a task from pending and move to active atomically."""
        result = self.redis.brpoplpush(self.q_pending, self.q_active, timeout=timeout)
        if result:
            task = json.loads(result)
            task["status"] = "active"
            task["start_time"] = time.time()
            # Update the task in the active list (atomic brpoplpush doesn't modify the payload)
            # To do this safely, we would need a more complex Redis script, but for now we just
            # return it. The payload in Redis is still the original JSON.
            return task
        return None

    def complete_task(self, task: dict[str, Any], result_data: dict[str, Any]):
        """Mark a task as completed and save results."""
        self._remove_from_active(task)
        task["status"] = "completed"
        task["result"] = result_data
        task["end_time"] = time.time()
        self.redis.rpush(self.q_completed, json.dumps(task))

    def fail_task(self, task: dict[str, Any], error_data: dict[str, Any]):
        """Mark a task as failed after retries."""
        self._remove_from_active(task)
        task["status"] = "failed"
        task["error"] = error_data
        task["end_time"] = time.time()
        self.redis.rpush(self.q_failed, json.dumps(task))

    def retry_task(self, task: dict[str, Any]):
        """Move task back to pending from active."""
        self._remove_from_active(task)
        task["status"] = "pending"
        self.redis.lpush(
            self.q_pending, json.dumps(task)
        )  # Put at the front of the queue

    def _remove_from_active(self, task: dict[str, Any]):
        """Helper to remove the task from the active queue."""
        # Find the exact JSON string to remove
        # In a real production system, you'd use Hashes keyed by task_id for state,
        # and only store task_ids in the queues. But this is simple and effective.
        # We need to remove the original JSON payload that was moved to active.
        # Since we modified the task dict in python, we must be careful.
        # It's better to find by task_id.
        active_tasks = self.redis.lrange(self.q_active, 0, -1)
        for t_str in active_tasks:
            t = json.loads(t_str)
            if t.get("task_id") == task.get("task_id"):
                self.redis.lrem(self.q_active, 1, t_str)
                break

    def get_queue_sizes(self) -> dict[str, int]:
        return {
            "pending": self.redis.llen(self.q_pending),
            "active": self.redis.llen(self.q_active),
            "completed": self.redis.llen(self.q_completed),
            "failed": self.redis.llen(self.q_failed),
        }
