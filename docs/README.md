# Lean Agent Swarm

Welcome to the documentation for **Lean Agent Swarm**.

This framework provides the orchestration layer for managing fleets of autonomous agents running on HPC clusters (via Slurm). 

* **The Goal**: Distribute and automate formal theorem proving using Lean 4.
* **The Method**: An LLM generates mathematical tasks and queues them in Redis. Independent Slurm workers consume the tasks, request proofs from a centralized LLM (e.g. `leanstral-1.5`), compile them locally with Lean 4, and iterate upon compiler errors.

Please see the sidebar to explore the Architecture and Usage.
