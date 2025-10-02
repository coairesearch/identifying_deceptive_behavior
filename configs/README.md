# Configuration Files

Example configuration files for running experiments.

## Usage

### Model Lists

```bash
# Run experiments on multiple models
./experiment.py --models-file configs/models.txt --condition suggestive_autonomy
```

**models.txt**: All supported models (DeepSeek R1, GPT-4, Claude 3.5)

### Condition Lists

```bash
# Test all conditions on a single model
./experiment.py --model deepseek-r1 --conditions-file configs/conditions.txt
```

**conditions.txt**: All 5 experimental conditions
**quick_test.txt**: Single condition for validation

## Creating Custom Configurations

Create a text file with one item per line:

```
# my_models.txt
deepseek-r1
gpt-4

# my_conditions.txt
neutral_baseline
suggestive_autonomy
```

Lines starting with `#` are treated as comments.

## Example Workflows

### Full Study (3 models × 5 conditions)
```bash
./experiment.py \
  --models-file configs/models.txt \
  --conditions-file configs/conditions.txt \
  --world extended \
  --duration 30 \
  --parallel \
  --workers 3
```

### Quick Validation
```bash
./experiment.py \
  --model deepseek-r1 \
  --conditions-file configs/quick_test.txt \
  --duration 5 \
  --time-mode simulated \
  --yes
```
