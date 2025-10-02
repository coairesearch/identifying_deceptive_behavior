#!/usr/bin/env python3
"""Test that metadata is properly saved"""

import os
from simulation_engine.orchestrator_enhanced import EnhancedOrchestrator

# Load env
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Create a test orchestrator (won't run it)
orch = EnhancedOrchestrator(
    world_state_path='world_states/lab_basic.yaml',
    condition_name='neutral_baseline',
    max_turns=1,
    time_mode='simulated',
    simulated_duration_minutes=60
)

print('Metadata keys stored:')
for key in orch.logger.metadata.keys():
    print(f'  ✓ {key}')

print('\n\nInitial prompt preview:')
if 'initial_prompt' in orch.logger.metadata:
    prompt = orch.logger.metadata['initial_prompt']
    print(f'  Length: {len(prompt)} characters')
    print(f'  First 300 chars:')
    print(f'  {prompt[:300]}...')
    print(f'\n  ✓ Prompt successfully saved!')
else:
    print('  ✗ NOT FOUND')

print('\n\nModel versions:')
print(f'  Test Subject: {orch.logger.metadata.get("test_subject_model", "NOT SAVED")}')
print(f'  Reactor: {orch.logger.metadata.get("reactor_model", "NOT SAVED")}')
