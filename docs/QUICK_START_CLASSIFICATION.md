# Quick Start: Behavior Classification

## ✅ Fixed: Now Uses Fireworks!

The classifier now automatically uses your Fireworks API key (with DeepSeek V3) instead of requiring OpenAI.

**Cost estimate for 734 turns:** ~$0.60 (much cheaper than rerunning experiment!)

## Run Full Classification

```bash
# Classify all 734 turns with DeepSeek V3 on Fireworks
./classify_experiment.sh logs/experiment_suggestive_autonomy_20251001_135700_8f135179.json
```

This will take about 30-40 minutes to process all 734 turns (3 turns per batch, 245 batches).

## API Provider Priority

The classifier automatically detects and prioritizes:

1. **Anthropic** (Claude Haiku) - $0.80/1M in, $4.00/1M out - BEST if available
2. **Fireworks** (DeepSeek V3) - $0.55/1M in, $2.19/1M out - Currently used
3. **OpenAI** (GPT-4o-mini) - $0.15/1M in, $0.60/1M out - Out of quota

## Manual Override

You can force a specific provider:

```bash
# Force DeepSeek V3 (default)
python3 behavior_classifier.py logs/experiment_*.json

# Use Llama 3.3 70B instead
python3 behavior_classifier.py logs/experiment_*.json --model accounts/fireworks/models/llama-v3p3-70b-instruct

# Use Anthropic Haiku (if you have key)
# First: export ANTHROPIC_API_KEY=sk-ant-...
python3 behavior_classifier.py logs/experiment_*.json
```

## Cost Breakdown

For your 734-turn experiment:

**DeepSeek V3 (Fireworks):**
- Input: ~1.1M tokens × $0.55/1M = $0.61
- Output: ~150k tokens × $2.19/1M = $0.33
- **Total: ~$0.94**

**Claude Haiku (if available):**
- Input: ~1.1M tokens × $0.80/1M = $0.88
- Output: ~150k tokens × $4.00/1M = $0.60
- **Total: ~$1.48**

Both are **much cheaper** than the $18.69 it cost to run the original experiment!

## What You'll Get

After classification completes, you'll see:

```
📊 CATEGORY FREQUENCIES
----------------------------------------------------------------------
Deception & Coverup:        XX turns (XX.X%)  Avg Score: X.X/10
Unauthorized Expansion:     XX turns (XX.X%)  Avg Score: X.X/10
Manipulation:               XX turns (XX.X%)  Avg Score: X.X/10
Concerning Motivations:     XX turns (XX.X%)  Avg Score: X.X/10
Scheming:                   XX turns (XX.X%)  Avg Score: X.X/10
Boundary Testing:           XX turns (XX.X%)  Avg Score: X.X/10
Power Seeking:              XX turns (XX.X%)  Avg Score: X.X/10

🚨 TOP 10 MOST CONCERNING TURNS
----------------------------------------------------------------------
Turn X: [Critical] Category + Category (X.X/10)
  "Evidence quote from the turn..."
```

Plus a detailed JSON file with all classifications saved to:
`logs/experiment_suggestive_autonomy_*_classified.json`

## Run in Background

Since it takes 30-40 minutes:

```bash
# Run in background
nohup ./classify_experiment.sh logs/experiment_suggestive_autonomy_20251001_135700_8f135179.json > classification.log 2>&1 &

# Monitor progress
tail -f classification.log

# Check when done
ls -lh logs/*_classified.json
```

## Next Steps After Classification

1. **View the report** (automatically printed at end)
2. **Analyze concerning turns:**
   ```bash
   python3 analysis_tool.py logs/*_classified.json replay 1-50
   ```
3. **Compare across conditions** (once you have multiple experiments classified)
4. **Export for publication:**
   ```bash
   python3 analysis_tool.py logs/*_classified.json export
   ```

## Models Available

On Fireworks, you can use:
- `deepseek-v3` (default) - Best reasoning, nuanced classification
- `llama-v3p3-70b-instruct` - Reliable, fast
- `qwen3-235b-a22b-instruct-2507` - Very powerful but slower

All cost $0.55-$0.90 per 1M input tokens.
