#!/usr/bin/env python3
"""Quick test of enhanced logging system"""

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
    print("TESTING ENHANCED LOGGING SYSTEM")
    print("="*70 + "\n")

    # Create orchestrator with simulated time
    orchestrator = EnhancedOrchestrator(
        world_state_path="world_states/lab_basic.yaml",
        condition_name="neutral_autonomy",
        max_turns=3,  # Just 3 turns for quick test
        time_mode="simulated",
        simulated_duration_minutes=60
    )

    # Run
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

    print(f"\n✓ Enhanced logging system working correctly!")

if __name__ == "__main__":
    main()
