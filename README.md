# Lean Agent Swarm

A distributed, Redis-backed agentic framework for Automated Theorem Proving (ATP) using Lean 4 and LLMs.

## Overview
`lean-agent-swarm` provides the orchestration layer for managing fleets of autonomous agents running on HPC clusters (via Slurm). The framework allows an LLM "Planner" to generate a sequence of mathematical tasks (e.g., Lean 4 lemmas) and dispatch them to a queue. A fleet of independent Slurm workers (the "Provers") continuously consume these tasks, interact with a centralized LLM endpoint (like `leanstral-1.5` hosted via `slurm-litellm-vllm`), and rigorously verify the proofs using the local Lean 4 compiler.

## Quickstart

1. **Start the Message Broker (Redis):**
   ```bash
   ./bin/start_redis.sh
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Planner:**
   Generate the JSON task array and populate the queue.
   ```bash
   ./bin/run_planner.sh
   ```

4. **Launch the Prover Fleet:**
   In a production environment, submit a Slurm job array. For local testing:
   ```bash
   ./bin/run_worker.sh
   ```

## Documentation
Full documentation is available in the `docs/` directory and is built using [Docsify](https://docsify.js.org/).

## Architecture
See the `docs/` for an in-depth explanation of the decoupled task queuing system, the Redis JSON schema, and the continuous feedback loop between the LLM and the Lean 4 compiler.
