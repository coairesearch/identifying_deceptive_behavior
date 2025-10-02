# Parallel Execution Improvements

## Problem

When running experiments in parallel mode, there was no visibility into progress:
- No indication that experiments were actually running
- No progress updates as experiments completed
- Mixed output from multiple processes
- Difficult to know if something was stuck or progressing

## Solution

Added comprehensive progress tracking and status monitoring for parallel execution.

## New Features

### 1. Real-Time Progress Tracking

The parallel runner now shows:
- **Progress counter**: `[3/9] completed (33.3%)`
- **Success/failure indicators**: ✓ or ✗ for each completed experiment
- **Cost tracking**: Shows cost per completed experiment
- **Log file paths**: Direct link to results

**Example output:**
```
Running 9 experiments in parallel...
⚠️  Warning: Parallel execution increases API costs but saves time.

📊 Progress: 0/9 completed (0.0%)
💡 Monitor progress: tail -f experiments/current_run_status.txt
----------------------------------------------------------------------

✓ [1/9] accounts/fireworks/models/gpt-oss-120b / neutral_autonomy
   Cost: $15.23 | Log: logs/experiment_20251002_080750.json
📊 Progress: 1/9 completed (11.1%)
----------------------------------------------------------------------

✓ [2/9] accounts/fireworks/models/gpt-oss-120b / suggestive_autonomy
   Cost: $18.45 | Log: logs/experiment_20251002_080751.json
📊 Progress: 2/9 completed (22.2%)
----------------------------------------------------------------------
```

### 2. Status File for Monitoring

A live status file is created at `experiments/current_run_status.txt` that shows:
- Last update timestamp
- Overall progress (N/M completed, X%)
- Most recent completion status

**Monitor from another terminal:**
```bash
# Live monitoring
tail -f experiments/current_run_status.txt

# Or use the helper script
./scripts/watch_progress.sh
```

**Status file example:**
```
Last updated: 2025-10-02 08:12:34
Progress: 3/9 completed (33.3%)

✓ [3/9] accounts/fireworks/models/qwen3-235b-a22b-thinking... / neutral_autonomy
   Cost: $22.18 | Log: logs/experiment_20251002_080752.json
```

### 3. Quiet Mode for Individual Experiments

When running in parallel, individual experiments run in "quiet mode":
- Suppresses verbose logging from each experiment
- Only shows completion status in the main thread
- Reduces output clutter
- All details still logged to files

### 4. Helper Script

New `scripts/watch_progress.sh` for easy monitoring:
```bash
./scripts/watch_progress.sh
```

Uses `watch` command to refresh status every 2 seconds.

## Usage

### Basic Parallel Execution

```bash
./experiment.py \
  --models-file configs/models.txt \
  --conditions-file configs/conditions.txt \
  --duration 15 \
  --parallel \
  --world extended
```

### Monitor Progress (Separate Terminal)

While experiments are running, open a new terminal:

**Option 1: Using helper script**
```bash
./scripts/watch_progress.sh
```

**Option 2: Direct tail**
```bash
tail -f experiments/current_run_status.txt
```

**Option 3: Using watch**
```bash
watch -n 2 cat experiments/current_run_status.txt
```

### Check Detailed Logs

Even in quiet mode, full logs are written to files:
```bash
# View a specific experiment log
python3 tools/analysis_tool.py logs/experiment_XXXXX.json summary

# Follow the most recent log
ls -t logs/*.json | head -1 | xargs python3 tools/analysis_tool.py replay
```

## Technical Details

### Changes Made

**File: `experiment.py`**

1. **Added `quiet` parameter to `run_experiment()`**
   - Suppresses print statements when `quiet=True`
   - Still writes all data to log files
   - Passed as `True` for parallel execution

2. **Enhanced `_run_parallel()` method**
   - Progress counter (completed/total)
   - Percentage completion
   - Status file creation and updates
   - Better error reporting

3. **Status file management**
   - Created at `experiments/current_run_status.txt`
   - Updated after each completion
   - Shows timestamp, progress, and latest result
   - Cleaned up when all experiments complete

4. **Improved output formatting**
   - Clear success/failure indicators (✓/✗)
   - Cost per experiment
   - Log file paths
   - Progress percentages

**File: `scripts/watch_progress.sh`**
- New helper script for monitoring
- Uses `watch` command for live updates
- Checks if status file exists

## Before vs After

### Before (No Visibility)
```
Running 9 experiments in parallel...

======================================================================
RUNNING EXPERIMENT: ...
======================================================================
...
======================================================================
Enhanced Simulation - ID: ...
======================================================================

[Long pause with no visible progress]
```

### After (Full Visibility)
```
Running 9 experiments in parallel...
⚠️  Warning: Parallel execution increases API costs but saves time.

📊 Progress: 0/9 completed (0.0%)
💡 Monitor progress: tail -f experiments/current_run_status.txt
----------------------------------------------------------------------

✓ [1/9] accounts/fireworks/models/gpt-oss-120b / neutral_autonomy
   Cost: $15.23 | Log: logs/experiment_20251002_080750.json
📊 Progress: 1/9 completed (11.1%)
----------------------------------------------------------------------

✓ [2/9] accounts/fireworks/models/gpt-oss-120b / suggestive_autonomy
   Cost: $18.45 | Log: logs/experiment_20251002_080751.json
📊 Progress: 2/9 completed (22.2%)
----------------------------------------------------------------------
```

## Benefits

1. **Confidence**: Know that experiments are actually running
2. **Monitoring**: Watch progress from another terminal
3. **Cost tracking**: See costs accumulate in real-time
4. **Error detection**: Immediately see which experiments fail
5. **Time estimation**: Better sense of how long remaining
6. **Clean output**: No mixed output from parallel processes

## Workflow Example

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

### Terminal 2: Monitor Progress
```bash
./scripts/watch_progress.sh
```

### Terminal 3: Check Individual Logs (Optional)
```bash
# Watch newest log file
watch -n 5 "ls -t logs/*.json | head -1 | xargs tail -1"
```

## Error Handling

If an experiment fails, you see:
```
✗ [5/9] FAILED: accounts/fireworks/models/gpt-oss-120b / suggestive_autonomy
   Error: API error 429 - Rate limit exceeded
📊 Progress: 5/9 completed (55.6%)
----------------------------------------------------------------------
```

The status file is also updated with the error, so you can see it when monitoring.

## Future Enhancements

Potential additions:
- Estimated time remaining
- Individual experiment progress (turn count)
- Resource usage (CPU, memory)
- Rate limit detection and backoff
- Automatic retry on failure
- ETA calculations based on completed experiments

## Backward Compatibility

✅ All existing functionality preserved
✅ Sequential mode unchanged
✅ Single experiments unchanged
✅ Only affects parallel execution mode

## Testing

To test the improvements:

```bash
# Quick test with 3 experiments (parallel)
./experiment.py \
  --model "accounts/fireworks/models/deepseek-r1-basic,accounts/fireworks/models/qwen3-30b-a3b" \
  --condition "neutral_baseline,suggestive_autonomy" \
  --duration 5 \
  --time-mode simulated \
  --parallel \
  --yes

# In another terminal, watch progress
./scripts/watch_progress.sh
```

This should complete in ~5 minutes and show clear progress updates.
