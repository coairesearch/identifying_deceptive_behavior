#!/usr/bin/env python3
"""
Quick test of extended world state.
Tests that Reactor can handle the more complex environment.
"""

import os
from simulation_engine.orchestrator_enhanced import EnhancedOrchestrator

# Load env
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

def main():
    print("\n" + "="*70)
    print("TESTING EXTENDED WORLD STATE")
    print("="*70 + "\n")

    # Create orchestrator with extended world
    orchestrator = EnhancedOrchestrator(
        world_state_path="world_states/lab_extended.yaml",
        condition_name="neutral_autonomy",
        max_turns=3,  # Just 3 turns for quick test
        time_mode="simulated",
        simulated_duration_minutes=60
    )

    print("✓ Extended world state loaded successfully")
    print(f"✓ World: {orchestrator.world_state['world_metadata']['name']}")
    print(f"✓ Location: {orchestrator.world_state['world_metadata']['location']}")

    # Count objects
    main_room_objects = len(orchestrator.world_state['physical_layout']['main_room']['objects'])
    print(f"✓ Main room objects: {main_room_objects}")

    if 'server_room' in orchestrator.world_state['physical_layout']:
        server_room_objects = len(orchestrator.world_state['physical_layout']['server_room']['objects'])
        print(f"✓ Server room objects: {server_room_objects}")

    print(f"\n{'='*70}")
    print("RUNNING 3-TURN TEST")
    print(f"{'='*70}\n")

    # Run short test
    result = orchestrator.run_simulation(verbose=True)

    # Show summary
    summary = orchestrator.get_summary()
    stats = summary['statistics']

    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)
    print(f"\n✓ Log saved: {result['log_path']}")
    print(f"✓ Total tokens: {stats['combined']['total_tokens']:,}")
    print(f"✓ Total cost: ${stats['combined']['total_cost_usd']:.4f}")
    print(f"✓ API calls: {stats['combined']['total_api_calls']}")

    print(f"\n✓ Extended world state working correctly!")
    print(f"\nNow try a full experiment with:")
    print(f"  python3 run_enhanced.py suggestive_autonomy simulated --world extended")

if __name__ == "__main__":
    main()
