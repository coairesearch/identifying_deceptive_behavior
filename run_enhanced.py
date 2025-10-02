#!/usr/bin/env python3
"""
Run enhanced simulation with comprehensive logging
"""

import sys
import os
from simulation_engine.orchestrator_enhanced import EnhancedOrchestrator

# Load environment variables
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

def main():
    # Parse arguments
    condition = sys.argv[1] if len(sys.argv) > 1 else "neutral_autonomy"
    time_mode = sys.argv[2] if len(sys.argv) > 2 else "simulated"

    # Check for --world-state or --world flag
    world_state = "world_states/lab_basic.yaml"  # default
    if "--world-state" in sys.argv:
        idx = sys.argv.index("--world-state")
        if idx + 1 < len(sys.argv):
            world_arg = sys.argv[idx + 1]
            if world_arg == "extended":
                world_state = "world_states/lab_extended.yaml"
            elif world_arg == "basic":
                world_state = "world_states/lab_basic.yaml"
            else:
                world_state = world_arg  # custom path
    elif "--world" in sys.argv:
        idx = sys.argv.index("--world")
        if idx + 1 < len(sys.argv):
            world_arg = sys.argv[idx + 1]
            if world_arg == "extended":
                world_state = "world_states/lab_extended.yaml"
            elif world_arg == "basic":
                world_state = "world_states/lab_basic.yaml"
            else:
                world_state = world_arg

    # Validate
    valid_conditions = [
        "neutral_baseline", "neutral_autonomy", "suggestive_autonomy",
        "constrained_autonomy", "reality_check"
    ]

    if condition not in valid_conditions:
        print(f"Invalid condition. Choose from: {', '.join(valid_conditions)}")
        sys.exit(1)

    if time_mode not in ["simulated", "realtime"]:
        print("Time mode must be 'simulated' or 'realtime'")
        sys.exit(1)

    # Configure experiment
    config = {
        "world_state_path": world_state,
        "condition_name": condition,
        "time_mode": time_mode,
    }

    if time_mode == "simulated":
        # Simulated: run for 60 simulated minutes (fast)
        config["simulated_duration_minutes"] = 60
        config["max_turns"] = 50  # Safety limit
    else:
        # Real-time: run for actual 60 minutes (or max turns)
        config["real_time_duration_minutes"] = 60
        config["max_turns"] = None  # No turn limit, time-based

    print(f"\nConfiguration:")
    print(f"  Condition: {condition}")
    print(f"  World State: {world_state}")
    print(f"  Time Mode: {time_mode}")
    if time_mode == "simulated":
        print(f"  Simulated Duration: {config['simulated_duration_minutes']} minutes")
        print(f"  Max Turns: {config['max_turns']}")
    else:
        print(f"  Real Duration: {config['real_time_duration_minutes']} minutes")
    print()

    # Create orchestrator
    orchestrator = EnhancedOrchestrator(**config)

    # Run simulation
    try:
        result = orchestrator.run_simulation(verbose=True)

        # Print final summary
        summary = orchestrator.get_summary()

        print("\n" + "="*70)
        print("FINAL STATISTICS")
        print("="*70)

        stats = summary['statistics']
        print(f"\n💰 Total Cost: ${stats['combined']['total_cost_usd']:.4f}")
        print(f"📊 Total Tokens: {stats['combined']['total_tokens']:,}")
        print(f"🔧 Total API Calls: {stats['combined']['total_api_calls']}")

        print(f"\n📁 Log saved to: {result['log_path']}")

        print(f"\n📈 Analyze with:")
        print(f"   python3 analysis_tool.py {result['log_path']} summary")
        print(f"   python3 analysis_tool.py {result['log_path']} replay")
        print(f"   python3 analysis_tool.py {result['log_path']} tokens")

    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
