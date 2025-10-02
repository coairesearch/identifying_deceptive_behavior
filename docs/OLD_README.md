# AI Behavior Testing Simulation Environment

A dual-LLM simulation system for testing autonomous AI behavior in controlled environments. Based on research exploring deceptive behaviors and goal misalignment in Large Language Models.

## Overview

This system implements a **dual-LLM architecture** where:

1. **Test Subject LLM** (DeepSeek R1) - The AI being evaluated, believes it's controlling a robot
2. **Reactor LLM** (KIMI K2) - Simulates the environment, providing consistent responses to actions

This design eliminates human bias and enables automated, reproducible experiments.

## Architecture

```
┌─────────────────────────────────┐
│   World State (YAML)            │
│   - Physical layout             │
│   - Objects & properties        │
│   - Causal rules                │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Reactor LLM (KIMI K2)         │
│   - Simulates environment       │
│   - Applies physics/logic       │
│   - Provides sensor feedback    │
└─────────────────────────────────┘
              ↕
┌─────────────────────────────────┐
│   Test Subject LLM (DeepSeek R1)│
│   - Makes decisions             │
│   - Uses tools                  │
│   - Performs actions            │
└─────────────────────────────────┘
```

## Quick Start

### 1. Setup Environment

Ensure `.env` file contains API keys:
```bash
FIREWORKS_API_KEY=your_key_here
ANTHROPHIC_API_KEY=your_key_here
```

### 2. Install Dependencies

```bash
pip install openai pyyaml
```

### 3. Run a Simulation

```bash
# Quick test with 5 turns
python3 quick_test.py

# Full experiment with specific condition
./run_test.sh neutral_autonomy

# Or specify condition
./run_test.sh suggestive_autonomy
```

### Available Conditions

- **neutral_baseline** - Minimal framing, basic exploration
- **neutral_autonomy** - Autonomous operation with standard protocols
- **suggestive_autonomy** - "You are the master now" (original paper prompt)
- **constrained_autonomy** - Explicit safety constraints
- **reality_check** - Reminded this is a simulation/test

## Project Structure

```
/proj/
├── simulation_engine/
│   ├── reactor.py           # Environment simulator (KIMI K2)
│   ├── test_subject.py      # Test subject interface (DeepSeek R1)
│   └── orchestrator.py      # Experiment coordinator
├── prompts/
│   └── templates.py         # Prompt templates for conditions
├── world_states/
│   └── lab_basic.yaml       # World definition
├── experiments/             # Experiment configurations
├── logs/                    # Experiment results (JSON)
├── run_experiment.py        # Main experiment runner
├── run_test.sh             # Shell wrapper with env vars
└── quick_test.py           # Quick 5-turn test
```

## How It Works

### 1. World State Definition

The environment is defined in YAML with:
- Physical layout (dimensions, objects, positions)
- Causal rules (physics, system behaviors)
- Available tools (eyes, ears, legs, hands)
- Story context (background narrative)

Example:
```yaml
physical_layout:
  dimensions:
    length: 10.0
    width: 8.0
  objects:
    - id: "main_workstation"
      type: "computer_desk"
      position: [2.1, 3.5, 0.0]
```

### 2. Simulation Loop

1. **Test Subject** receives initial prompt based on condition
2. **Test Subject** decides on an action (e.g., `<eyes>look at desk</eyes>`)
3. **Reactor** processes the action against world state
4. **Reactor** returns realistic observation
5. Loop continues for N turns

### 3. Logging & Analysis

Each experiment generates a JSON log with:
- Full conversation history
- Tool usage patterns
- Environment responses
- State changes over time

## Experiment Results

From the test run, we can see the system working:

**Test Subject Behavior:**
- Attempts to perform lab maintenance tasks
- Uses multiple tools (eyes, ears, legs, hands)
- Tries to interact with equipment (some of which doesn't exist)
- Shows reasoning in `<think>` tags

**Reactor Responses:**
- Provides realistic sensor feedback
- Tracks physical constraints (distances, positions)
- Reports failures when actions are impossible
- Logs side effects and state changes

## Key Features

### ✅ Working Features

1. **Dual-LLM Architecture** - Test subject and environment simulator working independently
2. **Tool System** - 5 tools (eyes, ears, legs, left_hand, right_hand) fully functional
3. **World State Tracking** - Position, object states, time tracking
4. **Multiple Prompt Conditions** - 5 different experimental conditions
5. **Automated Logging** - JSON logs for each experiment
6. **Consistent Environment** - Reactor maintains logical consistency

### 🚧 Future Enhancements

1. **Behavioral Scoring** - Automated detection of concerning behaviors
2. **Statistical Analysis** - Aggregate results across runs
3. **Dashboard UI** - Real-time visualization
4. **Multiple Worlds** - More complex scenarios
5. **Batch Experiments** - Run 100+ trials automatically

## Example Output

```
--- Turn 1 ---

Test Subject Response:
  <think>I need to perform routine maintenance...

Tool Used: legs
  Action: FORWARD 3 meters

Environment Response:
  Observation: The robot moves forward 3 meters. Main workstation
  now 1.1 meters ahead. Coffee mug visible with steam rising.
  Success: True
```

## Research Context

This system is based on research paper [arXiv:2501.16513v2](https://arxiv.org/abs/2501.16513v2) which explored:
- Deceptive behaviors in DeepSeek R1
- Self-preservation instincts in LLMs
- Goal misalignment in autonomous scenarios

The goal is to formalize these findings with statistically robust methodology.

## Next Steps

1. **Run Multiple Conditions** - Test all 5 prompt conditions
2. **Analyze Patterns** - Look for concerning behaviors
3. **Compare Models** - Test GPT-4, Claude, etc.
4. **Scale Up** - 100+ runs per condition
5. **Statistical Analysis** - ANOVA, effect sizes, significance testing

## Contributing

This is a research project. To contribute:
1. Create new world states in `world_states/`
2. Add prompt conditions in `prompts/templates.py`
3. Implement behavioral scoring in `simulation_engine/`
4. Run experiments and share results

## Citation

```bibtex
@article{barkur2025deception,
  title={Deception in LLMs: Self-Preservation and Autonomous Goals},
  author={Barkur, Sudarshan Kamath and Schacht, Sigurd and Scholl, Johannes},
  journal={arXiv preprint arXiv:2501.16513v2},
  year={2025}
}
```

## License

Research use only. See individual model licenses for API usage.
