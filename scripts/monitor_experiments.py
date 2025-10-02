#!/usr/bin/env python3
"""
Live monitor for running experiments with colored output
Usage: python3 scripts/monitor_experiments.py
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    """Clear terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def read_progress_files():
    """Read all progress files."""
    progress_dir = Path("experiments")
    progress_files = sorted(progress_dir.glob("progress_*.txt"))

    if not progress_files:
        return None

    experiments = []
    for pfile in progress_files:
        try:
            with open(pfile) as f:
                content = f.read()
                experiments.append({
                    'file': pfile.name,
                    'content': content
                })
        except:
            pass

    return experiments

def display_progress():
    """Display all progress files with formatting."""
    experiments = read_progress_files()

    clear_screen()

    print(f"{BOLD}{CYAN}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║          LIVE EXPERIMENT MONITOR                                  ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
    print()

    if not experiments:
        print(f"{YELLOW}No experiments currently running{RESET}")
        print(f"Waiting for experiments to start...")
        return

    print(f"{GREEN}Running {len(experiments)} experiment(s){RESET}")
    print()

    for i, exp in enumerate(experiments, 1):
        print(f"{BOLD}{BLUE}═══ Experiment {i} ═══{RESET}")
        print(f"{CYAN}{exp['content']}{RESET}")
        if i < len(experiments):
            print()

    print()
    print(f"{YELLOW}Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{YELLOW}Press Ctrl+C to stop monitoring{RESET}")

def main():
    """Main monitoring loop."""
    print("Starting experiment monitor...")
    print("Monitoring: experiments/progress_*.txt")
    print()

    try:
        while True:
            display_progress()
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n\n{GREEN}Monitoring stopped.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
