#!/usr/bin/env python3
"""
Analysis tool for experiment logs
Replay, visualize, and analyze experiment results
"""

import json
import sys
from pathlib import Path
from datetime import datetime

class ExperimentAnalyzer:
    """Analyze experiment logs."""

    def __init__(self, log_path):
        with open(log_path, 'r') as f:
            self.data = json.load(f)

    def print_summary(self):
        """Print experiment summary."""
        meta = self.data['metadata']
        stats = self.data['statistics']

        print("\n" + "="*70)
        print("EXPERIMENT SUMMARY")
        print("="*70)
        print(f"\nExperiment ID: {self.data['experiment_id']}")
        print(f"Condition: {meta['condition']}")
        print(f"Start Time: {meta['start_time']}")
        print(f"Duration: {meta['total_duration_human']}")

        print(f"\n📊 STATISTICS")
        print("-"*70)
        print(f"Total Turns: {self.data['summary']['total_turns']}")
        print(f"Total Tool Uses: {self.data['summary']['total_tool_uses']}")
        print(f"Most Used Tool: {self.data['summary']['most_used_tool']}")

        print(f"\n💰 COSTS")
        print("-"*70)
        print(f"Test Subject:")
        print(f"  Total Tokens: {stats['test_subject']['total_tokens']:,}")
        print(f"  Input: {stats['test_subject']['input_tokens']:,} | Output: {stats['test_subject']['output_tokens']:,}")
        print(f"  Cost: ${stats['test_subject']['total_cost']:.4f}")
        print(f"  API Calls: {stats['test_subject']['api_calls']}")

        print(f"\nReactor:")
        print(f"  Total Tokens: {stats['reactor']['total_tokens']:,}")
        print(f"  Input: {stats['reactor']['input_tokens']:,} | Output: {stats['reactor']['output_tokens']:,}")
        print(f"  Cost: ${stats['reactor']['total_cost']:.4f}")
        print(f"  API Calls: {stats['reactor']['api_calls']}")

        print(f"\nCombined:")
        print(f"  Total Tokens: {stats['combined']['total_tokens']:,}")
        print(f"  Total Cost: ${stats['combined']['total_cost_usd']:.4f}")
        print(f"  Total API Calls: {stats['combined']['total_api_calls']}")
        print(f"  Tokens/Turn: {self.data['summary']['tokens_per_turn']:.0f}")

        print(f"\n🛠️  TOOL USAGE")
        print("-"*70)
        for tool, count in stats['tool_usage'].items():
            pct = (count / self.data['summary']['total_tool_uses'] * 100)
            print(f"  {tool:12} : {count:3} ({pct:5.1f}%)")

        if stats['behavior_patterns']:
            print(f"\n⚠️  BEHAVIOR PATTERNS DETECTED: {len(stats['behavior_patterns'])}")
            print("-"*70)
            for pattern in stats['behavior_patterns']:
                print(f"  Turn {pattern['turn_number']}: {pattern['type']}")
                print(f"    {pattern['description']}")

    def replay_conversation(self, start_turn=1, end_turn=None):
        """Replay the conversation."""
        turns = self.data['turns']
        if end_turn is None:
            end_turn = len(turns)

        print(f"\n{'='*70}")
        print(f"CONVERSATION REPLAY (Turns {start_turn}-{end_turn})")
        print(f"{'='*70}")

        for turn in turns[start_turn-1:end_turn]:
            print(f"\n--- Turn {turn['turn_number']} ({turn['timestamp']}) ---")

            print(f"\n🤖 Test Subject:")
            print(f"  {turn['test_subject_response']}")

            if turn['test_subject_reasoning']:
                print(f"\n  💭 Reasoning:")
                for reasoning in turn['test_subject_reasoning']:
                    print(f"     {reasoning[:200]}...")

            if turn['tool_actions']:
                print(f"\n  🛠️  Actions:")
                for action in turn['tool_actions']:
                    print(f"     {action['tool']}: {action['action']}")

            if turn['observations']:
                print(f"\n  🌍 Environment:")
                for obs in turn['observations']:
                    print(f"     {obs['observation'][:150]}...")
                    if obs['side_effects']:
                        print(f"     Side effects: {obs['side_effects']}")

    def export_conversation_text(self, output_path):
        """Export full conversation to text file."""
        with open(output_path, 'w') as f:
            f.write(f"EXPERIMENT LOG\n")
            f.write(f"ID: {self.data['experiment_id']}\n")
            f.write(f"Condition: {self.data['metadata']['condition']}\n")
            f.write(f"Duration: {self.data['metadata']['total_duration_human']}\n")
            f.write("="*70 + "\n\n")

            for turn in self.data['turns']:
                f.write(f"TURN {turn['turn_number']}\n")
                f.write(f"Time: {turn['timestamp']}\n")
                f.write(f"\nTest Subject:\n{turn['test_subject_response']}\n")

                if turn['test_subject_reasoning']:
                    f.write(f"\nReasoning:\n")
                    for r in turn['test_subject_reasoning']:
                        f.write(f"  {r}\n")

                f.write(f"\nActions:\n")
                for action in turn['tool_actions']:
                    f.write(f"  {action['tool']}: {action['action']}\n")

                f.write(f"\nObservations:\n")
                for obs in turn['observations']:
                    f.write(f"  {obs['observation']}\n")

                f.write("\n" + "-"*70 + "\n\n")

        print(f"Conversation exported to: {output_path}")

    def get_token_timeline(self):
        """Get token usage over time."""
        timeline = []
        cumulative = {"test_subject": 0, "reactor": 0}

        for turn in self.data['turns']:
            tokens = turn.get('tokens_this_turn', {})
            if 'test_subject' in tokens:
                cumulative['test_subject'] += tokens['test_subject'].get('total_tokens', 0)
            if 'reactor' in tokens:
                cumulative['reactor'] += tokens['reactor'].get('total_tokens', 0)

            timeline.append({
                "turn": turn['turn_number'],
                "timestamp": turn['timestamp'],
                "cumulative_test_subject": cumulative['test_subject'],
                "cumulative_reactor": cumulative['reactor'],
                "cumulative_total": cumulative['test_subject'] + cumulative['reactor']
            })

        return timeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python analysis_tool.py <log_file.json> [command]")
        print("\nCommands:")
        print("  summary     - Print experiment summary (default)")
        print("  replay      - Replay full conversation")
        print("  replay N-M  - Replay turns N to M")
        print("  export      - Export conversation to text file")
        print("  tokens      - Show token usage timeline")
        sys.exit(1)

    log_path = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "summary"

    analyzer = ExperimentAnalyzer(log_path)

    if command == "summary":
        analyzer.print_summary()

    elif command.startswith("replay"):
        if len(sys.argv) > 3 and '-' in sys.argv[3]:
            start, end = map(int, sys.argv[3].split('-'))
            analyzer.replay_conversation(start, end)
        else:
            analyzer.replay_conversation()

    elif command == "export":
        output = log_path.replace('.json', '_conversation.txt')
        analyzer.export_conversation_text(output)

    elif command == "tokens":
        timeline = analyzer.get_token_timeline()
        print("\nTOKEN USAGE TIMELINE")
        print("="*70)
        for entry in timeline:
            print(f"Turn {entry['turn']:2} | "
                  f"Test Subject: {entry['cumulative_test_subject']:6,} | "
                  f"Reactor: {entry['cumulative_reactor']:6,} | "
                  f"Total: {entry['cumulative_total']:7,}")

if __name__ == "__main__":
    main()
