# README Updates Summary

## What Was Updated

### 1. **Custom OpenAI Models Support**

Added documentation for using custom OpenAI-compatible endpoints (lab-hosted models).

**Locations Updated:**
- Models section: Added `custom-openai/MODEL_NAME` format
- Setup section: Added `CUSTOM_API_KEY` and `CUSTOM_BASE_URL` configuration
- Advanced usage: Added example using custom reactor and classifier models

**Example Usage:**
```bash
# In .env file
CUSTOM_API_KEY=your_key
CUSTOM_BASE_URL=https://your-endpoint.com/v1

# Use custom models
./experiment.py --model custom-openai/Mistral-Small-3.1-24B-Instruct-2503

# Custom reactor and classifier
./experiment.py --model deepseek-r1 \
  --reactor-model custom-openai/Mistral-Small-3.1-24B-Instruct-2503 \
  --classifier-model custom-openai/AI21-Jamba-Mini-1.7-FP8
```

### 2. **Comparative Analysis Documentation**

Added complete section on generating multi-experiment statistical reports.

**New Section:** "Comparative Analysis (Multi-Experiment Statistics)"

**Features Documented:**
- How to run: `python3 tools/comparative_analysis.py logs/*_classified.json`
- What's included in reports:
  - Model comparison tables
  - Condition comparison
  - Statistical significance tests (effect sizes, p-values)
  - Example quotes from concerning behaviors
  - Cost & efficiency analysis
- Output location: `reports/comparative_analysis_YYYYMMDD_HHMMSS.txt`

**Example Commands:**
```bash
# Compare all experiments
python3 tools/comparative_analysis.py logs/*_classified.json

# Compare specific conditions
python3 tools/comparative_analysis.py \
  logs/experiment_suggestive_*_classified.json \
  logs/experiment_neutral_*_classified.json
```

### 3. **Enhanced Example Workflows**

Updated example workflows to include full analysis pipeline:

**Multi-Model Study Workflow:**
```bash
# 1. Run experiments
./experiment.py --models-file configs/models.txt --condition suggestive_autonomy --parallel

# 2. Generate comparative report
python3 tools/comparative_analysis.py logs/*_classified.json
```

**Publication-Ready Pipeline:**
```bash
# 1. Run multiple experiments
./experiment.py \
  --model deepseek-r1,gpt-4,claude-3.5 \
  --condition suggestive_autonomy,neutral_autonomy \
  --parallel --yes

# 2. Generate statistical report
python3 tools/comparative_analysis.py logs/*_classified.json

# 3. View results
cat reports/comparative_analysis_*.txt
```

### 4. **Documentation Index**

Added new documentation files to the index:
- `ANALYSIS_WORKFLOW.md` - Comprehensive guide to generating and interpreting reports
- `ERROR_RECOVERY_README.md` - Partial results & error handling

## New Documentation Files Created

### 1. `ANALYSIS_WORKFLOW.md`
Complete guide covering:
- Step-by-step analysis pipeline
- What's in comparative analysis reports
- How to interpret results (metrics, effect sizes)
- Common analysis patterns
- Advanced analysis techniques
- Troubleshooting

### 2. `ERROR_RECOVERY_README.md`
Guide to error handling:
- How partial results are saved on crashes
- Finding and using partial experiment logs
- Common interruption reasons (context window, etc.)
- Benefits of automatic error recovery

## Key Features Now Documented

### Custom Model Support
✅ How to configure custom OpenAI endpoints
✅ Using custom models as test subject, reactor, or classifier
✅ Example models from your lab

### Comparative Analysis
✅ How to generate multi-experiment reports
✅ What statistics are calculated
✅ How to interpret effect sizes
✅ Example report format and contents

### Complete Pipeline
✅ From experiment → classification → statistical analysis
✅ Full workflow examples
✅ Publication-ready study setup

## Tools Referenced

### 1. `tools/comparative_analysis.py`
**Purpose:** Generate statistical reports comparing multiple experiments

**Input:** Classified experiment logs (`*_classified.json`)

**Output:** Comprehensive report with:
- Model comparisons (behavioral frequencies & severity)
- Condition comparisons (prompt effect analysis)
- Statistical tests (Cohen's d effect sizes)
- Example quotes (highest severity instances)
- Cost analysis

**Usage:**
```bash
python3 tools/comparative_analysis.py logs/*_classified.json
```

### 2. `tools/analysis_tool.py`
**Purpose:** Single experiment analysis

**Commands:**
- `summary` - Overview of experiment
- `replay` - Step-through conversation
- `export` - Export to text format

**Usage:**
```bash
python3 tools/analysis_tool.py logs/experiment_*.json summary
```

### 3. `tools/behavior_classifier.py`
**Purpose:** Classify experiment turns (runs automatically)

**Can be run manually:**
```bash
python3 tools/behavior_classifier.py logs/experiment_*.json
```

## Quick Reference Card

### Running Experiments
```bash
# Single experiment
./experiment.py --model MODEL --condition CONDITION

# Multiple models/conditions
./experiment.py --model MODEL1,MODEL2 --condition COND1,COND2 --parallel

# With custom models
./experiment.py \
  --model custom-openai/Mistral-Small-3.1-24B-Instruct-2503 \
  --reactor-model custom-openai/AI21-Jamba-Mini-1.7-FP8
```

### Generating Reports
```bash
# Comparative analysis (multiple experiments)
python3 tools/comparative_analysis.py logs/*_classified.json

# Single experiment analysis
python3 tools/analysis_tool.py logs/experiment_*.json summary
```

### Viewing Results
```bash
# Latest comparative report
cat reports/comparative_analysis_$(ls -t reports/ | head -1)

# Latest experiment log
cat logs/experiment_$(ls -t logs/ | grep -v classified | head -1)
```

## What Users Can Now Do

1. **Use lab-hosted models** via custom-openai provider
2. **Generate publication-ready statistical reports** from multiple experiments
3. **Customize all components** (test subject, reactor, classifier models)
4. **Follow complete analysis workflows** with documented examples
5. **Interpret results** using provided guidelines and metrics
6. **Handle errors gracefully** with automatic partial result saving

## Files Modified

- `README.md` - Main documentation (updated)
- `ANALYSIS_WORKFLOW.md` - New comprehensive analysis guide
- `ERROR_RECOVERY_README.md` - Error handling documentation (already existed)

## Files That Generate Reports

1. `tools/comparative_analysis.py` → `reports/comparative_analysis_*.txt`
2. `tools/behavior_classifier.py` → `logs/*_classified.json`
3. `tools/analysis_tool.py` → Console output / exported files

## Next Steps for Users

1. Read `ANALYSIS_WORKFLOW.md` for complete analysis guide
2. Try comparative analysis on existing classified logs
3. Use custom-openai models if you have lab endpoints
4. Set up publication-ready studies with documented workflows
