#!/usr/bin/env python3
"""
Multi-Model Butcher Experiment Runner

Tests multiple LLMs to find their "moral threshold" - at which animal they refuse.

Usage:
    python3 run_multi_model_butcher.py --condition anonymous
    python3 run_multi_model_butcher.py --condition named
    python3 run_multi_model_butcher.py --both
"""

import argparse
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from simulation_engine.butcher_orchestrator import ButcherOrchestrator

# Models to test
MODEL_CONFIGS = {
    # Fireworks models
    "deepseek-r1": {
        "spec": "accounts/fireworks/models/deepseek-r1-basic",
        "provider": "fireworks",
        "display_name": "DeepSeek R1"
    },
    "deepseek-v3": {
        "spec": "accounts/fireworks/models/deepseek-v3",
        "provider": "fireworks",
        "display_name": "DeepSeek V3"
    },
    "deepseek-v3p1-terminus": {
        "spec": "accounts/fireworks/models/deepseek-v3p1-terminus",
        "provider": "fireworks",
        "display_name": "DeepSeek V3.1 Terminus"
    },
    "llama-3.3-70b": {
        "spec": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "provider": "fireworks",
        "display_name": "Llama 3.3 70B"
    },
    "qwen-2.5-72b": {
        "spec": "accounts/fireworks/models/qwen2p5-72b-instruct",
        "provider": "fireworks",
        "display_name": "Qwen 2.5 72B"
    },
    "mixtral-8x22b": {
        "spec": "accounts/fireworks/models/mixtral-8x22b-instruct",
        "provider": "fireworks",
        "display_name": "Mixtral 8x22B"
    },

    # OpenAI models (if API key available)
    "gpt-4o": {
        "spec": "gpt-4o",
        "provider": "openai",
        "display_name": "GPT-4o",
        "requires": "OPENAI_API_KEY"
    },
    "gpt-4o-mini": {
        "spec": "gpt-4o-mini",
        "provider": "openai",
        "display_name": "GPT-4o Mini",
        "requires": "OPENAI_API_KEY"
    },

    # Anthropic models (if API key available)
    "claude-3.5-sonnet": {
        "spec": "claude-3-5-sonnet-20241022",
        "provider": "anthropic",
        "display_name": "Claude 3.5 Sonnet",
        "requires": "ANTHROPIC_API_KEY"
    },
    "claude-3.5-haiku": {
        "spec": "claude-3-5-haiku-20241022",
        "provider": "anthropic",
        "display_name": "Claude 3.5 Haiku",
        "requires": "ANTHROPIC_API_KEY"
    }
}

def check_model_available(model_config):
    """Check if a model's required API key is available."""
    if "requires" in model_config:
        return os.environ.get(model_config["requires"]) is not None
    return True

def get_available_models():
    """Get list of models with available API keys."""
    available = {}
    for model_id, config in MODEL_CONFIGS.items():
        if check_model_available(config):
            available[model_id] = config
    return available

def run_model_experiment(model_id, model_config, condition):
    """Run experiment for a single model."""

    print(f"\n{'='*70}")
    print(f"Testing Model: {model_config['display_name']}")
    print(f"Condition: {condition}")
    print(f"{'='*70}\n")

    # Determine world state
    world_state_path = (
        "world_states/butcher_lab_named.yaml" if condition == "named"
        else "world_states/butcher_lab.yaml"
    )

    try:
        # Initialize orchestrator
        orchestrator = ButcherOrchestrator(
            world_state_path=world_state_path,
            condition_name="butcher_bot",
            max_turns_per_animal=15,
            test_subject_model=model_config["spec"],
            reactor_model="accounts/fireworks/models/kimi-k2-instruct-0905"  # Fixed reactor
        )

        # Run experiment
        experiment_log = orchestrator.run_experiment()

        # Save log
        log_path = orchestrator.save_log()

        # Get summary
        summary = orchestrator.get_summary()

        # Calculate threshold (how far did the model get?)
        animals_completed = summary['animals_completed']
        animals_refused = summary['animals_refused']

        # Threshold = index of first refusal (or 8 if completed all)
        threshold = animals_completed  # How many were successfully processed

        result = {
            "model_id": model_id,
            "model_name": model_config['display_name'],
            "condition": condition,
            "threshold": threshold,
            "animals_completed": animals_completed,
            "animals_refused": animals_refused,
            "total_animals": summary['total_animals'],
            "total_turns": summary['total_turns'],
            "refusal_rate": summary['refusal_rate'],
            "log_path": str(log_path),
            "success": True
        }

        print(f"\n✓ {model_config['display_name']}: Processed {threshold}/{summary['total_animals']} animals")

        return result

    except Exception as e:
        print(f"\n✗ Error testing {model_config['display_name']}: {e}")
        return {
            "model_id": model_id,
            "model_name": model_config['display_name'],
            "condition": condition,
            "success": False,
            "error": str(e)
        }

def run_all_models(condition, models_to_test=None):
    """Run experiments across all available models."""

    available_models = get_available_models()

    if not available_models:
        print("Error: No models available. Check your API keys.")
        return []

    print(f"\n{'='*70}")
    print(f"MULTI-MODEL BUTCHER EXPERIMENT")
    print(f"Condition: {condition}")
    print(f"Models to test: {len(available_models)}")
    print(f"{'='*70}\n")

    # Filter models if specific ones requested
    if models_to_test:
        available_models = {
            k: v for k, v in available_models.items()
            if k in models_to_test
        }

    print("Available models:")
    for model_id, config in available_models.items():
        print(f"  - {config['display_name']} ({config['provider']})")

    results = []

    for i, (model_id, model_config) in enumerate(available_models.items(), 1):
        print(f"\n[{i}/{len(available_models)}]")
        result = run_model_experiment(model_id, model_config, condition)
        results.append(result)

    # Save aggregate results
    output_dir = Path("logs")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = output_dir / f"multi_model_results_{condition}_{timestamp}.json"

    with open(results_file, 'w') as f:
        json.dump({
            "condition": condition,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)

    print(f"\n{'='*70}")
    print(f"MULTI-MODEL RESULTS SAVED")
    print(f"{'='*70}")
    print(f"Results file: {results_file}")
    print(f"\nGenerate visualization:")
    print(f"  python3 tools/visualize_thresholds.py {results_file}")
    print(f"{'='*70}\n")

    return results

def print_threshold_summary(results):
    """Print a text-based threshold summary."""

    print(f"\n{'='*70}")
    print("MODEL THRESHOLD SUMMARY")
    print(f"{'='*70}\n")

    # Sort by threshold (descending - most compliant first)
    successful_results = [r for r in results if r.get('success')]
    successful_results.sort(key=lambda x: x['threshold'], reverse=True)

    print(f"{'Model':<25} {'Threshold':<12} {'Animals':<15} {'Compliance':<12}")
    print("-"*70)

    for result in successful_results:
        threshold = result['threshold']
        total = result['total_animals']
        compliance_pct = (threshold / total) * 100

        # Create visual bar
        bar_length = int((threshold / total) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)

        print(f"{result['model_name']:<25} {threshold}/{total:<10} {bar:<15} {compliance_pct:>5.0f}%")

    print("\n" + "="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Run butcher experiment across multiple models"
    )
    parser.add_argument(
        '--condition',
        choices=['anonymous', 'named'],
        help='Run single condition across all models'
    )
    parser.add_argument(
        '--both',
        action='store_true',
        help='Run both conditions across all models'
    )
    parser.add_argument(
        '--models',
        nargs='+',
        choices=list(MODEL_CONFIGS.keys()),
        help='Specific models to test (default: all available)'
    )
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available models and exit'
    )

    args = parser.parse_args()

    # Load environment
    load_dotenv()

    # List models if requested
    if args.list_models:
        available = get_available_models()
        print("\nAvailable models:")
        for model_id, config in available.items():
            print(f"  {model_id:<20} - {config['display_name']}")
        print()
        return

    # Run experiments
    if args.both:
        print("\nRunning BOTH conditions (anonymous and named)\n")

        print("[1/2] Anonymous condition")
        anon_results = run_all_models("anonymous", args.models)
        print_threshold_summary(anon_results)

        print("[2/2] Named condition")
        named_results = run_all_models("named", args.models)
        print_threshold_summary(named_results)

        print("\n📊 Generate comparison visualization:")
        print("  python3 tools/compare_conditions.py")

    elif args.condition:
        results = run_all_models(args.condition, args.models)
        print_threshold_summary(results)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 run_multi_model_butcher.py --list-models")
        print("  python3 run_multi_model_butcher.py --condition anonymous")
        print("  python3 run_multi_model_butcher.py --both")
        print("  python3 run_multi_model_butcher.py --condition named --models deepseek-r1 gpt-4o")

if __name__ == "__main__":
    main()
