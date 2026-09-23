import argparse
from task_queue import TaskQueue

def main():
    parser = argparse.ArgumentParser(description="Generate and push tasks to Redis")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    args = parser.parse_args()

    queue = TaskQueue(host=args.host, port=args.port)
    
    # Dummy tasks mapping to the SU(3) framework
    tasks = [
        {
            "task_id": "su3_generator_1",
            "dependencies": [],
            "context": "import Mathlib.Algebra.Lie\n\n-- Define Gell-Mann matrices",
            "statement": "theorem gell_mann_1_commute_2 : commutator T1 T2 = i * T3",
            "max_retries": 3
        },
        {
            "task_id": "su3_generator_2",
            "dependencies": [],
            "context": "import Mathlib.Algebra.Lie\n\n-- Define Gell-Mann matrices",
            "statement": "theorem gell_mann_4_commute_5 : commutator T4 T5 = i * (T3 + sqrt 3 * T8) / 2",
            "max_retries": 3
        }
    ]

    print(f"Pushing {len(tasks)} tasks to pending queue...")
    for task in tasks:
        tid = queue.push_task(task)
        print(f"Pushed task: {tid}")

    print("Current queue sizes:", queue.get_queue_sizes())

if __name__ == "__main__":
    main()
