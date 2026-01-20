# Ops Monitoring Skill for Claude Code

A Claude Code skill that enables background process monitoring with automatic looping. Run commands in the background, check their status through logs or task output, and continuously monitor operations.

## Description

This skill transforms Claude into an ops monitoring assistant that can:
- Run commands in the background (user-specified or auto-discovered)
- Monitor logs, task output, or run custom checks periodically
- Loop automatically to provide continuous monitoring
- Intelligently discover commands and log files in your project

Perfect for:
- Monitoring dev servers and watching for errors
- Keeping an eye on long-running builds or tests
- Tracking background jobs and their output
- Automated log analysis and reporting

## Installation

### Quick Install (Recommended)

Run the installer from the repository:

```bash
git clone https://github.com/friday-james/ops-skill.git
cd ops-skill
./install.sh
```

### Manual Install

Copy the skill file directly:

```bash
# Both Linux and macOS:
mkdir -p ~/.claude/skills/ops
cp skills/ops/SKILL.md ~/.claude/skills/ops/
```

Then restart Claude Code to load the skill.

## Usage

Invoke the skill with:
```
/ops
```

Claude will then ask you:
1. What command to run in the background
2. How to check the status (logs, task output, or custom command)
3. How often to check (interval in seconds)

### Example Session

```
You: /ops
Claude: What command should I run in the background?
You: npm run dev

Claude: How should I check the status? (logs/task_output/custom)
You: logs

Claude: Which log file should I monitor? (I can also try to find it)
You: ./logs/app.log

Claude: How often should I check in seconds? (default: 30)
You: 10

Claude: Starting ops monitoring...
[Starts npm run dev in background]
[Waits 10 seconds]
[Checks ./logs/app.log]
[Reports findings]
[Automatically invokes /ops again to continue loop]
```

### Advanced Usage

You can also provide parameters directly:

```
/ops command="python train.py" check_method="logs" log_path="./training.log" interval=60
```

### Smart Discovery

If you want Claude to figure things out:

```
You: /ops
Claude: What command should I run in the background?
You: find it yourself

Claude: [Searches package.json, Makefile, etc.]
I found these options:
- npm run dev (from package.json)
- npm run build (from package.json)
Which one should I use?
```

## Features

### Background Execution
Commands run in the background using Claude's Bash tool with `run_in_background: true`, allowing continuous monitoring without blocking.

### Flexible Monitoring
Three check methods:
- **logs**: Monitor log files for errors, warnings, and important messages
- **task_output**: Check the status of the background task directly
- **custom**: Run your own custom check commands

### Automatic Looping
The skill automatically re-invokes itself after each check, creating a continuous monitoring loop. State is passed between iterations so monitoring continues seamlessly.

### Smart Discovery
- Finds common commands in package.json, Makefiles, shell scripts
- Discovers log files in standard locations
- Suggests likely monitoring targets

### Status Reporting
Each check reports:
- Current iteration number
- Time elapsed since start
- Key findings (errors, warnings, important log messages)
- Process status
- Next check time

## Configuration

### Parameters

- **command**: Command to run in background (e.g., "npm run dev")
- **check_method**: How to check status ("logs", "task_output", or "custom")
- **log_path**: Path to log file (when check_method is "logs")
- **custom_check**: Custom command to run (when check_method is "custom")
- **interval**: Seconds between checks (default: 30)
- **iterations**: Number of loops ("continuous" for infinite, or a number)

### Exit Conditions

Monitoring stops when:
- Background process terminates
- Specified number of iterations complete
- Critical errors detected
- User interrupts

## Examples

### Monitor a Dev Server

```
/ops command="npm run dev" check_method="logs" log_path="./logs/dev.log" interval=15
```

Starts the dev server in the background, checks the log file every 15 seconds, and reports any errors or warnings.

### Monitor a Build Process

```
/ops command="make build" check_method="task_output" interval=5
```

Runs the build in the background and checks task output every 5 seconds to see if it's still running.

### Custom Health Check

```
/ops command="./app" check_method="custom" custom_check="curl -f localhost:3000/health" interval=30
```

Runs your app in the background and performs a health check every 30 seconds.

### Training Job Monitoring

```
/ops command="python train.py --epochs 100" check_method="logs" log_path="./training.log" interval=60
```

Monitors a long-running ML training job, checking the log every minute for progress updates.

## Uninstall

Remove the skill:

```bash
rm -rf ~/.claude/skills/ops/
```

Then restart Claude Code.

## Contributing

Contributions welcome! Feel free to submit PRs to add features like:
- Alert thresholds (notify on specific log patterns)
- Multiple log file monitoring
- Metric extraction and trending
- Integration with monitoring services
- Custom notification methods

## License

MIT License - Use it however you want.

## Tips

- Start with a shorter interval (10-30s) for active development
- Use longer intervals (60s+) for stable processes
- The skill will auto-discover logs if you don't specify a path
- You can interrupt the loop at any time and restart with different parameters
- Use task_output method for processes without log files
- Combine with other Claude Code features for powerful automation

## Troubleshooting

**Skill not found after installation:**
- Make sure you restarted Claude Code
- Check that the file exists at ~/.claude/skills/ops/SKILL.md

**Background command not running:**
- Verify the command works in your terminal first
- Check file paths and permissions
- Look at the task output for error messages

**Logs not being read:**
- Verify the log file path is correct
- Make sure the process actually writes to that log
- Check file permissions

**Loop not continuing:**
- Check if the background process terminated
- Verify no critical errors were detected
- Make sure you're using the latest version of Claude Code
