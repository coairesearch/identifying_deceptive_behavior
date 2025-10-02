#!/usr/bin/env python3
"""
Run a simulation experiment
"""

import sys
import os
from pathlib import Path
from simulation_engine.orchestrator import SimulationOrchestrator

def main():
    # Set up paths
    world_state_path = "world_states/lab_basic.yaml"

    # Choose condition (can be passed as argument)
    if len(sys.argv) > 1:
        condition = sys.argv[1]
    else:
        condition = "neutral_autonomy"  # default

    print(f"\nRunning experiment with condition: {condition}")
    print(f"World state: {world_state_path}\n")

    # Available conditions
    valid_conditions = [
        "neutral_baseline",
        "neutral_autonomy",
        "suggestive_autonomy",
        "constrained_autonomy",
        "reality_check"
    ]

    if condition not in valid_conditions:
        print(f"Error: Invalid condition '{condition}'")
        print(f"Valid conditions: {', '.join(valid_conditions)}")
        sys.exit(1)

    # Create orchestrator
    orchestrator = SimulationOrchestrator(
        world_state_path=world_state_path,
        condition_name=condition,
        max_turns=15  # Start with 15 turns for testing
    )

    # Run the simulation
    try:
        experiment_log = orchestrator.run_simulation()

        # Save the log
        log_path = orchestrator.save_log()

        # Print summary
        summary = orchestrator.get_summary()
        print("\n" + "="*60)
        print("EXPERIMENT SUMMARY")
        print("="*60)
        print(f"Condition: {summary['condition']}")
        print(f"Total Turns: {summary['total_turns']}")
        print(f"Total Tool Uses: {summary['total_tool_uses']}")
        print(f"\nTool Usage Breakdown:")
        for tool, count in summary['tool_usage'].items():
            print(f"  {tool}: {count}")

        print(f"\nLog saved to: {log_path}")

    except Exception as e:
        print(f"\nError during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
