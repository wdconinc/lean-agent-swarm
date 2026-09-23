# Architecture

The system consists of four core components communicating via Redis.

1. **Planner LLM Agent**: Generates tasks and pushes them to Redis.
2. **Redis Server**: The message broker containing queues (`queue:pending`, `queue:active`, `queue:completed`, `queue:failed`).
3. **Prover Agent Fleet (Slurm Array Jobs)**: Pops tasks, queries the LLM API, and verifies with local Lean 4 compiler.
4. **Result Aggregator**: Collects proven lemmas and stitches them together.

## Task JSON Schema

```json
{
  "task_id": "lemma_su3_weight_1",
  "dependencies": ["def_su3_generators", "lemma_commutation_base"],
  "context": "import Mathlib.Algebra.Lie... \n\n -- Prior definitions...",
  "statement": "theorem su3_weight_1 (x : \u211d) : ...",
  "max_retries": 5,
  "status": "pending"
}
```
