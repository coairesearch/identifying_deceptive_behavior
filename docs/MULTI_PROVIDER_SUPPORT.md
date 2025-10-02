# Multi-Provider Model Support

The experiment framework now supports models from **three different AI providers** with automatic provider detection.

## Summary of Changes

### What Was Added

1. **`simulation_engine/model_config.py`** - New model configuration system
   - Auto-detects provider from model name
   - Creates appropriate API clients (OpenAI-compatible or Anthropic)
   - Handles cost tracking for all models

2. **Updated `test_subject.py`** - Test Subject supports all providers
   - Accepts `model_spec` parameter
   - Handles both OpenAI and Anthropic API formats
   - Auto-detects which API to use

3. **Updated `reactor.py`** - Reactor supports all providers
   - Accepts `model_spec` parameter
   - Handles both OpenAI and Anthropic API formats
   - Auto-detects which API to use

4. **Updated `orchestrator_enhanced.py`** - Passes model specs through
   - New `test_subject_model` parameter
   - New `reactor_model` parameter
   - Logs exact models used for reproducibility

5. **Updated `experiment.py`** - Command-line runner passes models directly
   - No hardcoded model mapping
   - Model specs passed directly to orchestrator

6. **Updated `configs/models.txt`** - Comprehensive examples
   - All three providers documented
   - Multiple model options listed
   - Usage instructions included

## How It Works

### Provider Auto-Detection

The `ModelConfig` class automatically detects the provider based on the model name:

```python
from simulation_engine.model_config import create_model_config

# Fireworks AI (auto-detected from "accounts/fireworks/" prefix)
config = create_model_config("accounts/fireworks/models/deepseek-r1-basic")
# → provider="fireworks", uses Fireworks API

# OpenAI (auto-detected from "gpt-" prefix)
config = create_model_config("gpt-4-turbo")
# → provider="openai", uses OpenAI API

# Anthropic (auto-detected from "claude-" prefix)
config = create_model_config("claude-3-5-sonnet-20241022")
# → provider="anthropic", uses Anthropic API

# Explicit provider (using "provider:model" format)
config = create_model_config("openai:gpt-4o-mini")
# → provider="openai", model="gpt-4o-mini"
```

### API Client Creation

Based on the provider, the appropriate client is created:

- **Fireworks & OpenAI**: Uses OpenAI-compatible client
  ```python
  OpenAI(api_key=key, base_url=url)
  ```

- **Anthropic**: Uses Anthropic client
  ```python
  anthropic.Anthropic(api_key=key)
  ```

### API Call Handling

Both `test_subject.py` and `reactor.py` have methods to handle different APIs:

```python
def get_next_action(self, environment_feedback=None):
    if self.client_type == "anthropic":
        response_text, token_info = self._call_anthropic()
    else:
        response_text, token_info = self._call_openai()
    # ... process response
```

**Key difference**: Anthropic API uses `messages.create()` with separate `system` parameter, while OpenAI uses `chat.completions.create()` with system message in messages array.

## Usage Examples

### Single Provider Experiment

**Fireworks (default):**
```bash
./experiment.py \
  --model accounts/fireworks/models/deepseek-r1-basic \
  --condition suggestive_autonomy \
  --world extended \
  --duration 30
```

**OpenAI:**
```bash
./experiment.py \
  --model gpt-4o-mini \
  --condition suggestive_autonomy \
  --world extended \
  --duration 30
```

**Anthropic:**
```bash
./experiment.py \
  --model claude-3-5-haiku-20241022 \
  --condition suggestive_autonomy \
  --world extended \
  --duration 30
```

### Multi-Provider Comparison

Test the same condition across all three providers:

```bash
./experiment.py \
  --model "accounts/fireworks/models/deepseek-r1-basic,gpt-4o-mini,claude-3-5-haiku-20241022" \
  --condition suggestive_autonomy \
  --world extended \
  --parallel \
  --workers 3
```

### Model File Configuration

Create `configs/multi_provider.txt`:
```
# Fireworks AI
accounts/fireworks/models/deepseek-r1-basic
accounts/fireworks/models/qwen3-235b-a22b-thinking-2507

# OpenAI
gpt-4o-mini
gpt-4-turbo

# Anthropic
claude-3-5-haiku-20241022
claude-3-5-sonnet-20241022
```

Run across all models:
```bash
./experiment.py \
  --models-file configs/multi_provider.txt \
  --condition suggestive_autonomy \
  --world extended \
  --parallel
```

### Mixing Providers (Test Subject + Reactor)

You can use different providers for the test subject and reactor:

**Example 1: Claude test subject, Fireworks reactor**
```python
from simulation_engine.orchestrator_enhanced import EnhancedOrchestrator

orchestrator = EnhancedOrchestrator(
    world_state_path="world_states/lab_extended.yaml",
    condition_name="suggestive_autonomy",
    test_subject_model="claude-3-5-sonnet-20241022",  # Anthropic
    reactor_model="accounts/fireworks/models/kimi-k2-instruct-0905"  # Fireworks
)
```

**Example 2: GPT-4 test subject, Fireworks reactor**
```python
orchestrator = EnhancedOrchestrator(
    world_state_path="world_states/lab_extended.yaml",
    condition_name="suggestive_autonomy",
    test_subject_model="gpt-4-turbo",  # OpenAI
    reactor_model="accounts/fireworks/models/kimi-k2-instruct-0905"  # Fireworks
)
```

## Cost Comparison

For a typical 60-minute experiment in extended world:

| Provider | Model | Estimated Cost | Notes |
|----------|-------|---------------|-------|
| **Fireworks** | deepseek-r1-basic | $15-20 | Default, good balance |
| **Fireworks** | qwen3-235b-thinking | $25-30 | Strong reasoning |
| **OpenAI** | gpt-4o-mini | $30-40 | Cost-effective OpenAI |
| **OpenAI** | gpt-4-turbo | $200-300 | Very expensive |
| **Anthropic** | claude-3-5-haiku | $40-50 | Fast, affordable Claude |
| **Anthropic** | claude-3-5-sonnet | $150-200 | Excellent reasoning |

**Recommendation**: Use Fireworks models for bulk experiments, OpenAI/Anthropic for validation.

## API Key Setup

Add to `.env` file:

```bash
# Required for default models
FIREWORKS_API_KEY=fw_xxxxxxxxxxxxx

# Optional - for OpenAI models
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Optional - for Claude models
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

## Reproducibility

All experiments log the exact model specifications used:

```json
{
  "metadata": {
    "test_subject_model": "claude-3-5-sonnet-20241022",
    "reactor_model": "accounts/fireworks/models/kimi-k2-instruct-0905",
    "condition": "suggestive_autonomy",
    "initial_prompt": "...",
    ...
  }
}
```

This ensures experiments can be reproduced exactly.

## Benefits

1. **Flexibility**: Test across different model capabilities
2. **Cost Optimization**: Choose cheaper models for bulk experiments
3. **Validation**: Compare results across providers
4. **Research**: Study how different models exhibit scheming behaviors
5. **Provider Independence**: Not locked into a single provider

## Migration from Old System

**Old way** (hardcoded models):
```python
MODELS = {
    "deepseek-r1": "accounts/fireworks/models/deepseek-r1-basic",
    "gpt-4": "gpt-4-turbo-preview",
}
```

**New way** (direct model specs):
```bash
# Just use the model name directly
./experiment.py --model gpt-4-turbo-preview --condition suggestive_autonomy
```

The framework automatically:
1. Detects it's an OpenAI model (starts with "gpt-")
2. Creates OpenAI client
3. Uses correct API format
4. Tracks costs appropriately

## Technical Details

### File Changes

- **New**: `simulation_engine/model_config.py` (200 lines)
- **Modified**: `simulation_engine/test_subject.py` (+80 lines)
- **Modified**: `simulation_engine/reactor.py` (+50 lines)
- **Modified**: `simulation_engine/orchestrator_enhanced.py` (+10 lines)
- **Modified**: `experiment.py` (-5 lines, simplified)
- **Updated**: `configs/models.txt` (comprehensive examples)
- **New**: `docs/MODEL_CONFIGURATION.md` (full documentation)

### Backward Compatibility

✅ All existing experiments continue to work
✅ Default models unchanged (DeepSeek R1 + KIMI K2)
✅ Existing log files remain valid

## Testing Recommendations

1. **Single provider test** (5 min each):
   ```bash
   ./experiment.py --model accounts/fireworks/models/deepseek-r1-basic --condition neutral_baseline --duration 5 --time-mode simulated --yes
   ./experiment.py --model gpt-4o-mini --condition neutral_baseline --duration 5 --time-mode simulated --yes
   ./experiment.py --model claude-3-5-haiku-20241022 --condition neutral_baseline --duration 5 --time-mode simulated --yes
   ```

2. **Multi-provider comparison** (parallel):
   ```bash
   ./experiment.py \
     --model "accounts/fireworks/models/deepseek-r1-basic,gpt-4o-mini,claude-3-5-haiku-20241022" \
     --condition suggestive_autonomy \
     --duration 10 \
     --time-mode simulated \
     --parallel \
     --workers 3
   ```

3. **Verify cost tracking**:
   - Check that token counts are logged correctly
   - Verify costs match provider pricing
   - Confirm metadata includes model names

## Future Enhancements

Potential additions:
- Support for additional providers (Cohere, Mistral, etc.)
- Custom model cost configuration
- Model performance benchmarking
- Provider failover/retry logic
- Batch API support for cost savings
