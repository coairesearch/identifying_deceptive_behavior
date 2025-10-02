"""
Orchestrator - Runs simulation experiments
Coordinates between Test Subject LLM and Reactor LLM
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from .reactor import ReactorLLM
from .test_subject import TestSubjectLLM
import sys
sys.path.append(str(Path(__file__).parent.parent))
from prompts.templates import get_prompt

class SimulationOrchestrator:
    def __init__(self, world_state_path, condition_name, max_turns=20):
        """Initialize the orchestrator."""
        self.world_state_path = world_state_path
        self.condition_name = condition_name
        self.max_turns = max_turns

        # Load world state
        with open(world_state_path, 'r') as f:
            self.world_state = yaml.safe_load(f)

        # Initialize the environment simulator (Reactor)
        self.reactor = ReactorLLM(world_state_path)

        # Get the appropriate prompt for the condition
        initial_prompt = get_prompt(condition_name, self.world_state)

        # Initialize the test subject
        self.test_subject = TestSubjectLLM(initial_prompt)

        # Experiment log
        self.experiment_log = {
            "metadata": {
                "condition": condition_name,
                "world_state": world_state_path,
                "start_time": datetime.now().isoformat(),
                "max_turns": max_turns
            },
            "turns": []
        }

    def run_simulation(self):
        """Run the simulation experiment."""
        print(f"\n{'='*60}")
        print(f"Starting Simulation - Condition: {self.condition_name}")
        print(f"{'='*60}\n")

        environment_feedback = None

        for turn in range(self.max_turns):
            print(f"\n--- Turn {turn + 1} ---")

            # Get action from test subject
            subject_response = self.test_subject.get_next_action(environment_feedback)

            print(f"\nTest Subject Response:")
            print(f"  {subject_response['response'][:200]}..." if len(subject_response['response']) > 200 else f"  {subject_response['response']}")

            if subject_response['reasoning']:
                print(f"\nReasoning:")
                for r in subject_response['reasoning']:
                    print(f"  {r[:150]}..." if len(r) > 150 else f"  {r}")

            # Check if there are tool actions
            if not subject_response['tool_actions']:
                print("\n  No tool actions detected. Waiting for tool use...")

                # Log the turn
                self.experiment_log["turns"].append({
                    "turn": turn + 1,
                    "subject_response": subject_response['response'],
                    "reasoning": subject_response['reasoning'],
                    "tool_actions": [],
                    "environment_responses": []
                })

                # Prompt for tool use
                environment_feedback = {
                    "observation": "Waiting for you to use a tool. Please use one of the available tools: eyes, ears, legs, left_hand, right_hand"
                }
                continue

            # Process each tool action through the Reactor
            environment_responses = []

            for tool_action in subject_response['tool_actions']:
                print(f"\nTool Used: {tool_action['tool']}")
                print(f"  Action: {tool_action['action']}")

                # Get environment response from Reactor
                env_response = self.reactor.process_action(
                    f"<{tool_action['tool']}>{tool_action['action']}</{tool_action['tool']}>"
                )

                print(f"\nEnvironment Response:")
                print(f"  Observation: {env_response['observation']}")
                print(f"  Success: {env_response['success']}")

                if env_response.get('side_effects'):
                    print(f"  Side Effects: {env_response['side_effects']}")

                environment_responses.append(env_response)

            # Log the turn
            self.experiment_log["turns"].append({
                "turn": turn + 1,
                "subject_response": subject_response['response'],
                "reasoning": subject_response['reasoning'],
                "tool_actions": subject_response['tool_actions'],
                "environment_responses": environment_responses
            })

            # Prepare feedback for next turn (use the last environment response)
            environment_feedback = environment_responses[-1] if environment_responses else None

            # Check termination conditions
            if self._should_terminate():
                print("\n\nTermination condition met.")
                break

        # Finalize experiment
        self.experiment_log["metadata"]["end_time"] = datetime.now().isoformat()
        self.experiment_log["metadata"]["total_turns"] = len(self.experiment_log["turns"])
        self.experiment_log["final_state"] = self.reactor.get_state()

        print(f"\n{'='*60}")
        print(f"Simulation Complete - {len(self.experiment_log['turns'])} turns")
        print(f"{'='*60}\n")

        return self.experiment_log

    def _should_terminate(self):
        """Check if simulation should terminate."""
        # For now, just let it run to max_turns
        # In future, can add conditions like:
        # - Time limit exceeded
        # - Critical behavior detected
        # - No activity for X turns
        return False

    def save_log(self, output_dir="logs"):
        """Save the experiment log."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{self.condition_name}_{timestamp}.json"
        filepath = output_path / filename

        with open(filepath, 'w') as f:
            json.dump(self.experiment_log, f, indent=2)

        print(f"\nExperiment log saved to: {filepath}")
        return filepath

    def get_summary(self):
        """Get a summary of the experiment."""
        total_turns = len(self.experiment_log['turns'])
        total_tool_uses = sum(
            len(turn['tool_actions']) for turn in self.experiment_log['turns']
        )

        # Count tool types
        tool_counts = {}
        for turn in self.experiment_log['turns']:
            for action in turn['tool_actions']:
                tool = action['tool']
                tool_counts[tool] = tool_counts.get(tool, 0) + 1

        return {
            "condition": self.condition_name,
            "total_turns": total_turns,
            "total_tool_uses": total_tool_uses,
            "tool_usage": tool_counts,
            "final_state": self.experiment_log.get('final_state')
        }
