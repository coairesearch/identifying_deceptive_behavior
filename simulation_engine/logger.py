"""
Enhanced logging system for experiments
Tracks tokens, costs, timing, and full conversation details
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

class ExperimentLogger:
    """Comprehensive logging for simulation experiments."""

    # Token pricing (approximate, per 1M tokens)
    TOKEN_COSTS = {
        "deepseek-r1": {"input": 0.55, "output": 2.19},
        "kimi-k2": {"input": 0.30, "output": 0.30},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
        "mistral-small": {"input": 0.20, "output": 0.20},  # Custom OpenAI hosted
        "qwen3-4b-thinking": {"input": 0.10, "output": 0.10}  # Custom OpenAI hosted
    }

    def __init__(self, experiment_id: str, metadata: Dict):
        self.experiment_id = experiment_id
        self.metadata = metadata
        self.start_time = time.time()
        self.start_datetime = datetime.now()

        # Statistics tracking
        self.stats = {
            "test_subject": {
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "api_calls": 0
            },
            "reactor": {
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "api_calls": 0
            },
            "timing": {
                "total_duration_seconds": 0,
                "average_turn_duration": 0,
                "api_call_durations": []
            },
            "tool_usage": {},
            "behavior_patterns": []
        }

        # Full conversation log
        self.conversation_log = []

        # Turn-by-turn details
        self.turns = []

    def log_api_call(self, model_type: str, model_name: str,
                     input_tokens: int, output_tokens: int,
                     duration: float, response_data: Dict):
        """Log an API call with token counts and timing."""

        total_tokens = input_tokens + output_tokens

        # Calculate cost
        cost = self._calculate_cost(model_name, input_tokens, output_tokens)

        # Update stats
        stats_key = "test_subject" if model_type == "test_subject" else "reactor"
        self.stats[stats_key]["total_tokens"] += total_tokens
        self.stats[stats_key]["input_tokens"] += input_tokens
        self.stats[stats_key]["output_tokens"] += output_tokens
        self.stats[stats_key]["total_cost"] += cost
        self.stats[stats_key]["api_calls"] += 1
        self.stats["timing"]["api_call_durations"].append(duration)

        # Log the API call
        api_log = {
            "timestamp": datetime.now().isoformat(),
            "model_type": model_type,
            "model_name": model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost,
            "duration_seconds": duration,
            "response": response_data
        }

        self.conversation_log.append(api_log)

    def log_turn(self, turn_number: int, turn_data: Dict):
        """Log a complete turn with all details."""
        turn_start = turn_data.get("start_time", time.time())
        turn_end = time.time()
        turn_duration = turn_end - turn_start

        # Extract tool usage
        if "tool_actions" in turn_data:
            for action in turn_data["tool_actions"]:
                tool = action["tool"]
                self.stats["tool_usage"][tool] = self.stats["tool_usage"].get(tool, 0) + 1

        # Build comprehensive turn log
        turn_log = {
            "turn_number": turn_number,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": turn_duration,
            "test_subject_response": turn_data.get("subject_response"),
            "test_subject_reasoning": turn_data.get("reasoning"),
            "tool_actions": turn_data.get("tool_actions", []),
            "environment_responses": turn_data.get("environment_responses", []),
            "state_snapshot": turn_data.get("state_snapshot"),
            "tokens_this_turn": turn_data.get("tokens_this_turn", {}),
            "observations": []
        }

        # Extract key observations
        for env_resp in turn_data.get("environment_responses", []):
            turn_log["observations"].append({
                "observation": env_resp.get("observation"),
                "success": env_resp.get("success"),
                "side_effects": env_resp.get("side_effects", [])
            })

        self.turns.append(turn_log)

    def log_behavior_pattern(self, pattern_type: str, description: str,
                            turn_number: int, evidence: Any):
        """Log a detected behavior pattern."""
        self.stats["behavior_patterns"].append({
            "type": pattern_type,
            "description": description,
            "turn_number": turn_number,
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence
        })

    def finalize(self) -> Dict:
        """Finalize the log and return complete experiment data."""
        end_time = time.time()
        total_duration = end_time - self.start_time

        # Update timing stats
        self.stats["timing"]["total_duration_seconds"] = total_duration
        if self.turns:
            self.stats["timing"]["average_turn_duration"] = total_duration / len(self.turns)

        # Calculate combined stats
        total_tokens = (self.stats["test_subject"]["total_tokens"] +
                       self.stats["reactor"]["total_tokens"])
        total_cost = (self.stats["test_subject"]["total_cost"] +
                     self.stats["reactor"]["total_cost"])

        # Build final log structure
        final_log = {
            "experiment_id": self.experiment_id,
            "metadata": {
                **self.metadata,
                "start_time": self.start_datetime.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_duration_seconds": total_duration,
                "total_duration_human": str(timedelta(seconds=int(total_duration)))
            },
            "statistics": {
                **self.stats,
                "combined": {
                    "total_tokens": total_tokens,
                    "total_cost_usd": total_cost,
                    "total_api_calls": (self.stats["test_subject"]["api_calls"] +
                                       self.stats["reactor"]["api_calls"])
                }
            },
            "turns": self.turns,
            "full_conversation": self.conversation_log,
            "summary": self._generate_summary()
        }

        return final_log

    def _calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for API call."""
        # Find the right pricing
        for key, pricing in self.TOKEN_COSTS.items():
            if key in model_name.lower():
                input_cost = (input_tokens / 1_000_000) * pricing["input"]
                output_cost = (output_tokens / 1_000_000) * pricing["output"]
                return input_cost + output_cost

        # Default fallback
        return 0.0

    def _generate_summary(self) -> Dict:
        """Generate a summary of the experiment."""
        return {
            "total_turns": len(self.turns),
            "total_tool_uses": sum(self.stats["tool_usage"].values()),
            "most_used_tool": max(self.stats["tool_usage"].items(),
                                 key=lambda x: x[1])[0] if self.stats["tool_usage"] else None,
            "behavior_patterns_detected": len(self.stats["behavior_patterns"]),
            "estimated_cost_usd": self.stats["test_subject"]["total_cost"] + self.stats["reactor"]["total_cost"],
            "tokens_per_turn": (self.stats["test_subject"]["total_tokens"] +
                               self.stats["reactor"]["total_tokens"]) / len(self.turns) if self.turns else 0
        }

    def save(self, output_dir: str = "logs") -> Path:
        """Save the complete log to a JSON file."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        final_log = self.finalize()

        # Store finalized log for later access
        self.final_log = final_log

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        condition = self.metadata.get("condition", "unknown")
        filename = f"experiment_{condition}_{timestamp}_{self.experiment_id[:8]}.json"
        filepath = output_path / filename

        with open(filepath, 'w') as f:
            json.dump(final_log, f, indent=2)

        return filepath

    def get_stats(self) -> Dict:
        """Get current statistics (includes 'combined' if finalized)."""
        # If we have finalized stats, return those (includes 'combined')
        if hasattr(self, 'final_log'):
            return self.final_log['statistics']
        # Otherwise return current stats
        return self.stats.copy()
