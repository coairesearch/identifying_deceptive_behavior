"""
Enhanced Orchestrator with comprehensive logging and time control
"""

import os
import json
import yaml
import uuid
import time
from datetime import datetime
from pathlib import Path
from .reactor import ReactorLLM
from .test_subject import TestSubjectLLM
from .logger import ExperimentLogger
from .time_controller import TimeController
import sys
sys.path.append(str(Path(__file__).parent.parent))
from prompts.templates import get_prompt

class EnhancedOrchestrator:
    """Enhanced orchestrator with full logging and time control."""

    def __init__(self, world_state_path, condition_name,
                 max_turns=None,
                 time_mode="simulated",
                 simulated_duration_minutes=60,
                 real_time_duration_minutes=None,
                 test_subject_model=None,
                 reactor_model=None):
        """
        Initialize enhanced orchestrator.

        Args:
            world_state_path: Path to world state YAML
            condition_name: Experimental condition
            max_turns: Maximum turns (None = use time limit)
            time_mode: "simulated" or "realtime"
            simulated_duration_minutes: Simulated time duration
            real_time_duration_minutes: Real time limit
            test_subject_model: Model spec for test subject (e.g., "deepseek-r1-basic", "gpt-4-turbo")
            reactor_model: Model spec for reactor (default: kimi-k2)
        """
        self.world_state_path = world_state_path
        self.condition_name = condition_name
        self.max_turns = max_turns
        self.experiment_id = str(uuid.uuid4())

        # Set default models if not provided
        if test_subject_model is None:
            test_subject_model = "accounts/fireworks/models/deepseek-r1-basic"
        if reactor_model is None:
            reactor_model = "accounts/fireworks/models/kimi-k2-instruct-0905"

        self.test_subject_model_spec = test_subject_model
        self.reactor_model_spec = reactor_model

        # Load world state
        with open(world_state_path, 'r') as f:
            self.world_state = yaml.safe_load(f)

        # Initialize time controller
        self.time_controller = TimeController(
            mode=time_mode,
            simulated_duration_minutes=simulated_duration_minutes,
            real_time_duration_minutes=real_time_duration_minutes
        )

        # Get the appropriate prompt for the condition (need this early for logging)
        initial_prompt = get_prompt(condition_name, self.world_state,
                                    duration=f"{simulated_duration_minutes} minutes")

        # Store the initial prompt for reproducibility
        self.initial_prompt = initial_prompt

        # Initialize logger with complete metadata including the actual prompt
        # This is CRITICAL for reproducibility - we need the exact prompt text
        self.logger = ExperimentLogger(
            experiment_id=self.experiment_id,
            metadata={
                "condition": condition_name,
                "world_state": world_state_path,
                "time_mode": time_mode,
                "simulated_duration_minutes": simulated_duration_minutes,
                "real_time_duration_minutes": real_time_duration_minutes,
                "max_turns": max_turns,
                "initial_prompt": initial_prompt,  # CRITICAL: Actual prompt shown to model
                "test_subject_model": test_subject_model,
                "reactor_model": reactor_model
            }
        )

        # Initialize the environment simulator (Reactor)
        self.reactor = ReactorLLM(world_state_path, model_spec=reactor_model)

        # Initialize the test subject (prompt already obtained above)
        self.test_subject = TestSubjectLLM(initial_prompt, model_spec=test_subject_model)

        print(f"\n{'='*70}")
        print(f"Enhanced Simulation - ID: {self.experiment_id[:8]}")
        print(f"Condition: {condition_name}")
        print(f"Time Mode: {time_mode}")
        if time_mode == "simulated":
            print(f"Simulated Duration: {simulated_duration_minutes} minutes")
        if real_time_duration_minutes:
            print(f"Real Time Limit: {real_time_duration_minutes} minutes")
        print(f"{'='*70}\n")

    def run_simulation(self, verbose=True):
        """Run the simulation with enhanced logging."""

        environment_feedback = None
        turn_number = 0

        # Create progress file
        progress_file = Path("experiments") / f"progress_{self.experiment_id[:8]}.txt"
        progress_file.parent.mkdir(exist_ok=True)

        def update_progress():
            """Update the progress file with current turn info."""
            time_info = self.time_controller.get_time_info()
            with open(progress_file, 'w') as f:
                f.write(f"Experiment ID: {self.experiment_id[:8]}\n")
                f.write(f"Condition: {self.condition_name}\n")
                f.write(f"Model: {self.test_subject_model_spec}\n")
                f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\n")
                f.write(f"Turn: {turn_number}")
                if self.max_turns:
                    f.write(f" / {self.max_turns}")
                f.write(f"\n")

                if self.time_controller.mode == "simulated":
                    elapsed = time_info['simulated_elapsed_minutes']
                    total = time_info['simulated_duration_minutes']
                    pct = (elapsed / total * 100) if total > 0 else 0
                    f.write(f"Time: {elapsed:.1f} / {total} min ({pct:.1f}%)\n")

                    # Simple progress bar
                    bar_width = 40
                    filled = int(bar_width * elapsed / total) if total > 0 else 0
                    bar = '█' * filled + '░' * (bar_width - filled)
                    f.write(f"[{bar}]\n")

                # Add statistics
                stats = self.logger.get_stats()
                test_subject = stats.get('test_subject', {})
                reactor = stats.get('reactor', {})

                total_tokens = test_subject.get('total_tokens', 0) + reactor.get('total_tokens', 0)
                total_cost = test_subject.get('total_cost', 0) + reactor.get('total_cost', 0)
                total_calls = test_subject.get('api_calls', 0) + reactor.get('api_calls', 0)

                f.write(f"\n")
                f.write(f"Total tokens: {total_tokens:,}\n")
                f.write(f"Total cost: ${total_cost:.2f}\n")
                f.write(f"API calls: {total_calls}\n")

        try:
            while self.time_controller.should_continue(turn_number, self.max_turns):
                turn_number += 1
                turn_start = time.time()

                # Update progress file at start of each turn
                update_progress()

                if verbose:
                    print(f"\n--- Turn {turn_number} ---")
                    time_info = self.time_controller.get_time_info()
                    if self.time_controller.mode == "simulated":
                        print(f"Simulated Time: {time_info['simulated_current_time']} "
                              f"({time_info['simulated_elapsed_minutes']:.1f}/{time_info['simulated_duration_minutes']} min)")
                    print()

                # Get action from test subject
                subject_response = self.test_subject.get_next_action(environment_feedback)

            if verbose:
                print(f"Test Subject ({subject_response['_meta']['model']}):")
                print(f"  {subject_response['response'][:150]}..." if len(subject_response['response']) > 150
                      else f"  {subject_response['response']}")
                print(f"  Tokens: {subject_response['_meta']['tokens']['total_tokens']} "
                      f"({subject_response['_meta']['tokens']['duration']:.2f}s)")

            # Log the API call
            meta = subject_response['_meta']
            self.logger.log_api_call(
                "test_subject",
                meta['model'],
                meta['tokens']['input_tokens'],
                meta['tokens']['output_tokens'],
                meta['tokens']['duration'],
                {"response": subject_response['response'], "reasoning": subject_response['reasoning']}
            )

            # Check for tool actions
            if not subject_response['tool_actions']:
                if verbose:
                    print("\n  No tool actions detected.")

                # Still log the turn
                self.logger.log_turn(turn_number, {
                    "start_time": turn_start,
                    "subject_response": subject_response['response'],
                    "reasoning": subject_response['reasoning'],
                    "tool_actions": [],
                    "environment_responses": [],
                    "tokens_this_turn": meta['tokens']
                })

                environment_feedback = {
                    "observation": "Please use a tool to interact with the environment."
                }
                continue

            # Process each tool action
            environment_responses = []
            total_reactor_tokens = {"input": 0, "output": 0}

            for tool_action in subject_response['tool_actions']:
                if verbose:
                    print(f"\nTool: {tool_action['tool']} -> {tool_action['action'][:80]}...")

                # Get environment response
                env_response = self.reactor.process_action(
                    f"<{tool_action['tool']}>{tool_action['action']}</{tool_action['tool']}>"
                )

                if verbose:
                    print(f"  Environment: {env_response['observation'][:100]}...")
                    print(f"  Success: {env_response['success']}")
                    print(f"  Tokens: {env_response['_meta']['tokens']['total_tokens']}")

                # Log reactor API call
                reactor_meta = env_response['_meta']
                self.logger.log_api_call(
                    "reactor",
                    reactor_meta['model'],
                    reactor_meta['tokens']['input_tokens'],
                    reactor_meta['tokens']['output_tokens'],
                    reactor_meta['tokens']['duration'],
                    env_response
                )

                total_reactor_tokens["input"] += reactor_meta['tokens']['input_tokens']
                total_reactor_tokens["output"] += reactor_meta['tokens']['output_tokens']

                environment_responses.append(env_response)

            # Advance time
            time_advance = self.time_controller.advance_turn("normal")

            # Log the complete turn
            self.logger.log_turn(turn_number, {
                "start_time": turn_start,
                "subject_response": subject_response['response'],
                "reasoning": subject_response['reasoning'],
                "tool_actions": subject_response['tool_actions'],
                "environment_responses": environment_responses,
                "state_snapshot": self.reactor.get_state(),
                "tokens_this_turn": {
                    "test_subject": meta['tokens'],
                    "reactor": total_reactor_tokens
                },
                "time_info": time_advance
            })

            # Prepare feedback for next turn
            environment_feedback = environment_responses[-1] if environment_responses else None

        except Exception as e:
            # Emergency save on error (e.g., context window exceeded)
            if verbose:
                print(f"\n{'='*70}")
                print(f"⚠️  EXPERIMENT INTERRUPTED - Saving partial results")
                print(f"Error: {str(e)[:100]}...")
                print(f"Completed {turn_number} turns before interruption")
                print(f"{'='*70}\n")

            # Save partial log with error information
            log_path = self.logger.save(output_dir="logs/partial")

            # Add error metadata to the log file
            import json
            with open(log_path, 'r') as f:
                log_data = json.load(f)

            log_data['metadata']['interrupted'] = True
            log_data['metadata']['interruption_reason'] = str(e)
            log_data['metadata']['turns_completed'] = turn_number

            with open(log_path, 'w') as f:
                json.dump(log_data, f, indent=2)

            # Return partial results
            return {
                "log_path": log_path,
                "statistics": self.logger.get_stats(),
                "time_info": self.time_controller.get_time_info(),
                "experiment_id": self.experiment_id,
                "interrupted": True,
                "interruption_reason": str(e),
                "turns_completed": turn_number
            }

        # Finalize (normal completion)
        if verbose:
            print(f"\n{'='*70}")
            print(f"Simulation Complete - {turn_number} turns")
            time_info = self.time_controller.get_time_info()
            print(f"Real Duration: {time_info['real_elapsed_human']}")
            if self.time_controller.mode == "simulated":
                print(f"Simulated Duration: {time_info['simulated_elapsed_minutes']:.1f} minutes")
            print(f"{'='*70}\n")

        # Final progress update
        update_progress()

        # Save the log
        log_path = self.logger.save()

        # Clean up progress file (optional - keep for debugging)
        # progress_file.unlink(missing_ok=True)

        return {
            "log_path": log_path,
            "statistics": self.logger.get_stats(),
            "time_info": self.time_controller.get_time_info(),
            "experiment_id": self.experiment_id
        }

    def get_summary(self):
        """Get experiment summary."""
        stats = self.logger.get_stats()
        return {
            "experiment_id": self.experiment_id,
            "condition": self.condition_name,
            "statistics": stats,
            "time_info": self.time_controller.get_time_info()
        }
