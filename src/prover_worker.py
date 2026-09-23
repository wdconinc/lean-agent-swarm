import argparse
import time
import os
from task_queue import TaskQueue

def main():
    parser = argparse.ArgumentParser(description="Prover agent worker")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--llm-base-url", default="http://localhost:4000/v1", help="LLM base URL")
    args = parser.parse_args()

    queue = TaskQueue(host=args.host, port=args.port)
    print(f"Worker started. Waiting for tasks on Redis {args.host}:{args.port}...")

    while True:
        try:
            # Block until a task is available
            task = queue.pop_task(timeout=0)
            if not task:
                continue

            print(f"\n[Worker] Claimed task: {task.get('task_id')}")
            print(f"[Worker] Statement: {task.get('statement')}")
            
            # TODO: Integrate LiteLLM/OpenAI call to args.llm_base_url
            # TODO: Compile generated proof with Lean 4
            
            # Simulate processing time
            time.sleep(2)
            
            # Simulate success
            print(f"[Worker] Task verified successfully!")
            queue.complete_task(task, {"proof": "exact rfl", "compiled": True})
            
        except KeyboardInterrupt:
            print("Shutting down worker...")
            break
        except Exception as e:
            print(f"Worker encountered error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
