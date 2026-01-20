# Ops Monitoring Skill for Claude Code

**Automate background process monitoring with automatic looping and optional Telegram notifications.**

## Why Use This?

Stop manually checking if your long-running processes are healthy. The ops skill:

- ✅ Runs commands in the background automatically
- ✅ Monitors logs/output at your chosen interval
- ✅ Sends status updates to Telegram (optional)
- ✅ Loops continuously until process completes or fails
- ✅ Detects and reports errors/warnings automatically
- ✅ Works while you do other things - true "set it and forget it"
- 🔥 **SELF-HEALING: Lives inside Claude Code - can analyze errors and fix issues automatically**

## 🚀 The Self-Healing Advantage

**Unlike traditional monitoring tools that just report errors, ops monitoring runs inside Claude Code - an AI that can actually FIX problems.**

### What This Means:

**Traditional Monitoring (Datadog, New Relic, etc.):**
```
❌ Server crashed → Alert sent → You wake up at 3am → Manual investigation → Manual fix
❌ Port already in use → Alert sent → You ssh in → Kill process manually
❌ Dependencies missing → Build fails → Notification → You investigate → You fix
```

**Ops Monitoring in Claude Code:**
```
✅ Server crashed → Claude detects it → Analyzes logs → Identifies root cause → Restarts with fix
✅ Port already in use → Claude finds the PID → Kills conflicting process → Restarts service
✅ Dependencies missing → Claude reads error → Runs npm install → Rebuilds automatically
```

### Real Self-Healing Examples:

**Scenario 1: Dev server crashes due to memory**
- Traditional: Get alert, investigate, add memory limit, restart
- **Ops + Claude Code**: Detects crash pattern → Automatically restarts with `--max-old-space-size=4096` → Notifies you of the fix

**Scenario 2: Port 3000 already in use**
- Traditional: Get alert, ssh in, find process, kill it, restart
- **Ops + Claude Code**: Detects port conflict → Runs `lsof -ti:3000 | xargs kill` → Restarts server → Reports what it did

**Scenario 3: Database connection timeout**
- Traditional: Get alert, check DB status, restart connection pool manually
- **Ops + Claude Code**: Detects DB timeout → Checks if DB is up → Restarts connection → If DB is down, notifies with diagnostic info

**Scenario 4: Build fails due to TypeScript errors**
- Traditional: Get alert, read errors, fix code manually
- **Ops + Claude Code**: Detects TS errors → Reads error messages → Applies fixes automatically → Re-runs build → Reports results

### How Self-Healing Works:

1. **Monitoring detects an issue** (crash, error, warning)
2. **Claude analyzes the problem** using its code understanding
3. **Claude determines if it can auto-fix** (based on error type and context)
4. **Claude applies the fix** (restart with new params, install deps, kill processes, edit configs)
5. **Claude verifies the fix worked** (checks next monitoring iteration)
6. **Claude reports what it did** (to console and Telegram)

You can configure how aggressive the self-healing should be:
- **Passive mode**: Just report issues (like traditional monitoring)
- **Conservative mode**: Auto-fix safe issues (restarts, dependency installs)
- **Aggressive mode**: Auto-fix code issues, config changes, etc.

This is only possible because ops monitoring lives **inside Claude Code** - you have a full AI developer monitoring your processes, not just a dumb alerting system.

## Real-World Use Cases

### 1. Development Server Monitoring

**Problem:** You start `npm run dev` and want to know if it crashes or shows errors, but you're working on other things.

**Solution:**
```bash
/ops
# Command: npm run dev
# Check method: task_output
# Interval: 60
```

**Result:** Get updates every 60 seconds. If the server crashes or shows errors, you're notified immediately via Telegram.

**Time Saved:** No more manual terminal checking. Work on other tasks while monitoring runs automatically.

---

### 2. Long-Running Build Monitoring

**Problem:** Docker builds or compilation takes 20+ minutes. You want to know when it's done or if it fails, without babysitting the terminal.

**Solution:**
```bash
/ops
# Command: docker build -t myapp:latest .
# Check method: task_output
# Interval: 120
```

**Result:** Check every 2 minutes. Get Telegram notification when build completes or fails. No need to stay at your desk.

**Time Saved:** 20+ minutes of freed attention. Get notified on your phone wherever you are.

---

### 3. Test Suite Monitoring

**Problem:** Running a large test suite that takes 10 minutes. Want to catch failures early without watching the entire run.

**Solution:**
```bash
/ops
# Command: pytest tests/ -v
# Check method: task_output
# Interval: 30
```

**Result:** Updates every 30 seconds showing test progress. First failure triggers immediate notification.

**Time Saved:** Catch issues early, fix them, restart tests faster.

---

### 4. Production Log Monitoring

**Problem:** Need to monitor production logs for errors while working on other tasks.

**Solution:**
```bash
/ops
# Command: tail -f /var/log/app/production.log
# Check method: task_output
# Interval: 60
```

**Result:** Scans logs every minute, alerts you to ERROR or WARNING lines via Telegram.

**Time Saved:** Proactive monitoring instead of reactive firefighting.

---

### 5. Database Migration Monitoring

**Problem:** Database migration running on production. Takes 30 minutes. Need to ensure it doesn't fail.

**Solution:**
```bash
/ops
# Command: python manage.py migrate
# Check method: task_output
# Interval: 60
```

**Result:** Updates every minute. Immediate alert if migration fails. Notification when complete.

**Time Saved:** Peace of mind + freed attention to work on other tasks.

---

## Example Output

### Console Output
```
Ops Monitoring - Iteration 3

Status: ✓ Running
Task ID: abc123f
Time Elapsed: ~3 minutes
Process Iterations: 45 completed

Key Findings:
- Process running normally
- 2 WARNING messages detected
- 1 ERROR at iteration 20 (simulated)
- Latest: Iteration 45 at 14:23:15
- Progress: 8 new iterations since last check

Health Status: Good - Process continues after error

Telegram notification sent successfully! ✓

Next check in 30 seconds...
```

### Telegram Notification
```
🔄 Ops Monitoring - Iteration 3

📊 Status: Running ✓
🆔 Task: abc123f
⏱️ Time Elapsed: ~3 min
🔢 Process Iterations: 45

Key Findings:
• Process running normally
• 2 WARNING messages detected
• 1 ERROR at iteration 20 (simulated)
• Latest: Iteration 45 at 14:23:15
• Progress: 8 new iterations since last check

✅ Health: Good - Process continues after error

🔁 Next check in 30 seconds
```

---

## Setup

### Basic Setup (Console Only)

1. Just run the skill:
   ```bash
   /ops
   ```

2. Answer the prompts:
   - Command to run
   - Check method (logs/task_output/custom)
   - Interval in seconds

3. Done! Monitoring starts automatically.

### Advanced Setup (With Telegram Notifications)

#### Step 1: Create a Telegram Bot

1. Open Telegram and chat with [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow the prompts to create your bot
4. **Save the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Step 2: Get Your Chat ID

**Option A: Using your bot**
1. Start a chat with your bot
2. Send any message (e.g., "hello")
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find `"chat":{"id":123456789}` in the JSON
5. That number is your chat ID

**Option B: Using @userinfobot**
1. Chat with [@userinfobot](https://t.me/userinfobot)
2. It will send you your user ID
3. That's your chat ID

#### Step 3: Set Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
export TELEGRAM_CHAT_ID="123456789"
```

Reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

#### Step 4: Install Python Dependencies

```bash
pip install -r /home/james/.claude/skills/ops/requirements.txt
```

Or manually:
```bash
pip install requests
```

#### Step 5: Test Telegram Integration

```bash
python3 /home/james/.claude/skills/ops/telegram_notifier.py "Hello from ops skill!"
```

You should receive the message on Telegram!

#### Step 6: Start Monitoring

```bash
/ops
```

Telegram notifications will now be sent automatically after each check!

---

## Productivity Benefits

### Before Ops Skill
- ❌ Start long process
- ❌ Watch terminal for 20 minutes
- ❌ Or switch tasks and forget to check back
- ❌ Miss errors that happened 10 minutes ago
- ❌ Waste time context-switching

### After Ops Skill
- ✅ Start long process with `/ops`
- ✅ Switch to other work immediately
- ✅ Get updates on your phone via Telegram
- ✅ Errors reported as they happen
- ✅ No context switching needed
- ✅ Work on multiple things simultaneously

**Time Savings Example:**
- 5 builds per day × 15 minutes each = 75 minutes of "babysitting" time
- With ops skill: 0 minutes of watching, instant notifications
- **Result: 75 minutes saved daily = 6.25+ hours saved per week**

---

## Advanced Features

### Custom Check Commands

Monitor anything by running custom check commands:

```bash
/ops
# Command: ./my_long_script.sh
# Check method: custom
# Custom command: grep -i error /tmp/script.log | tail -5
# Interval: 45
```

### Log File Monitoring

Point directly at log files:

```bash
/ops
# Command: npm start
# Check method: logs
# Log path: ./logs/app.log
# Interval: 30
```

### Multiple Processes

Run multiple monitoring sessions in parallel:
```bash
# Terminal 1: Monitor API server
/ops command="npm run api" interval=60

# Terminal 2: Monitor background jobs
/ops command="python worker.py" interval=120

# Terminal 3: Monitor database
/ops command="tail -f /var/log/postgresql/postgresql.log" interval=90
```

Each sends separate Telegram notifications!

---

## Configuration Options

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `command` | Command to run in background | (required) | `npm run dev` |
| `check_method` | How to check status | `task_output` | `logs`, `task_output`, `custom` |
| `interval` | Seconds between checks | 30 | `60`, `120`, `300` |
| `iterations` | Number of loops (or "continuous") | continuous | `10`, `continuous` |
| `log_path` | Path to log file (if check_method=logs) | (auto-detect) | `./logs/app.log` |
| `custom_command` | Custom check command (if check_method=custom) | - | `grep ERROR logs/app.log` |

---

## Stopping Monitoring

The monitoring will automatically stop if:
- The background process terminates
- Critical errors are detected
- You've reached the iteration limit (if set)

To manually stop:
- Press Ctrl+C to interrupt the current iteration
- The loop won't continue to the next iteration

---

## Troubleshooting

### Telegram notifications not working?

**Check environment variables:**
```bash
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID
```

If empty, they're not set. Re-run Step 3 above.

**Test the notifier directly:**
```bash
python3 /home/james/.claude/skills/ops/telegram_notifier.py
```

Should output: `Telegram is configured and ready!`

**Check Python dependencies:**
```bash
pip install requests
```

### Process not running?

**Check task status:**
```bash
/tasks
```

Look for your task ID. If it shows "completed" or "failed", the process has stopped.

**Check the command:**
Make sure the command works when run manually first.

### No output being captured?

Some commands buffer output. Add flush flags:
- Python: `python -u script.py`
- Node: Use `console.log` which auto-flushes
- General: Pipe through `stdbuf -o0`

---

## Tips for Maximum Productivity

1. **Set Telegram notifications** - Get updates on your phone, work from anywhere
2. **Use longer intervals for stable processes** - 120+ seconds for builds, 30-60 for dev servers
3. **Monitor multiple things at once** - Run several `/ops` sessions in different Claude Code instances
4. **Create shell aliases** for common monitoring tasks:
   ```bash
   alias monitor-api='/ops command="npm run api" interval=60'
   alias monitor-tests='/ops command="pytest" interval=45'
   ```
5. **Use custom check commands** to filter noise - only show ERRORs or specific patterns

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  /ops skill invocation                      │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  1. Run command in background (first time)  │
│     OR reuse existing task_id               │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  2. Sleep for <interval> seconds            │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  3. Check status (logs/task_output/custom)  │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  4. Analyze output (errors/warnings/status) │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  5. Report to console                       │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  6. Send to Telegram (if configured)        │
│     via telegram_notifier.py                │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  7. Loop: Invoke /ops again with same       │
│     parameters + incremented iteration      │
└─────────────────────────────────────────────┘
```

---

## Files

- `SKILL.md` - Main skill instructions for Claude
- `telegram_notifier.py` - Python script for Telegram integration
- `requirements.txt` - Python dependencies (requests)
- `README.md` - This file

---

## Contributing

Have ideas for improvements? Want to add more check methods or notification channels?

File an issue or submit a PR at the Claude Code repository.

---

## License

Part of Claude Code by Anthropic.

---

## FAQ

**Q: Can I monitor multiple processes at once?**
A: Yes! Run `/ops` in different Claude Code sessions or terminals. Each monitors independently and sends separate Telegram notifications.

**Q: Does this work on Windows?**
A: The skill is designed for Unix-like systems (Linux, macOS). Windows support via WSL should work.

**Q: Can I use other notification services besides Telegram?**
A: Currently only Telegram is supported. The architecture makes it easy to add more (Discord, Slack, email, etc.) - contributions welcome!

**Q: What if my process doesn't produce output?**
A: Use `check_method="custom"` and write a custom check command that verifies your process is healthy (e.g., curl an endpoint, check a file, query a database).

**Q: Can I change the interval mid-monitoring?**
A: Not currently. Stop the current monitoring (Ctrl+C) and restart with the new interval.

**Q: Does this consume a lot of API tokens?**
A: Minimal! Each check is a simple tool call. Most of the time is spent sleeping (which consumes nothing).

**Q: Can I export monitoring history?**
A: The background task output is saved to a file. You can read it with:
```bash
cat /tmp/claude/-home-james-Documents-Projects-njamez-ops-skill/tasks/<task_id>.output
```

---

## Get Started Now

```bash
/ops
```

That's it. Start monitoring smarter, not harder.
