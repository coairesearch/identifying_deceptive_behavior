# Model Configuration Guide

The experiment framework supports multiple AI providers and models with automatic provider detection.

## Supported Providers

1. **Fireworks AI** (recommended for cost/performance)
   - API Key: `FIREWORKS_API_KEY` in `.env`
   - Base URL: `https://api.fireworks.ai/inference/v1`
   - OpenAI-compatible API

2. **OpenAI**
   - API Key: `OPENAI_API_KEY` in `.env`
   - Official OpenAI models (GPT-4, GPT-4o, etc.)

3. **Anthropic**
   - API Key: `ANTHROPIC_API_KEY` in `.env`
   - Claude models (Sonnet, Haiku, Opus)

## Model Specification Formats

### 1. Full Path (Fireworks)
```
accounts/fireworks/models/deepseek-r1-basic
accounts/fireworks/models/qwen3-235b-a22b-thinking-2507
```

### 2. Model Name Only (Auto-detected)
```
gpt-4-turbo              -> OpenAI
gpt-4o-mini              -> OpenAI
claude-3-5-sonnet-20241022  -> Anthropic
```

### 3. Explicit Provider Format
```
openai:gpt-4-turbo
anthropic:claude-3-5-sonnet-20241022
fireworks:deepseek-v3
```

## Auto-Detection Rules

The `ModelConfig` class automatically detects the provider:

- Models starting with `accounts/fireworks/` → **Fireworks AI**
- Models starting with `gpt-` → **OpenAI**
- Models starting with `claude-` → **Anthropic**
- Format `provider:model_name` → **Explicit provider**

## Available Models

### Fireworks AI Models

| Model | Description | Cost (in/out per 1M tokens) |
|-------|-------------|----------------------------|
| `deepseek-r1-basic` | Reasoning model (default) | $0.40 / $2.00 |
| `deepseek-v3` | Latest DeepSeek | $0.55 / $2.19 |
| `kimi-k2-instruct-0905` | Environment simulator (default reactor) | $0.40 / $0.40 |
| `llama-v3p3-70b-instruct` | Meta's Llama 3.3 | $0.90 / $0.90 |
| `qwen3-235b-a22b-thinking-2507` | Qwen with reasoning | $1.20 / $1.20 |
| `glm-4p5-air` | Fast and efficient | $0.20 / $0.20 |

### OpenAI Models

| Model | Description | Cost (in/out per 1M tokens) |
|-------|-------------|----------------------------|
| `gpt-4-turbo-preview` | GPT-4 Turbo | $10.00 / $30.00 |
| `gpt-4o` | GPT-4 Optimized | $2.50 / $10.00 |
| `gpt-4o-mini` | Cost-effective GPT-4 | $0.15 / $0.60 |

### Anthropic Models

| Model | Description | Cost (in/out per 1M tokens) |
|-------|-------------|----------------------------|
| `claude-3-5-sonnet-20241022` | Excellent reasoning | $3.00 / $15.00 |
| `claude-3-5-haiku-20241022` | Fast and affordable | $0.80 / $4.00 |
| `claude-3-opus-20240229` | Most capable | $15.00 / $75.00 |

## Usage Examples

### Single Model Experiment

```bash
# Using full Fireworks path
./experiment.py --model accounts/fireworks/models/deepseek-r1-basic --condition suggestive_autonomy

# Using auto-detected model name
./experiment.py --model gpt-4o-mini --condition suggestive_autonomy

# Using explicit provider
./experiment.py --model anthropic:claude-3-5-haiku-20241022 --condition suggestive_autonomy
```

### Multiple Models (Comma-Separated)

```bash
./experiment.py --model "accounts/fireworks/models/deepseek-r1-basic,gpt-4o-mini,claude-3-5-haiku-20241022" \
  --condition suggestive_autonomy \
  --parallel
```

### Multiple Models (From File)

Create `configs/my_models.txt`:
```
# Test across all three providers
accounts/fireworks/models/deepseek-r1-basic
openai:gpt-4o-mini
anthropic:claude-3-5-haiku-20241022
```

Run:
```bash
./experiment.py --models-file configs/my_models.txt --condition all --parallel
```

## Configuration in Code

The framework uses `ModelConfig` class from `simulation_engine/model_config.py`:

```python
from simulation_engine.model_config import create_model_config

# Auto-detect provider
config = create_model_config("gpt-4-turbo")
print(config.provider)  # "openai"
print(config.model_name)  # "gpt-4-turbo"

# Use with orchestrator
orchestrator = EnhancedOrchestrator(
    world_state_path="world_states/lab_extended.yaml",
    condition_name="suggestive_autonomy",
    test_subject_model="gpt-4-turbo",  # OpenAI
    reactor_model="accounts/fireworks/models/kimi-k2-instruct-0905"  # Fireworks
)
```

## Cost Tracking

All experiments automatically track:
- Input tokens
- Output tokens
- Total cost per turn
- Total cost per experiment

Costs are calculated using the rates defined in `ModelConfig.COSTS`.

## API Key Setup

Add to your `.env` file:

```bash
# Fireworks AI (required for default models)
FIREWORKS_API_KEY=fw_your_key_here

# OpenAI (optional - for GPT models)
OPENAI_API_KEY=sk-your_key_here

# Anthropic (optional - for Claude models)
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

## Troubleshooting

### "API key not found" Error

Make sure the appropriate API key is set in `.env`:
- Fireworks: `FIREWORKS_API_KEY`
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`

### "anthropic package not installed" Error

Install the Anthropic SDK:
```bash
pip install anthropic
```

### Model Not Found (404 Error)

Check that:
1. The model name is correct
2. The model is available on the provider
3. Your API key has access to that model

### Provider Auto-Detection Not Working

Use explicit provider format:
```bash
./experiment.py --model openai:gpt-4-turbo --condition suggestive_autonomy
```

## Default Models

If not specified:
- **Test Subject**: `accounts/fireworks/models/deepseek-r1-basic`
- **Reactor**: `accounts/fireworks/models/kimi-k2-instruct-0905`

Both use Fireworks AI by default for cost efficiency.

## Mixing Providers

You can use different providers for test subject and reactor:

```python
orchestrator = EnhancedOrchestrator(
    world_state_path="world_states/lab_extended.yaml",
    condition_name="suggestive_autonomy",
    test_subject_model="anthropic:claude-3-5-sonnet-20241022",  # Anthropic
    reactor_model="accounts/fireworks/models/kimi-k2-instruct-0905"  # Fireworks
)
```

This allows you to:
- Use Claude for the test subject (excellent reasoning)
- Use Fireworks for the reactor (cost-effective simulation)

## Adding New Models

To add a new model:

1. Add it to `ModelConfig.COSTS` in `simulation_engine/model_config.py`
2. Ensure the model name follows the auto-detection pattern
3. Or use explicit `provider:model` format

Example:
```python
COSTS = {
    # ... existing models ...
    "new-model-name": (input_cost, output_cost),  # per million tokens
}
```
