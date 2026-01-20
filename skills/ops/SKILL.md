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
- **telegram_enabled**: Whether to send Telegram notifications (optional, auto-detected from env vars)
- **healing_mode**: Self-healing aggressiveness (options: "passive", "conservative", "aggressive", default: "conservative")
  - passive: Only report issues, no auto-fixing
  - conservative: Auto-fix safe issues (restarts, kill processes, install dependencies)
  - aggressive: Auto-fix code issues, config changes, everything possible

## Telegram Notifications (Optional)

The skill supports sending status reports via Telegram. This is completely optional and requires:

- **TELEGRAM_BOT_TOKEN**: Environment variable with your bot token from @BotFather
- **TELEGRAM_CHAT_ID**: Environment variable with your chat ID (get from @userinfobot)

If these environment variables are set, the skill will automatically send status updates to Telegram after each check. If not set, monitoring continues normally without Telegram notifications.

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
   - If Telegram is configured (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars are set), send the status report to Telegram as well

4b. **Self-Healing (if enabled)**: After analyzing the output, use your capabilities as Claude Code to fix issues automatically:
   - **Passive mode**: Only report issues, never auto-fix
   - **Conservative mode** (default): Auto-fix safe, reversible issues:
     - Process crashed → Restart it
     - Port already in use → Kill conflicting process and restart
     - Missing dependencies → Run package manager install command
     - Disk space full in /tmp → Clean up temp files
     - Memory errors → Restart with increased memory limits
   - **Aggressive mode**: Fix everything you can:
     - All conservative fixes PLUS:
     - TypeScript/compilation errors → Read errors, fix code, rebuild
     - Configuration issues → Update config files
     - Database connection issues → Restart connections, check DB health
     - Test failures → Analyze failures, fix code, re-run tests

   **Important self-healing guidelines:**
   - Always report what you're about to do before doing it
   - Verify the fix worked in the next iteration
   - If a fix fails 3 times, stop auto-fixing and alert the user
   - Never make destructive changes (delete data, drop tables, etc.) even in aggressive mode
   - Always notify the user of fixes via Telegram (if configured)

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

### Telegram Notifications Implementation

To send Telegram notifications after each check:
1. Check if Telegram is configured by running: `python3 /home/james/.claude/skills/ops/telegram_notifier.py` (without arguments)
2. If configured, send status report using: `python3 /home/james/.claude/skills/ops/telegram_notifier.py "Your status message here"`
3. Format the message with:
   - Iteration number
   - Process status (running/stopped)
   - Key findings (errors, warnings)
   - Timestamp
4. Use Markdown formatting in messages for better readability

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
