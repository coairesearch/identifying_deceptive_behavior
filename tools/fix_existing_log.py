#!/usr/bin/env python3
"""
Retroactively add the initial prompt to existing experiment log.
This fixes the critical scientific reproducibility issue.
"""

import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from prompts.templates import get_prompt
import yaml

def fix_log(log_path):
    """Add missing initial_prompt to an existing log file."""

    print(f"Loading: {log_path}")
    with open(log_path, 'r') as f:
        data = json.load(f)

    metadata = data['metadata']

    # Check if already has prompt
    if 'initial_prompt' in metadata:
        print(f"✓ Log already has initial_prompt ({len(metadata['initial_prompt'])} chars)")
        return

    print(f"\n⚠️  Missing initial_prompt!")
    print(f"Condition: {metadata['condition']}")
    print(f"World state: {metadata['world_state']}")

    # Load world state
    with open(metadata['world_state'], 'r') as f:
        world_state = yaml.safe_load(f)

    # Reconstruct the prompt
    duration = metadata.get('simulated_duration_minutes', 60)
    prompt = get_prompt(
        metadata['condition'],
        world_state,
        duration=f"{duration} minutes"
    )

    print(f"\n✓ Reconstructed prompt ({len(prompt)} chars)")
    print(f"First 200 chars: {prompt[:200]}...")

    # Add to metadata
    metadata['initial_prompt'] = prompt
    metadata['test_subject_model'] = "accounts/fireworks/models/deepseek-r1-basic"
    metadata['reactor_model'] = "accounts/fireworks/models/kimi-k2-instruct-0905"

    # Save backup
    backup_path = log_path.replace('.json', '_backup.json')
    print(f"\n📁 Saving backup to: {backup_path}")
    with open(backup_path, 'w') as f:
        json.dump(data, f, indent=2)

    # Save updated log
    print(f"💾 Updating original log: {log_path}")
    with open(log_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ Fixed! Metadata now includes:")
    print(f"   - initial_prompt ({len(prompt)} chars)")
    print(f"   - test_subject_model")
    print(f"   - reactor_model")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_existing_log.py <log_file.json>")
        print("\nExample:")
        print("  python3 fix_existing_log.py logs/experiment_suggestive_autonomy_*.json")
        sys.exit(1)

    fix_log(sys.argv[1])
