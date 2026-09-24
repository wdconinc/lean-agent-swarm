# Usage

To run the framework locally:

1. **Start Redis:**
```bash
./bin/start_redis.sh
```

2. **Run the Planner:**
```bash
./bin/run_planner.sh
```

3. **(Optional) Run the MCP Server:**
Expose the swarm orchestration API to Claude Desktop or Cursor:
```bash
./bin/run_mcp_server.sh
```

4. **Run the Worker:**
```bash
./bin/run_worker.sh
```
