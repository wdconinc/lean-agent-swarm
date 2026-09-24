import os
import json
from mcp.server.fastmcp import FastMCP
from task_queue import TaskQueue

# Initialize the MCP Server
mcp = FastMCP("Lean Swarm Coordinator")

# Initialize the Redis Queue connection
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
queue = TaskQueue(host=redis_host, port=redis_port)

@mcp.tool()
def dispatch_lemma(statement: str, context: str = "", dependencies: list[str] = None) -> str:
    """
    Dispatch a new Lean 4 lemma to the Slurm compute swarm for distributed proving.
    
    Args:
        statement: The theorem statement (e.g., 'theorem su3_weight : ...').
        context: Any necessary imports or preceding definitions.
        dependencies: A list of task_ids this lemma depends on.
    """
    task = {
        "statement": statement,
        "context": context,
        "dependencies": dependencies or [],
        "max_retries": 3
    }
    task_id = queue.push_task(task)
    return f"Task dispatched successfully to the pending queue. Task ID: {task_id}"

@mcp.tool()
def get_swarm_status() -> str:
    """
    Get the current queue sizes of the distributed swarm (pending, active, completed, failed).
    """
    sizes = queue.get_queue_sizes()
    return json.dumps(sizes, indent=2)

@mcp.tool()
def fetch_task_result(task_id: str) -> str:
    """
    Retrieve the status, proof, or error trace of a specific task by its ID.
    
    Args:
        task_id: The ID of the task to fetch.
    """
    # Search across all queues
    for q_name in [queue.q_completed, queue.q_failed, queue.q_active, queue.q_pending]:
        tasks = queue.redis.lrange(q_name, 0, -1)
        for t_str in tasks:
            t = json.loads(t_str)
            if t.get("task_id") == task_id:
                return json.dumps(t, indent=2)
                
    return f"Task ID {task_id} not found in any queue."

if __name__ == "__main__":
    mcp.run()
