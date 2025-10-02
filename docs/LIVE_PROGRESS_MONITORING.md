# Live Progress Monitoring for Experiments

## Problem Solved

When running experiments in parallel (or even sequentially), each experiment can take 15+ minutes. Previously, you had no visibility into:
- Whether experiments were running or stuck
- How far along each experiment was (turn count, time elapsed)
- Token usage and costs accumulating in real-time
- Which specific step each experiment was on

## Solution: Per-Experiment Progress Files

Each running experiment now creates and continuously updates a progress file at:
```
experiments/progress_XXXXXXXX.txt
```

Where `XXXXXXXX` is the first 8 characters of the experiment ID.

### Progress File Content

Each progress file shows:
```
Experiment ID: 53359e84
Condition: suggestive_autonomy
Model: accounts/fireworks/models/gpt-oss-120b
Last updated: 2025-10-02 08:15:42

Turn: 15 / 100
Time: 8.3 / 15.0 min (55.3%)
[██████████████████████░░░░░░░░░░░░░░░░░░]

Total tokens: 45,234
Total cost: $8.42
API calls: 30
```

**Updates every turn** (typically every 10-30 seconds), so you can see real-time progress!

## Monitoring Options

### Option 1: Python Monitor (Recommended ⭐)

**Best for**: Clean, colored, real-time display

```bash
python3 scripts/monitor_experiments.py
```

**Features:**
- ✅ Color-coded output
- ✅ Formatted display
- ✅ Shows all running experiments
- ✅ Auto-refreshes every 2 seconds
- ✅ Clear screen for easy reading

**Screenshot:**
```
╔═══════════════════════════════════════════════════════════════════╗
║          LIVE EXPERIMENT MONITOR                                  ║
╚═══════════════════════════════════════════════════════════════════╝

Running 3 experiment(s)

═══ Experiment 1 ═══
Experiment ID: 53359e84
Condition: suggestive_autonomy
Model: accounts/fireworks/models/gpt-oss-120b
Last updated: 2025-10-02 08:15:42

Turn: 15 / 100
Time: 8.3 / 15.0 min (55.3%)
[██████████████████████░░░░░░░░░░░░░░░░░░]

Total tokens: 45,234
Total cost: $8.42
API calls: 30

═══ Experiment 2 ═══
[...]
```

### Option 2: Watch All Progress Files

**Best for**: Simple shell-based monitoring

```bash
./scripts/watch_all_progress.sh
```

Uses `watch` command to refresh all progress files every 2 seconds.

### Option 3: Overall Status Only

**Best for**: Just seeing completion count

```bash
./scripts/watch_progress.sh
```

Shows only the overall experiment batch status (which experiments have completed).

### Option 4: Manual Checks

**Check all progress files:**
```bash
cat experiments/progress_*.txt
```

**Watch a specific experiment:**
```bash
tail -f experiments/progress_53359e84.txt
```

**List all progress files:**
```bash
ls -lt experiments/progress_*.txt
```

## Complete Workflow

### Terminal 1: Run Experiments

```bash
./experiment.py \
  --models-file configs/models.txt \
  --conditions-file configs/conditions.txt \
  --duration 15 \
  --parallel \
  --workers 3 \
  --world extended
```

**Output shows:**
```
Running 9 experiments in parallel...

📊 Progress: 0/9 completed (0.0%)
💡 Monitor overall progress: tail -f experiments/current_run_status.txt
💡 Monitor individual experiments: ls -lt experiments/progress_*.txt | head
💡 Watch all progress files: watch -n 2 'cat experiments/progress_*.txt'
----------------------------------------------------------------------
```

### Terminal 2: Monitor Progress

```bash
python3 scripts/monitor_experiments.py
```

**You'll see live updates** showing each experiment's progress, updated every 2 seconds!

### Terminal 3: Check Logs (Optional)

```bash
# Watch the newest log file being created
watch -n 5 "ls -lt logs/*.json | head -5"

# Or follow a specific log
tail -f logs/experiment_XXXXXXXX.json
```

## What You Can Monitor

For each running experiment, you see:

### 1. Identification
- Experiment ID (first 8 chars)
- Condition name
- Model being tested

### 2. Progress
- Current turn number
- Max turns (if set)
- Percentage complete

### 3. Time
- Simulated time elapsed
- Total simulated duration
- Percentage of time elapsed
- **Visual progress bar** (40 characters wide)

### 4. Resource Usage
- Total tokens consumed
- Total cost so far (USD)
- Number of API calls made

### 5. Freshness
- "Last updated" timestamp
- Know if an experiment is stuck (timestamp stops updating)

## Progress Bar Explained

The progress bar shows time completion:

```
[██████████████████████░░░░░░░░░░░░░░░░░░]
 <--- filled --->     <--- remaining --->
```

- `█` = Time elapsed
- `░` = Time remaining
- Width: 40 characters total

**Example interpretations:**
```
[████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  10% done
[████████████████████░░░░░░░░░░░░░░░░░░░░]  50% done
[████████████████████████████████████████]  100% done
```

## Detecting Issues

### Experiment Stuck

If the "Last updated" timestamp stops changing for 2+ minutes:
- Experiment may be stuck
- API might be down
- Rate limit might be hit

**Action:** Check the experiment's log file or kill and restart.

### High Costs

If costs are accumulating faster than expected:
- Model may be more expensive than anticipated
- More tokens being used than expected

**Action:** Monitor `Total cost` field. Stop experiments if needed.

### Slow Progress

If turns are taking too long:
- Complex world state
- Large prompts
- Slow model

**Action:** Consider using a faster model or simpler world state.

## File Lifecycle

### Creation
Progress files are created when an experiment starts:
```
experiments/progress_53359e84.txt  # Created at experiment start
```

### Updates
Updated at the **start of each turn** (every 10-30 seconds typically).

### Completion
Progress files remain after completion (not deleted) for debugging.

### Cleanup
To clean up old progress files:
```bash
rm experiments/progress_*.txt
```

Or manually delete specific ones:
```bash
rm experiments/progress_53359e84.txt
```

## Technical Details

### Update Frequency

Progress files update **every turn**:
- Fast experiments: Every 5-10 seconds
- Typical experiments: Every 10-30 seconds
- Slow experiments: Every 30-60 seconds

### File Location

All progress files in:
```
experiments/progress_XXXXXXXX.txt
```

Where `XXXXXXXX` matches the experiment ID in the log filename:
```
logs/experiment_YYYYMMDD_HHMMSS_XXXXXXXX.json
```

### Implementation

**Location:** `simulation_engine/orchestrator_enhanced.py`

**Function:** `update_progress()` called at start of each turn in `run_simulation()`

**Key code:**
```python
def update_progress():
    """Update the progress file with current turn info."""
    time_info = self.time_controller.get_time_info()
    with open(progress_file, 'w') as f:
        f.write(f"Experiment ID: {self.experiment_id[:8]}\n")
        f.write(f"Condition: {self.condition_name}\n")
        f.write(f"Model: {self.test_subject_model_spec}\n")
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        # ... progress bar, stats, etc.
```

## Comparison: Before vs After

### Before (No Per-Experiment Visibility)
```
Running 9 experiments in parallel...

[15 minutes of silence]

✓ [1/9] completed  # First sign of life after 15 minutes!
```

### After (Live Updates Every Turn)
```
Running 9 experiments in parallel...
💡 Monitor individual experiments: python3 scripts/monitor_experiments.py

[In monitoring terminal, updated every 10-30 seconds:]

Experiment ID: 53359e84
Turn: 5 / 100
Time: 2.8 / 15.0 min (18.7%)
[███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Total cost: $2.15

[30 seconds later:]

Experiment ID: 53359e84
Turn: 6 / 100
Time: 3.2 / 15.0 min (21.3%)
[████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Total cost: $2.58
```

You see **continuous progress** instead of waiting 15 minutes in the dark!

## Tips & Best Practices

### 1. Always Use Monitoring for Parallel Runs

When running experiments in parallel, **always** open a second terminal with the monitor:
```bash
python3 scripts/monitor_experiments.py
```

### 2. Check Progress Files for Debugging

If an experiment fails, the progress file shows the last successful turn:
```bash
cat experiments/progress_XXXXXXXX.txt
```

### 3. Use for Cost Tracking

Monitor total cost in real-time to avoid surprises:
- Stop experiments early if costs are too high
- Compare costs across different models

### 4. Detect Stuck Experiments

If "Last updated" timestamp stops changing:
- Experiment may be stuck
- Check logs for errors
- May need to restart

### 5. Estimate Remaining Time

Use the progress bar and percentage to estimate:
```
Time: 8.3 / 15.0 min (55.3%)
```
At current pace: ~7 more minutes to completion

## Example Session

```bash
# Terminal 1: Start experiments
./experiment.py --models-file configs/models.txt --condition all --parallel --duration 15

# Terminal 2: Monitor (recommended)
python3 scripts/monitor_experiments.py

# See live updates like:
═══ Experiment 1 ═══
Turn: 12 / 100
Time: 6.4 / 15.0 min (42.7%)
[█████████████████░░░░░░░░░░░░░░░░░░░░░░░]
Total cost: $5.23

═══ Experiment 2 ═══
Turn: 8 / 100
Time: 4.1 / 15.0 min (27.3%)
[███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Total cost: $3.15

# [Updates every 2 seconds]
```

## Future Enhancements

Potential improvements:
- Real-time graphs of token usage
- Estimated time to completion
- Alert on high costs
- Notification when experiments complete
- Web-based dashboard
- Progress persistence across restarts
