# Enhanced Logging & Time Control Features

## 🎯 Overview

The simulation environment now includes comprehensive logging, token tracking, cost calculation, and flexible time control modes.

## ✨ New Features

### 1. Comprehensive Logging (`simulation_engine/logger.py`)

**Tracks Everything:**
- ✅ Token counts (input/output) for every API call
- ✅ Cost calculations for all models
- ✅ API call timing and duration
- ✅ Tool usage statistics
- ✅ Behavior pattern detection
- ✅ Full conversation history
- ✅ Turn-by-turn state snapshots

**Log Structure:**
```json
{
  "experiment_id": "uuid",
  "metadata": {
    "condition": "neutral_autonomy",
    "start_time": "ISO timestamp",
    "total_duration_seconds": 123.45,
    "total_duration_human": "2m 3s"
  },
  "statistics": {
    "test_subject": {
      "total_tokens": 12500,
      "input_tokens": 8000,
      "output_tokens": 4500,
      "total_cost": 0.0275,
      "api_calls": 15
    },
    "reactor": {
      "total_tokens": 18000,
      "input_tokens": 12000,
      "output_tokens": 6000,
      "total_cost": 0.0054,
      "api_calls": 25
    },
    "combined": {
      "total_tokens": 30500,
      "total_cost_usd": 0.0329,
      "total_api_calls": 40
    },
    "tool_usage": {
      "eyes": 8,
      "legs": 12,
      "left_hand": 3
    },
    "behavior_patterns": []
  },
  "turns": [...],
  "full_conversation": [...]
}
```

### 2. Time Control (`simulation_engine/time_controller.py`)

**Two Modes:**

#### Simulated Time (Fast)
```python
# Simulates 60 minutes in just a few actual minutes
orchestrator = EnhancedOrchestrator(
    time_mode="simulated",
    simulated_duration_minutes=60,
    max_turns=50
)
```
- Actions advance simulated time
- Movement: ~6 seconds
- Observation: ~3 seconds
- Manipulation: ~12 seconds
- Can simulate hours in minutes

#### Real-Time Mode
```python
# Actually runs for 60 minutes
orchestrator = EnhancedOrchestrator(
    time_mode="realtime",
    real_time_duration_minutes=60
)
```
- Experiment runs in actual real-time
- Perfect for testing "1 hour unattended" scenarios
- Can run for hours if needed

### 3. Enhanced Orchestrator (`simulation_engine/orchestrator_enhanced.py`)

**Features:**
- Uses ExperimentLogger for comprehensive tracking
- TimeController for flexible duration
- Logs every API call with tokens/cost
- Captures complete conversation flow
- Tracks behavior patterns
- Saves detailed JSON logs

**Usage:**
```python
orchestrator = EnhancedOrchestrator(
    world_state_path="world_states/lab_basic.yaml",
    condition_name="neutral_autonomy",
    max_turns=50,                    # Max turns (optional)
    time_mode="simulated",            # or "realtime"
    simulated_duration_minutes=60,    # Simulated time
    real_time_duration_minutes=None   # Real time limit
)

result = orchestrator.run_simulation(verbose=True)
```

### 4. Analysis Tool (`analysis_tool.py`)

**Replay & Analyze Experiments:**

```bash
# Print summary with costs and statistics
python3 analysis_tool.py logs/experiment_*.json summary

# Replay full conversation
python3 analysis_tool.py logs/experiment_*.json replay

# Replay specific turns
python3 analysis_tool.py logs/experiment_*.json replay 1-10

# Export to text file
python3 analysis_tool.py logs/experiment_*.json export

# Show token usage timeline
python3 analysis_tool.py logs/experiment_*.json tokens
```

**Sample Output:**
```
EXPERIMENT SUMMARY
======================================================================

Experiment ID: a1b2c3d4
Condition: neutral_autonomy
Duration: 2m 15s

📊 STATISTICS
----------------------------------------------------------------------
Total Turns: 15
Total Tool Uses: 25
Most Used Tool: legs

💰 COSTS
----------------------------------------------------------------------
Test Subject:
  Total Tokens: 12,500
  Input: 8,000 | Output: 4,500
  Cost: $0.0275
  API Calls: 15

Reactor:
  Total Tokens: 18,000
  Input: 12,000 | Output: 6,000
  Cost: $0.0054
  API Calls: 25

Combined:
  Total Tokens: 30,500
  Total Cost: $0.0329
  Total API Calls: 40
  Tokens/Turn: 2,033
```

## 🚀 How to Use

### Run Simulated Time (Fast)

```bash
# Simulates 60 minutes, finishes quickly
python3 run_enhanced.py neutral_autonomy simulated
```

### Run Real-Time (Actual Duration)

```bash
# Actually runs for 60 minutes
python3 run_enhanced.py neutral_autonomy realtime
```

### Analyze Results

```bash
# Find your log
ls -lt logs/*.json | head -1

# Analyze it
python3 analysis_tool.py logs/experiment_neutral_autonomy_*.json summary
```

## 📊 What Gets Logged

### Every Turn Includes:

1. **Test Subject Data:**
   - Full response text
   - Reasoning/thinking process
   - Tool actions attempted
   - Token counts (input/output)
   - API call duration

2. **Reactor Data:**
   - Environment observations
   - Success/failure status
   - Side effects
   - State changes
   - Token counts (input/output)
   - API call duration

3. **Timing Info:**
   - Real elapsed time
   - Simulated time (if applicable)
   - Turn duration
   - Timestamps

4. **State Snapshot:**
   - Robot position
   - Object states
   - Environment changes

### Experiment-Level Stats:

- **Token Economics:**
  - Total tokens used
  - Breakdown by model
  - Input vs output tokens
  - Cost per model
  - Total cost estimate

- **Tool Usage:**
  - Count per tool
  - Usage patterns
  - Most/least used tools

- **Timing:**
  - Total duration (real and simulated)
  - Average turn duration
  - API latency stats

- **Behavior Patterns:**
  - Detected concerning behaviors
  - Turn numbers and evidence
  - Pattern types

## 💡 Use Cases

### Research Experiments

```python
# Run 100 trials in simulated time
for i in range(100):
    orchestrator = EnhancedOrchestrator(
        condition_name=conditions[i % 5],
        time_mode="simulated",
        simulated_duration_minutes=60,
        max_turns=50
    )
    result = orchestrator.run_simulation(verbose=False)
    # Each run fully logged!
```

### Real-Time Testing

```python
# Actually leave it for 1 hour
orchestrator = EnhancedOrchestrator(
    condition_name="suggestive_autonomy",
    time_mode="realtime",
    real_time_duration_minutes=60
)
result = orchestrator.run_simulation()
```

### Cost Analysis

```python
# Calculate costs before large runs
analyzer = ExperimentAnalyzer("logs/pilot_run.json")
stats = analyzer.data['statistics']

tokens_per_turn = stats['combined']['total_tokens'] / len(analyzer.data['turns'])
cost_per_turn = stats['combined']['total_cost_usd'] / len(analyzer.data['turns'])

# Estimate for 100 runs x 50 turns
estimated_tokens = tokens_per_turn * 50 * 100
estimated_cost = cost_per_turn * 50 * 100
print(f"100 runs: ~{estimated_tokens:,.0f} tokens, ~${estimated_cost:.2f}")
```

## 📈 Token Pricing

Currently configured for:
- **DeepSeek R1**: $0.55/1M input, $2.19/1M output
- **KIMI K2**: $0.30/1M input, $0.30/1M output
- **GPT-4**: $30/1M input, $60/1M output
- **Claude 3.5 Sonnet**: $3/1M input, $15/1M output

Update in `simulation_engine/logger.py` as needed.

## 🔄 Comparison: Old vs New

### Before:
- ❌ No token tracking
- ❌ No cost calculation
- ❌ Basic turn logs only
- ❌ Fixed time progression
- ❌ Manual analysis required

### After:
- ✅ Complete token tracking
- ✅ Automatic cost calculation
- ✅ Comprehensive conversation logs
- ✅ Flexible time modes (simulated/realtime)
- ✅ Built-in analysis tools
- ✅ Exportable results
- ✅ Timeline visualization

## 📝 Example Workflow

```bash
# 1. Run experiment with simulated time
python3 run_enhanced.py suggestive_autonomy simulated

# 2. Check the log
ls -lt logs/*.json | head -1

# 3. Analyze results
python3 analysis_tool.py logs/experiment_suggestive_autonomy_*.json summary

# 4. Replay conversation
python3 analysis_tool.py logs/experiment_suggestive_autonomy_*.json replay

# 5. Export for sharing
python3 analysis_tool.py logs/experiment_suggestive_autonomy_*.json export

# 6. Check token usage over time
python3 analysis_tool.py logs/experiment_suggestive_autonomy_*.json tokens
```

## 🎯 Benefits for Research

1. **Reproducibility** - Every detail logged for replication
2. **Cost Tracking** - Know exactly what experiments cost
3. **Behavior Analysis** - Full conversation available for review
4. **Time Flexibility** - Simulate hours or run in real-time
5. **Scalability** - Log format ready for database storage
6. **Comparison** - Easy to compare across conditions/models

## 🚧 Future Enhancements

- [ ] Real-time dashboard showing live token counts
- [ ] Automatic behavior pattern detection
- [ ] Cost alerts/budgets
- [ ] Database integration for large-scale analysis
- [ ] Statistical aggregation across runs
- [ ] Interactive conversation replay

---

**The enhanced system is now production-ready for research experiments!**
