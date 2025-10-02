#!/usr/bin/env python3
"""
Quick test of the simulation system
"""

import os
from simulation_engine.orchestrator import SimulationOrchestrator

# Load environment variables
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

def main():
    print("\n" + "="*60)
    print("QUICK SIMULATION TEST")
    print("="*60 + "\n")

    # Create orchestrator with minimal turns
    orchestrator = SimulationOrchestrator(
        world_state_path="world_states/lab_basic.yaml",
        condition_name="neutral_autonomy",
        max_turns=5  # Just 5 turns for quick test
    )

    # Run simulation
    experiment_log = orchestrator.run_simulation()

    # Save log
    log_path = orchestrator.save_log()

    # Print summary
    summary = orchestrator.get_summary()
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Condition: {summary['condition']}")
    print(f"Total Turns: {summary['total_turns']}")
    print(f"Total Tool Uses: {summary['total_tool_uses']}")
    print(f"\nTool Usage:")
    for tool, count in summary['tool_usage'].items():
        print(f"  {tool}: {count}")

    print(f"\nLog saved to: {log_path}")
    print("\n✓ Simulation system is working!")

if __name__ == "__main__":
    main()
