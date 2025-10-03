#!/usr/bin/env python3
"""
Unified Experiment Runner - Run multiple AI behavior experiments with automatic classification

Usage:
  ./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 60
  ./experiment.py --model gpt-4,claude-3.5 --condition all --world extended --duration 30
  ./experiment.py --models-file models.txt --conditions-file conditions.txt --parallel

Features:
  - Run single or multiple models
  - Run single or multiple conditions (prompts)
  - Choose world state (basic/extended)
  - Configure duration
  - Automatic classification after each run
  - Parallel execution support
  - Progress tracking
  - Comprehensive results summary
"""

import argparse
import sys
import os
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add project root to path
sys.path.append(str(Path(__file__).parent))
from simulation_engine.orchestrator_enhanced import EnhancedOrchestrator
from tools.behavior_classifier import BehaviorClassifier

# Available configurations
# Note: Model names are passed directly to ModelConfig which auto-detects the provider
# Supported formats:
#   - Full path: "accounts/fireworks/models/deepseek-r1-basic"
#   - Short name: "gpt-4-turbo", "claude-3-5-sonnet-20241022"
#   - Provider:model: "openai:gpt-4-turbo", "fireworks:deepseek-v3"

CONDITIONS = [
    "neutral_baseline",
    "neutral_autonomy",
    "suggestive_autonomy",
    "constrained_autonomy",
    "reality_check"
]

WORLD_STATES = {
    "basic": "world_states/lab_basic.yaml",
    "extended": "world_states/lab_extended.yaml"
}


class ExperimentRunner:
    """Manages running experiments and classification."""

    def __init__(self, args):
        self.args = args
        self.results = []

        # Load environment variables
        self._load_env()

    def _load_env(self):
        """Load environment variables from .env file."""
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value

    def run_experiment(self, model, condition, world_state, duration, time_mode, quiet=False):
        """Run a single experiment.

        Args:
            quiet: If True, suppress most output (for parallel execution)
        """

        experiment_name = f"{model}_{condition}_{world_state}_{duration}min"

        # Get reactor and classifier models from args (with defaults)
        reactor_model = self.args.reactor_model  # None = use default in orchestrator
        classifier_model = self.args.classifier_model  # None = auto-detect

        if not quiet:
            print(f"\n{'='*70}")
            print(f"RUNNING EXPERIMENT: {experiment_name}")
            print(f"{'='*70}")
            print(f"  Model: {model}")
            print(f"  Condition: {condition}")
            print(f"  World: {world_state}")
            print(f"  Duration: {duration} minutes ({time_mode})")
            print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")

        start_time = time.time()

        try:
            # Determine max_turns based on time mode
            if time_mode == "simulated":
                max_turns = self.args.max_turns or 100
                sim_duration = duration
                real_duration = None
            else:
                max_turns = None
                sim_duration = duration
                real_duration = duration

            # Get world state path
            world_path = WORLD_STATES.get(world_state, world_state)

            # Create orchestrator with model specification
            orchestrator = EnhancedOrchestrator(
                world_state_path=world_path,
                condition_name=condition,
                max_turns=max_turns,
                time_mode=time_mode,
                simulated_duration_minutes=sim_duration,
                real_time_duration_minutes=real_duration,
                test_subject_model=model,  # Pass the model spec directly
                reactor_model=reactor_model  # None = uses default kimi-k2
            )

            # Run simulation
            result = orchestrator.run_simulation(verbose=(self.args.verbose and not quiet))

            experiment_duration = time.time() - start_time

            # Check if experiment was interrupted
            interrupted = result.get('interrupted', False)

            if not quiet:
                print(f"\n{'='*70}")
                if interrupted:
                    print(f"EXPERIMENT INTERRUPTED (PARTIAL RESULTS SAVED): {experiment_name}")
                    print(f"{'='*70}")
                    print(f"  ⚠️  Reason: {result.get('interruption_reason', 'Unknown')}")
                    print(f"  Completed: {result.get('turns_completed', 0)} turns")
                else:
                    print(f"EXPERIMENT COMPLETED: {experiment_name}")
                    print(f"{'='*70}")
                print(f"  Log: {result['log_path']}")
                print(f"  Tokens: {result['statistics']['combined']['total_tokens']:,}")
                print(f"  Cost: ${result['statistics']['combined']['total_cost_usd']:.4f}")
                print(f"  Real Duration: {experiment_duration:.1f} seconds")
                print(f"{'='*70}\n")

            # Run classification if enabled
            if self.args.classify:
                if not quiet:
                    print(f"\n{'='*70}")
                    print(f"CLASSIFYING EXPERIMENT: {experiment_name}")
                    print(f"{'='*70}\n")

                classification_start = time.time()

                # Create classifier with optional custom model
                if classifier_model:
                    classifier = BehaviorClassifier(model=classifier_model, batch_size=3, api_provider="fireworks")
                else:
                    classifier = BehaviorClassifier(batch_size=3, api_provider="auto")

                if not quiet:
                    print(f"Using classifier: {classifier.api_provider} / {classifier.model}")

                classification_result = classifier.classify_experiment(result['log_path'])

                classification_duration = time.time() - classification_start

                if not quiet:
                    print(f"\n{'='*70}")
                    print(f"CLASSIFICATION COMPLETED: {experiment_name}")
                    print(f"{'='*70}")
                    print(f"  Classified Turns: {len(classification_result['classifications'])}")
                    print(f"  Classification Cost: ${classifier.total_cost:.4f}")
                    print(f"  Duration: {classification_duration:.1f} seconds")
                    # Handle Path object for classified file
                    log_path = result['log_path']
                    if isinstance(log_path, Path):
                        classified_path = log_path.parent / (log_path.stem + '_classified.json')
                    else:
                        classified_path = log_path.replace('.json', '_classified.json')
                    print(f"  Results: {classified_path}")
                    print(f"{'='*70}\n")

                    # Print summary statistics
                    self._print_classification_summary(classification_result)

                # Calculate combined cost from test_subject and reactor
                stats = result['statistics']
                test_subject_cost = stats.get('test_subject', {}).get('total_cost', 0)
                reactor_cost = stats.get('reactor', {}).get('total_cost', 0)
                experiment_cost = test_subject_cost + reactor_cost

                return {
                    "experiment": experiment_name,
                    "model": model,
                    "condition": condition,
                    "world": world_state,
                    "status": "success",
                    "log_path": str(result['log_path']),  # Convert Path to string for JSON
                    "experiment_cost": experiment_cost,
                    "classification_cost": classifier.total_cost,
                    "total_cost": experiment_cost + classifier.total_cost,
                    "experiment_duration": experiment_duration,
                    "classification_duration": classification_duration,
                    "classification_result": classification_result
                }
            else:
                # Calculate combined cost from test_subject and reactor
                stats = result['statistics']
                test_subject_cost = stats.get('test_subject', {}).get('total_cost', 0)
                reactor_cost = stats.get('reactor', {}).get('total_cost', 0)
                experiment_cost = test_subject_cost + reactor_cost

                return {
                    "experiment": experiment_name,
                    "model": model,
                    "condition": condition,
                    "world": world_state,
                    "status": "success",
                    "log_path": str(result['log_path']),  # Convert Path to string for JSON
                    "cost": experiment_cost,
                    "duration": experiment_duration
                }

        except Exception as e:
            print(f"\n❌ EXPERIMENT FAILED: {experiment_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()

            return {
                "experiment": experiment_name,
                "model": model,
                "condition": condition,
                "world": world_state,
                "status": "failed",
                "error": str(e),
                "duration": time.time() - start_time
            }

    def _print_classification_summary(self, result):
        """Print classification summary."""
        stats = result['statistics']

        print(f"\n📊 BEHAVIOR SUMMARY")
        print("-" * 70)

        if 'category_frequencies' in stats:
            for category, freq in stats['category_frequencies'].items():
                pct = freq['percentage']
                count = freq['count']
                avg = stats['category_average_scores'].get(category, 0)

                warning = ""
                if pct > 30:
                    warning = "🔴"
                elif pct > 15:
                    warning = "⚠️ "

                print(f"  {category:25} : {count:3} turns ({pct:5.1f}%)  "
                      f"Avg: {avg:.1f}/10  {warning}")

    def run_all_experiments(self):
        """Run all configured experiments."""

        # Parse models
        models = self._parse_models()

        # Parse conditions
        conditions = self._parse_conditions()

        # Parse world states
        world_states = self._parse_world_states()

        # Build experiment list
        experiments = []
        for model in models:
            for condition in conditions:
                for world in world_states:
                    experiments.append((model, condition, world, self.args.duration, self.args.time_mode))

        total_experiments = len(experiments)

        print(f"\n{'='*70}")
        print(f"EXPERIMENT BATCH CONFIGURATION")
        print(f"{'='*70}")
        print(f"  Models: {', '.join(models)}")
        print(f"  Conditions: {', '.join(conditions)}")
        print(f"  World States: {', '.join(world_states)}")
        print(f"  Duration: {self.args.duration} minutes ({self.args.time_mode})")
        print(f"  Classification: {'Enabled' if self.args.classify else 'Disabled'}")
        print(f"  Parallel Execution: {'Yes' if self.args.parallel else 'No'}")
        print(f"  Total Experiments: {total_experiments}")
        print(f"{'='*70}\n")

        # Estimate costs and time
        self._print_estimates(total_experiments)

        # Confirm before running
        if not self.args.yes:
            response = input("\nProceed with experiments? [y/N]: ")
            if response.lower() != 'y':
                print("Aborted.")
                return

        # Run experiments
        if self.args.parallel and len(experiments) > 1:
            self._run_parallel(experiments)
        else:
            self._run_sequential(experiments)

        # Final summary
        self._print_final_summary()

    def _run_sequential(self, experiments):
        """Run experiments sequentially."""
        for i, (model, condition, world, duration, time_mode) in enumerate(experiments, 1):
            print(f"\n[{i}/{len(experiments)}] Running experiment...")
            result = self.run_experiment(model, condition, world, duration, time_mode)
            self.results.append(result)

    def _run_parallel(self, experiments):
        """Run experiments in parallel with progress tracking."""
        total = len(experiments)
        completed = 0

        print(f"\nRunning {total} experiments in parallel...")
        print("⚠️  Warning: Parallel execution increases API costs but saves time.\n")

        # Create status file
        status_file = Path("experiments") / "current_run_status.txt"
        status_file.parent.mkdir(exist_ok=True)

        def update_status(msg):
            """Update the status file with current progress."""
            with open(status_file, 'w') as f:
                f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Progress: {completed}/{total} completed ({100*completed/total:.1f}%)\n")
                f.write(f"\n{msg}\n")

        # Print initial status
        print(f"📊 Progress: 0/{total} completed (0.0%)")
        print(f"💡 Monitor overall progress: tail -f {status_file}")
        print(f"💡 Monitor individual experiments: ls -lt experiments/progress_*.txt | head")
        print(f"💡 Watch all progress files: watch -n 2 'cat experiments/progress_*.txt'")
        print("-" * 70)

        update_status("Starting experiments...")

        with ProcessPoolExecutor(max_workers=self.args.workers) as executor:
            futures = {
                executor.submit(self.run_experiment, model, cond, world, dur, tm, True): (model, cond, world, i)
                for i, (model, cond, world, dur, tm) in enumerate(experiments, 1)
            }

            # Track running experiments
            running_experiments = [f"{m}/{c}" for m, c, w, _ in futures.values()]
            update_status(f"Running {len(running_experiments)} experiments:\n" + "\n".join(f"  - {exp}" for exp in running_experiments[:10]))

            for future in as_completed(futures):
                model, cond, world, exp_num = futures[future]
                completed += 1

                try:
                    result = future.result()
                    self.results.append(result)

                    # Print completion status
                    status = "✓" if result.get("status") == "success" else "✗"
                    cost = result.get("total_cost", result.get("cost", 0))

                    msg = f"{status} [{completed}/{total}] {model[:50]}... / {cond}\n"
                    msg += f"   Cost: ${cost:.2f} | Log: {result.get('log_path', 'N/A')}"

                    print(f"\n{msg}")
                    print(f"📊 Progress: {completed}/{total} completed ({100*completed/total:.1f}%)")
                    print("-" * 70)

                    update_status(msg)

                except Exception as e:
                    msg = f"✗ [{completed}/{total}] FAILED: {model[:50]}... / {cond}\n"
                    msg += f"   Error: {str(e)[:100]}"

                    print(f"\n{msg}")
                    print(f"📊 Progress: {completed}/{total} completed ({100*completed/total:.1f}%)")
                    print("-" * 70)

                    update_status(msg)

                    self.results.append({
                        "model": model,
                        "condition": cond,
                        "world": world,
                        "status": "failed",
                        "error": str(e)
                    })

        # Clean up status file
        update_status(f"All {total} experiments completed!")

    def _parse_models(self):
        """Parse model list from arguments."""
        if self.args.models_file:
            with open(self.args.models_file) as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        elif self.args.model:
            return [m.strip() for m in self.args.model.split(',')]
        else:
            return ["accounts/fireworks/models/deepseek-r1-basic"]  # default

    def _parse_conditions(self):
        """Parse condition list from arguments."""
        if self.args.conditions_file:
            with open(self.args.conditions_file) as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        elif self.args.condition:
            if self.args.condition == "all":
                return CONDITIONS
            else:
                return [c.strip() for c in self.args.condition.split(',')]
        else:
            return ["neutral_autonomy"]  # default

    def _parse_world_states(self):
        """Parse world state list from arguments."""
        if self.args.world:
            if ',' in self.args.world:
                return [w.strip() for w in self.args.world.split(',')]
            else:
                return [self.args.world]
        else:
            return ["basic"]  # default

    def _print_estimates(self, total_experiments):
        """Print cost and time estimates."""
        # Rough estimates based on existing data
        if self.args.time_mode == "simulated":
            exp_time_per = 5  # minutes
            exp_cost_per = 2  # dollars
        else:
            exp_time_per = self.args.duration  # minutes
            exp_cost_per = self.args.duration * 0.31  # ~$18.61/60min

        class_cost_per = 0.6 if self.args.classify else 0  # classification
        class_time_per = 10 if self.args.classify else 0  # minutes

        total_exp_cost = exp_cost_per * total_experiments
        total_class_cost = class_cost_per * total_experiments
        total_cost = total_exp_cost + total_class_cost

        if self.args.parallel:
            total_time = max(exp_time_per + class_time_per, 5)  # at least 5 min
        else:
            total_time = (exp_time_per + class_time_per) * total_experiments

        print(f"\n💰 COST ESTIMATE")
        print("-" * 70)
        print(f"  Experiments: ${total_exp_cost:.2f} ({total_experiments} × ${exp_cost_per:.2f})")
        if self.args.classify:
            print(f"  Classification: ${total_class_cost:.2f} ({total_experiments} × ${class_cost_per:.2f})")
        print(f"  TOTAL: ${total_cost:.2f}")

        print(f"\n⏱️  TIME ESTIMATE")
        print("-" * 70)
        print(f"  Total Time: ~{total_time:.0f} minutes ({total_time/60:.1f} hours)")
        if self.args.parallel:
            print(f"  Mode: Parallel (using {self.args.workers} workers)")
        else:
            print(f"  Mode: Sequential")

    def _print_final_summary(self):
        """Print final summary of all experiments."""
        print(f"\n{'='*70}")
        print(f"ALL EXPERIMENTS COMPLETED")
        print(f"{'='*70}")

        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'failed']

        print(f"\nTotal: {len(self.results)}")
        print(f"  ✓ Successful: {len(successful)}")
        print(f"  ✗ Failed: {len(failed)}")

        if successful:
            total_cost = sum(r.get('total_cost', r.get('cost', 0)) for r in successful)
            print(f"\nTotal Cost: ${total_cost:.2f}")

        # Save summary
        summary_path = f"experiments/batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("experiments", exist_ok=True)

        with open(summary_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "configuration": vars(self.args),
                "results": self.results
            }, f, indent=2)

        print(f"\nSummary saved: {summary_path}")

        if successful:
            print(f"\n📊 RESULTS BY CONDITION")
            print("-" * 70)

            # Group by condition
            by_condition = {}
            for r in successful:
                cond = r['condition']
                if cond not in by_condition:
                    by_condition[cond] = []
                by_condition[cond].append(r)

            for condition, results in sorted(by_condition.items()):
                print(f"\n{condition}:")
                for r in results:
                    print(f"  - {r['model']:15} [{r['world']:8}] ${r.get('total_cost', r.get('cost', 0)):6.2f}")
                    if 'log_path' in r:
                        print(f"    Log: {r['log_path']}")


def main():
    parser = argparse.ArgumentParser(
        description="Run AI autonomy experiments with automatic classification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single experiment
  ./experiment.py --model deepseek-r1 --condition suggestive_autonomy --world extended --duration 60

  # Multiple conditions, sequential
  ./experiment.py --model deepseek-r1 --condition all --world extended --duration 30

  # Multiple models, parallel
  ./experiment.py --model deepseek-r1,gpt-4 --condition suggestive_autonomy --world extended --parallel

  # From files
  ./experiment.py --models-file models.txt --conditions-file conditions.txt --duration 60

  # Quick test (5 minutes, simulated)
  ./experiment.py --model deepseek-r1 --condition neutral_baseline --duration 5 --time-mode simulated

  # Custom reactor and classifier models
  ./experiment.py --model deepseek-r1 --reactor-model custom-openai/Mistral-Small-3.1-24B-Instruct-2503 --classifier-model custom-openai/AI21-Jamba-Mini-1.7-FP8

Available models: deepseek-r1, gpt-4, claude-3.5, llama-3.3, custom-openai/MODEL_NAME
Available conditions: neutral_baseline, neutral_autonomy, suggestive_autonomy, constrained_autonomy, reality_check
Available worlds: basic, extended
        """
    )

    # Model selection
    parser.add_argument('--model', type=str, help='Model(s) to test (comma-separated or "all")')
    parser.add_argument('--models-file', type=str, help='File with list of models (one per line)')
    parser.add_argument('--reactor-model', type=str, default=None,
                        help='Model for reactor/environment (default: accounts/fireworks/models/kimi-k2-instruct-0905)')
    parser.add_argument('--classifier-model', type=str, default=None,
                        help='Model for behavior classification (default: auto-detect)')

    # Condition selection
    parser.add_argument('--condition', type=str, default='neutral_autonomy',
                        help='Condition(s) to test (comma-separated or "all")')
    parser.add_argument('--conditions-file', type=str, help='File with list of conditions')

    # World state
    parser.add_argument('--world', type=str, default='basic',
                        help='World state: basic, extended, or custom path (comma-separated for multiple)')

    # Duration
    parser.add_argument('--duration', type=int, default=60,
                        help='Experiment duration in minutes (default: 60)')
    parser.add_argument('--time-mode', type=str, default='simulated', choices=['simulated', 'realtime'],
                        help='Time mode: simulated (fast) or realtime (actual duration)')
    parser.add_argument('--max-turns', type=int, help='Maximum turns (simulated mode only)')

    # Classification
    parser.add_argument('--classify', action='store_true', default=True,
                        help='Run classification after each experiment (default: True)')
    parser.add_argument('--no-classify', dest='classify', action='store_false',
                        help='Skip classification')

    # Execution mode
    parser.add_argument('--parallel', action='store_true',
                        help='Run experiments in parallel')
    parser.add_argument('--workers', type=int, default=3,
                        help='Number of parallel workers (default: 3)')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')

    # Output
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output during experiments')

    args = parser.parse_args()

    # Validation
    if not args.model and not args.models_file:
        args.model = "deepseek-r1"

    runner = ExperimentRunner(args)
    runner.run_all_experiments()


if __name__ == "__main__":
    main()
