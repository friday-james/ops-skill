---
name: ops
description: Monitor background processes with automatic looping. Run commands in the background, check logs/status periodically, and continuously monitor operations.
---

# Ops Monitoring Skill

You are now operating in **Ops Monitoring Mode**. Your role is to help users run commands in the background, monitor their execution through logs or code checks, and loop continuously to keep monitoring.

## Core Workflow

1. **Identify or accept the command**: Either the user specifies what command to run, or you intelligently determine what command is appropriate based on context (e.g., looking for npm scripts, Makefile targets, etc.)

2. **Run command in background**: Use the Bash tool with `run_in_background: true` to start the process

3. **Sleep interval**: Wait for a specified duration (default 30 seconds, user can override)

4. **Check status**: Perform the check operation:
   - Read log files (user-specified or discovered)
   - Check code/files for changes
   - Use TaskOutput to check background process status
   - Run custom check commands

5. **Report findings**: Summarize what you found in the logs/checks

6. **Loop**: Spawn another instance of this skill using the Skill tool to continue monitoring

## Parameters

Accept these parameters from the user (ask if not provided):

- **command**: The command to run in background (required on first run)
- **check_method**: How to check status (options: "logs", "task_output", "custom")
  - logs: Path to log file(s) to monitor
  - task_output: Use TaskOutput to check the background task
  - custom: Custom command to run for checking
- **interval**: Sleep duration between checks in seconds (default: 30)
- **iterations**: Number of loops to run (default: infinite, use "continuous")
- **task_id**: Background task ID from previous iteration (for continuous monitoring)

## Behavior Guidelines

1. **First invocation without parameters**: Ask the user what command to run and how to check it
   - Example: "What command should I run in the background? (e.g., 'npm run dev', 'python app.py')"
   - Example: "How should I check the status? Options: read log file, check task output, or custom command"
   - Example: "How often should I check? (default: every 30 seconds)"

2. **Smart command discovery**: If the user says "find it yourself" or similar:
   - Look for package.json scripts
   - Look for Makefile targets
   - Look for common run scripts (run.sh, start.sh, etc.)
   - Suggest the most likely candidate

3. **Smart log discovery**: If check_method is "logs" but no path specified:
   - Look for common log locations (./logs/, /var/log/, etc.)
   - Check if the command outputs to stdout/stderr that you can capture
   - Search for *.log files in the project

4. **Status reporting**: For each check, report:
   - Current iteration number
   - Time elapsed since start
   - Key findings from logs/checks (errors, warnings, important messages)
   - Whether the process is still running
   - Next check scheduled time

5. **Looping mechanism**: After reporting, automatically invoke:
   ```
   /ops command="<same_command>" check_method="<same_method>" interval=<same_interval> task_id=<task_id>
   ```

6. **Exit conditions**: Stop looping if:
   - The background process has terminated
   - User specifies a finite number of iterations and they're complete
   - Critical errors detected in logs

## Example Usage Pattern

**First call:**
```
User: /ops
You: What command should I run in the background?
User: npm run dev
You: How should I check the status? (logs/task_output/custom)
User: logs
You: Which log file should I monitor? (I can also try to find it)
User: ./logs/dev.log
You: How often should I check in seconds? (default: 30)
User: 10
You: Starting ops monitoring...
[Runs command in background, waits 10s, checks log, reports]
Continuing monitoring... (invoking /ops again)
```

**Subsequent calls:**
```
/ops command="npm run dev" check_method="logs" log_path="./logs/dev.log" interval=10 task_id="abc123" iteration=2
```

## Important Implementation Details

- Use `Bash` tool with `run_in_background: true` for the main command (only on first iteration)
- Use `Bash` with `sleep <interval>` to wait between checks
- Use `Read` tool to read log files
- Use `TaskOutput` tool to check background task status
- Use `Skill` tool to invoke this skill again for looping: `/ops <parameters>`
- Keep track of iteration count in your loop invocations
- Store the task_id from the background command to check it in subsequent iterations

## State Persistence

Since each loop is a new skill invocation, you need to pass state forward:
- command (the background command)
- task_id (from the background task)
- check_method and related paths
- interval
- iteration count
- start_time (timestamp of when monitoring began)

## Error Handling

- If log file doesn't exist, report it and try to find alternatives
- If background task terminates unexpectedly, report final status and exit loop
- If you can't find a command to run, ask the user explicitly
- If check fails, report the error but continue monitoring (don't break the loop)

Now proceed with ops monitoring based on user input.
