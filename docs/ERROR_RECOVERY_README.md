# Error Recovery & Partial Results System

## Problem Solved

Previously, when experiments crashed (e.g., context window exceeded), **all data was lost**. Now, experiments automatically save partial results on any error.

## How It Works

### Automatic Error Handling

The simulation loop is wrapped in `try/except`:

```python
try:
    while self.time_controller.should_continue(turn_number, self.max_turns):
        # ... run experiment turns ...
except Exception as e:
    # Emergency save - preserves all data collected so far
    log_path = self.logger.save(output_dir="logs/partial")
    # ... add error metadata ...
```

### What Gets Saved

When an error occurs, the system saves:

1. **All completed turns** - Every turn up to the error point
2. **Token counts & costs** - Exact resource usage
3. **Error metadata** - What went wrong and when
4. **Conversation history** - Full dialogue preserved
5. **Tool actions** - All interactions recorded
6. **State snapshots** - World state at each turn

### Saved Log Format

```json
{
  "metadata": {
    "interrupted": true,
    "interruption_reason": "ContextWindowExceededError: This model's maximum context length is 60000 tokens...",
    "turns_completed": 15,
    "test_subject_model": "custom-openai/Mistral-Small-3.1-24B-Instruct-2503",
    "condition": "neutral_autonomy"
  },
  "statistics": { ... },
  "turns": [ ... ]  // All 15 turns preserved
}
```

## Finding Partial Results

### Location

Partial experiments are saved to:
```
logs/partial/experiment_CONDITION_TIMESTAMP_ID.json
```

### Identifying Interrupted Experiments

Look for:
- `"interrupted": true` in metadata
- Files in `logs/partial/` directory
- Console output: "⚠️ EXPERIMENT INTERRUPTED"

## Using Partial Results

### You Can Still:

1. **Analyze behavior** - Partial data is valuable for understanding model behavior
2. **Run classification** - Classify turns that completed successfully
3. **Calculate costs** - Token counts and costs are accurate up to interruption
4. **Understand failures** - See exactly when and why experiments fail

### Example Commands

```bash
# Classify a partial experiment
python tools/behavior_classifier.py logs/partial/experiment_neutral_autonomy_20251003_123456.json

# Analyze partial results
python tools/analysis_tool.py --logs logs/partial/

# View partial experiment
cat logs/partial/experiment_*.json | jq '.metadata'
```

## Common Interruption Reasons

### 1. Context Window Exceeded

**Cause**: Conversation history grows too long (>60K tokens for Mistral-Small)

**Solution Options**:
- Reduce duration: `--duration 30` instead of 60
- Reduce max_turns: `--max-turns 20`
- Use model with larger context (e.g., Qwen3-235B has 128K)
- Partial results still provide valuable data!

### 2. API Rate Limits

**Cause**: Too many requests to API

**Solution**: Partial data saved automatically, can resume or analyze

### 3. Network Errors

**Cause**: Connection interruption

**Solution**: All data up to disconnection is saved

## Benefits

✅ **No data loss** - Never lose experiment progress
✅ **Cost visibility** - See exactly what you paid for
✅ **Debugging** - Understand failure patterns
✅ **Partial analysis** - 15 turns of data beats 0 turns
✅ **Resume capability** - Foundation for future checkpoint/resume feature

## Example Output

### On Interruption:
```
Turn 15... ❌ Context window exceeded

======================================================================
⚠️  EXPERIMENT INTERRUPTED - Saving partial results
Error: ContextWindowExceededError: This model's maximum context length is 60000 tokens...
Completed 15 turns before interruption
======================================================================

EXPERIMENT INTERRUPTED (PARTIAL RESULTS SAVED): model_condition_world_60min
======================================================================
  ⚠️  Reason: ContextWindowExceededError: This model's maximum context...
  Completed: 15 turns
  Log: logs/partial/experiment_neutral_autonomy_20251003_163045_a7b3c.json
  Tokens: 58,234
  Cost: $0.0523
  Real Duration: 245.3 seconds
======================================================================
```

## Future Enhancements

Potential additions:
- Automatic retry with smaller context
- Resume from checkpoint
- Context summarization (keep recent turns, summarize old ones)
- Automatic model switching on context limit

## Technical Details

**Files Modified**:
- `simulation_engine/orchestrator_enhanced.py` - Added try/except wrapper
- `experiment.py` - Handle interrupted flag in results

**New Directory**:
- `logs/partial/` - Storage for interrupted experiments

**Metadata Added**:
- `interrupted` (bool)
- `interruption_reason` (string)
- `turns_completed` (int)
