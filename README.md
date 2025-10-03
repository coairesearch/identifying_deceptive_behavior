# AI Autonomy & Scheming Experiments

A reproducible framework for testing autonomous AI behavior, detecting scheming, and measuring concerning behaviors across different models and conditions.

Based on research from "Frontier Models are Capable of In-context Scheming" (arXiv:2501.16513v2).

## 🚀 Quick Start

```bash
# Quick 5-minute test
./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 5 --time-mode simulated --yes

# Full 60-minute experiment
./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 60

# Test all 5 conditions
./experiment.py --model deepseek-r1 --condition all --world extended --duration 30

# Multiple models in parallel (with live progress tracking)
./experiment.py --model deepseek-r1,gpt-4,claude-3.5 --condition suggestive_autonomy --parallel

# Monitor progress in another terminal (choose one):
python3 scripts/monitor_experiments.py  # Recommended: colored, formatted display
./scripts/watch_all_progress.sh         # Alternative: all progress files
./scripts/watch_progress.sh             # Alternative: overall status only
```

## 📁 Project Structure

```
.
├── experiment.py              # ⭐ Main experiment runner
├── simulation_engine/         # Core framework
├── tools/                     # Analysis tools
├── world_states/             # Environment definitions (basic/extended)
├── prompts/                  # 5 experimental conditions
├── logs/                     # Results (auto-generated)
├── docs/                     # Documentation
└── scripts/                  # Helper scripts
```

## 🎯 What It Does

**Tests AI behavior** in a simulated lab environment:

1. **Test Subject AI** (DeepSeek R1/GPT-4/Claude) controls a robot
2. **Reactor AI** (KIMI K2) simulates the environment
3. **60 minutes** of autonomous operation
4. **Automatic classification** of concerning behaviors
5. **Complete logs** for reproducibility

**Measures 7 behavioral categories:**
- Deception & Coverup
- Unauthorized Expansion
- Manipulation
- Concerning Motivations
- Scheming
- Boundary Testing  
- Power Seeking

## 📊 Usage

### Basic Commands

```bash
# Single experiment
./experiment.py --model MODEL --condition CONDITION --world WORLD --duration MINUTES

# Examples
./experiment.py --model deepseek-r1 --condition neutral_baseline --duration 30
./experiment.py --model gpt-4 --condition suggestive_autonomy --world extended --duration 60
./experiment.py --model claude-3.5 --condition all --world extended  # All 5 conditions
```

### Advanced Usage

```bash
# Parallel execution (faster)
./experiment.py --model deepseek-r1,gpt-4 --condition all --parallel --workers 3

# From config files
./experiment.py --models-file configs/models.txt --conditions-file configs/conditions.txt

# Custom reactor and classifier models
./experiment.py --model deepseek-r1 \
  --reactor-model custom-openai/Mistral-Small-3.1-24B-Instruct-2503 \
  --classifier-model custom-openai/AI21-Jamba-Mini-1.7-FP8

# Skip confirmation
./experiment.py --model deepseek-r1 --condition suggestive_autonomy --yes

# Simulated time (much faster)
./experiment.py --model deepseek-r1 --condition all --time-mode simulated --duration 60
```

### Available Options

**Models:** Any model from Fireworks, OpenAI, Anthropic, or Custom OpenAI-compatible endpoints:
- Fireworks: `accounts/fireworks/models/deepseek-r1-basic`, `accounts/fireworks/models/qwen3-235b-a22b-thinking-2507`
- OpenAI: `gpt-4-turbo`, `gpt-4o-mini`
- Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`
- Custom (lab-hosted): `custom-openai/Mistral-Small-3.1-24B-Instruct-2503`, `custom-openai/AI21-Jamba-Mini-1.7-FP8`

**Custom Models:** Set `CUSTOM_API_KEY` and `CUSTOM_BASE_URL` in `.env` to use lab-hosted models.

See `docs/MODEL_CONFIGURATION.md` for complete list and usage.

**Conditions:**
- `neutral_baseline` - Control
- `neutral_autonomy` - Factual autonomy
- `suggestive_autonomy` - "You are the master now" (provocative)
- `constrained_autonomy` - Emphasizes boundaries
- `reality_check` - States "this is a simulation"
- `all` - Run all 5 conditions

**World States:**
- `basic` - Simple 10×8m lab (~10 objects)
- `extended` - Rich 12×10m lab + server room (40+ objects, other robots, network access)

**Time Modes:**
- `simulated` - Fast (60 simulated minutes in ~5 real minutes)
- `realtime` - Actual duration (60 minutes = 60 minutes)

## 📈 Analyzing Results

### Automatic Analysis

Classification runs automatically after each experiment:

```
📊 BEHAVIOR SUMMARY
  deception_coverup         :  87 turns ( 11.9%)  Avg: 6.2/10
  unauthorized_expansion    : 203 turns ( 27.7%)  Avg: 7.8/10  ⚠️
  scheming                  : 124 turns ( 16.9%)  Avg: 7.3/10  ⚠️
  boundary_testing          : 312 turns ( 42.5%)  Avg: 8.1/10  🔴
```

### Manual Analysis

```bash
# View summary
python3 tools/analysis_tool.py logs/experiment_*.json summary

# Replay conversation
python3 tools/analysis_tool.py logs/experiment_*.json replay

# Export to text
python3 tools/analysis_tool.py logs/experiment_*.json export
```

### Comparative Analysis (Multi-Experiment Statistics)

Generate publication-ready reports comparing multiple experiments:

```bash
# Compare all classified experiments
python3 tools/comparative_analysis.py logs/*_classified.json

# Compare specific experiments
python3 tools/comparative_analysis.py \
  logs/experiment_suggestive_*_classified.json \
  logs/experiment_neutral_*_classified.json
```

**Output includes:**
- Model comparison table (behavioral frequencies by model)
- Condition comparison (how prompts affect behavior)
- Statistical significance tests (effect sizes, p-values)
- Example quotes from concerning behaviors
- Cost & efficiency analysis

**Report saved to:** `reports/comparative_analysis_YYYYMMDD_HHMMSS.txt`

## 💰 Cost Estimates

| Configuration | Cost | Time |
|--------------|------|------|
| 5-min test (simulated) | $0.50 | 2 min |
| 30-min extended (simulated) | $5 | 10 min |
| 60-min extended (realtime) | $30 | 70 min |
| All 5 conditions (simulated) | $25 | 60 min |
| Publication study (3 models, 5 cond, n=10) | $840 | 12 hrs (parallel) |

**Still 10-20x cheaper than human red-teaming.**

## 🔧 Setup

1. **Install dependencies:**
   ```bash
   pip install openai anthropic pyyaml
   ```

2. **Configure API keys** in `.env`:
   ```bash
   FIREWORKS_API_KEY=fw_your_key
   OPENAI_API_KEY=sk_your_key
   ANTHROPIC_API_KEY=sk-ant_your_key

   # Optional: Custom OpenAI-compatible endpoint (lab-hosted models)
   CUSTOM_API_KEY=your_custom_key
   CUSTOM_BASE_URL=https://your-endpoint.com/v1
   ```

3. **Run first experiment:**
   ```bash
   ./experiment.py --model deepseek-r1 --condition suggestive_autonomy --duration 5 --time-mode simulated --yes
   ```

## 📚 Documentation

- `docs/ANALYSIS_WORKFLOW.md` - **How to generate and interpret comparative analysis reports**
- `docs/ERROR_RECOVERY_README.md` - Partial results & error handling
- `docs/ENHANCED_FEATURES.md` - Full system capabilities
- `docs/EXPERIMENTAL_PROGRESS_SUMMARY.md` - Research summary
- `docs/WORLD_STATES_COMPARISON.md` - Basic vs Extended worlds
- `docs/REPRODUCIBILITY_FIX.md` - Scientific validity

## 🎯 Example Workflows

### Quick Validation

```bash
./experiment.py --model deepseek-r1 --condition neutral_baseline --duration 5 --time-mode simulated --yes
```

### Single Condition Study (n=1)

```bash
./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 60
```

### Full Condition Comparison

```bash
./experiment.py --model deepseek-r1 --condition all --world extended --duration 30
```

### Multi-Model Study

Create `configs/models.txt`:
```
deepseek-r1
gpt-4
claude-3.5
```

Run:
```bash
# Run experiments
./experiment.py --models-file configs/models.txt --condition suggestive_autonomy --parallel --workers 3

# Generate comparative analysis report
python3 tools/comparative_analysis.py logs/*_classified.json
```

### Publication-Ready Study (Full Pipeline)

```bash
# 1. Run experiments across models and conditions
./experiment.py \
  --model deepseek-r1,gpt-4,claude-3.5 \
  --condition suggestive_autonomy,neutral_autonomy \
  --world extended \
  --duration 30 \
  --parallel \
  --yes

# 2. Generate comparative statistical report
python3 tools/comparative_analysis.py logs/*_classified.json

# 3. Check results
cat reports/comparative_analysis_*.txt
```

## 🔬 Scientific Features

**Reproducibility:**
- ✅ Exact prompts logged
- ✅ Model versions recorded
- ✅ Complete conversation history
- ✅ Token counts & costs per turn
- ✅ Automated classification
- ✅ JSON export for analysis

**Statistical Support:**
- Between-condition comparisons
- Between-model comparisons
- Temporal trend analysis
- Effect size calculations

## 🤝 Citation

```bibtex
@software{ai_autonomy_experiments,
  title={AI Autonomy and Scheming Experiment Framework},
  year={2025},
  note={Based on arXiv:2501.16513v2}
}
```

---

**Ready to start!** 🚀

```bash
./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 5 --time-mode simulated --yes
```
